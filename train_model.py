import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score, confusion_matrix
import joblib

# ----------------------------------------------------------
# 1. LOAD DATASET
# ----------------------------------------------------------
try:
    df = pd.read_csv("space_landing_full.csv")
except FileNotFoundError:
    raise FileNotFoundError("ERROR: space_landing_full.csv not found in folder.")

# ----------------------------------------------------------
# 2. ENCODE CATEGORICAL COLUMNS
# ----------------------------------------------------------
df["Water_Present"] = df["Water_Present"].map({"Yes": 1, "No": 0})
df["Safe_to_Land"] = df["Safe_to_Land"].map({"Safe": 1, "Unsafe": 0})

# ----------------------------------------------------------
# 3. FEATURES USED IN THE MODEL
# ----------------------------------------------------------
feature_cols = [
    "Atmosphere_Quality",
    "Temperature",
    "Gravity",
    "Radiation_Level",
    "Magnetic_Field_Strength",
    "Wind_Speed",
    "Toxicity_Level"
]

X = df[feature_cols]
y = df["Safe_to_Land"]

# ----------------------------------------------------------
# 4. SPLIT DATA
# ----------------------------------------------------------
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# ----------------------------------------------------------
# 5. TRAIN DECISION TREE
# ----------------------------------------------------------
model = DecisionTreeClassifier(random_state=42)
model.fit(X_train, y_train)

# ----------------------------------------------------------
# 6. EVALUATE
# ----------------------------------------------------------
pred = model.predict(X_test)
acc = accuracy_score(y_test, pred)
matrix = confusion_matrix(y_test, pred)

print("\n--- MODEL TRAINED SUCCESSFULLY ---")
print("Accuracy:", round(acc * 100, 2), "%")
print("\nConfusion Matrix:")
print(matrix)

# ----------------------------------------------------------
# 7. SAVE MODEL TO FILE
# ----------------------------------------------------------
joblib.dump(model, "landing_model.pkl")
print("\nModel saved as landing_model.pkl\n")
