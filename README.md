🚀 AstroLanding Guardian

AstroLanding Guardian is a desktop AI assistant that evaluates whether a spacecraft landing is safe under specific planetary conditions.

It combines machine learning predictions with a real-time feedback loop, allowing the system to track and visualize its own performance over time.

🌌 Overview

Provide environmental conditions such as gravity, atmosphere, and terrain, and the system will predict:

✅ SAFE TO LAND
❌ UNSAFE TO LAND

After each prediction, you can confirm the real outcome, allowing the app to update a live confusion matrix that reflects real-world accuracy.

✨ Key Features
🧠 AI-Powered Decision Making
Decision Tree Classifier (scikit-learn)
Binary classification for landing safety
📊 Real-Time Performance Tracking
Model accuracy score
Static confusion matrix (test set)
Live confusion matrix (user-validated outcomes)
🖥️ Interactive Desktop Interface
Built with PyQt5
Clean input system for mission conditions
Popup summaries for predictions
🔄 Continuous Learning Feedback Loop
Confirm predictions after each run
Automatically updates performance metrics
🎵 Quality of Life
Background music loop (Windows)
Mute / unmute toggle
Reset inputs instantly
🧪 Input Parameters

The model evaluates the following:

Atmosphere
Gravity
Temperature
Radiation
Water Presence
Wind Speed
Toxicity
Terrain Type
🏗️ Tech Stack
Language: Python
UI Framework: PyQt5
Machine Learning: scikit-learn
Data Processing: pandas
Audio: winsound (Windows only)
📁 Project Structure
.
├── main.py                     # UI + application logic
├── MySpaceDecisionTree.py     # ML model + prediction logic
├── space_landing_full.csv     # Dataset
└── README.md
⚙️ Installation
1. Clone the repository
git clone https://github.com/SaraLarkem/Astro-landing-guardian.git
cd astro-landing-guardian
2. Install dependencies
pip install pandas scikit-learn pyqt5
3. Run the application
python main.py
🤖 Model Details
Data Processing
Validates dataset structure
Encodes:
Water_Present: Yes/No → 1/0
Safe_to_Land: Safe/Unsafe → 1/0
One-hot encodes Terrain_Type
Model
Algorithm: DecisionTreeClassifier
Train/test split applied
Outputs:
Accuracy score
Fixed confusion matrix (labels=[0,1])
Prediction
Accepts a single input sample
Ensures feature alignment with training data
Produces binary classification
📈 Evaluation System
📊 Test Reference Matrix (Static)
Generated during model training
Represents baseline performance
🔄 Live Confusion Matrix (Dynamic)
Updated after each confirmed prediction
Reflects real-world usage accuracy

This creates a feedback loop where the model is constantly being evaluated against reality.

🚀 Usage Flow
Enter landing conditions in the GUI
Run prediction
View result + metrics
Confirm actual outcome
Watch the live confusion matrix update
🧭 In One Sentence

A PyQt + scikit-learn desktop application that predicts spacecraft landing safety and continuously evaluates itself through user-confirmed outcomes.

📌 Future Improvements
Add support for additional ML models (Random Forest, XGBoost)
Export performance reports
Cross-platform audio support
Model retraining from live data
📜 License

This project is open-source and available under the MIT License.
