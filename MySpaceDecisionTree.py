import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import confusion_matrix, accuracy_score


class MySpaceDecisionTree:
    """
    Decision-tree model used by the GUI.

    Features used:
      - Atmosphere_Quality
      - Temperature
      - Gravity
      - Radiation_Level
      - Water_Present
      - Wind_Speed
      - Toxicity_Level
      - Terrain_Type (one-hot encoded)
    """

    def __init__(self, csv_path: str = "space_landing_full.csv", seed: int = 1):
        self.csv_path = csv_path
        self.seed = seed
        self.model: DecisionTreeClassifier | None = None
        self.feature_cols: list[str] = []
        self.terrain_categories: list[str] = []
        self.accuracy_: float | None = None
        self.confusion_ = None

        # Load and preprocess immediately
        self._load_and_prepare()

    # ------------------------------------------------------------------
    # DATA LOADING + PREPROCESSING
    # ------------------------------------------------------------------
    def _load_and_prepare(self) -> None:
        try:
            df = pd.read_csv(self.csv_path)
        except FileNotFoundError as e:
            raise FileNotFoundError(
                f"Could not find data file: {self.csv_path}"
            ) from e

        required_cols = [
            "Atmosphere_Quality",
            "Temperature",
            "Gravity",
            "Radiation_Level",
            "Water_Present",
            "Wind_Speed",
            "Toxicity_Level",
            "Terrain_Type",
            "Safe_to_Land",
        ]
        missing = [c for c in required_cols if c not in df.columns]
        if missing:
            raise ValueError(f"CSV is missing columns: {missing}")

        # Map Yes/No → 1/0
        df["Water_Present"] = df["Water_Present"].map({"Yes": 1, "No": 0})
        df["Safe_to_Land"] = df["Safe_to_Land"].map({"Safe": 1, "Unsafe": 0})

        # Collect unique terrain categories
        self.terrain_categories = sorted(df["Terrain_Type"].unique())

        # One-hot encode terrain
        terrain_dummies = pd.get_dummies(df["Terrain_Type"], prefix="Terrain")

        # IMPORTANT — this is the exact order features must follow
        numeric_cols = [
            "Atmosphere_Quality",
            "Temperature",     # MUST be 2nd
            "Gravity",         # MUST be 3rd
            "Radiation_Level",
            "Water_Present",
            "Wind_Speed",
            "Toxicity_Level",
        ]

        X = pd.concat([df[numeric_cols], terrain_dummies], axis=1)
        y = df["Safe_to_Land"]

        self.feature_cols = list(X.columns)
        self._X = X
        self._y = y

    # ------------------------------------------------------------------
    # TRAINING
    # ------------------------------------------------------------------
    def train(self):
        """Train the decision tree and return (accuracy, confusion_matrix)."""

        X_train, X_test, y_train, y_test = train_test_split(
            self._X,
            self._y,
            test_size=0.25,
            random_state=self.seed,
            stratify=self._y,
        )

        self.model = DecisionTreeClassifier(random_state=self.seed)
        self.model.fit(X_train, y_train)

        y_pred = self.model.predict(X_test)
        acc = accuracy_score(y_test, y_pred)
        # Always keep a stable 2x2 layout: [[TN, FP], [FN, TP]]
        cm = confusion_matrix(y_test, y_pred, labels=[0, 1])

        self.accuracy_ = float(acc)
        self.confusion_ = cm
        return self.accuracy_, self.confusion_

    # ------------------------------------------------------------------
    # BUILD FEATURE VECTOR FOR NEW INPUTS
    # ------------------------------------------------------------------
    def _vector_from_inputs(
        self,
        atmosphere: float,
        gravity: float,
        temperature: float,
        radiation: float,
        water_present: int,
        wind_speed: float,
        toxicity: float,
        terrain: str,
    ):
        """Create a feature vector in EXACT training column order."""

        if self.model is None:
            raise RuntimeError("Model has not been trained yet.")

        # Start all values as zero
        values = {col: 0.0 for col in self.feature_cols}

        # EXACT ORDER MUST MATCH numeric_cols
        values["Atmosphere_Quality"] = atmosphere
        values["Temperature"] = temperature     # correct order
        values["Gravity"] = gravity             # correct order
        values["Radiation_Level"] = radiation
        values["Water_Present"] = int(water_present)
        values["Wind_Speed"] = wind_speed
        values["Toxicity_Level"] = toxicity

        # One-hot terrain
        terrain_col = f"Terrain_{terrain}"
        if terrain_col in values:
            values[terrain_col] = 1.0

        # Return model-ready vector in exact column order
        return [values[col] for col in self.feature_cols]

    # ------------------------------------------------------------------
    # PREDICTION FOR ONE INPUT SET
    # ------------------------------------------------------------------
    def predict_single(
        self,
        atmosphere: float,
        gravity: float,
        temperature: float,
        radiation: float,
        water_present: int,
        wind_speed: float,
        toxicity: float,
        terrain: str,
    ) -> int:

        if self.model is None:
            raise RuntimeError("Model has not been trained yet.")

        vec = self._vector_from_inputs(
            atmosphere,
            gravity,
            temperature,
            radiation,
            water_present,
            wind_speed,
            toxicity,
            terrain,
        )

        pred = self.model.predict([vec])[0]
        return int(pred)
