import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
import joblib
import os

# Define path and filename
path = r"C:/Users/dhrit/Downloads/rockfall_prototype/data/"
filename = "balanced_synthetic_rockfall_data.csv"

# Load dataset
file_path = os.path.join(path, filename)
df = pd.read_csv(file_path)

# Possible categorical columns
possible_categorical_cols = ["Rock_Type", "Soil_Type", "Lithology", "Vegetation", "Land_Cover"]

# Only keep the ones that exist in this dataset
categorical_cols = [col for col in possible_categorical_cols if col in df.columns]

# One-hot encode categorical columns
df = pd.get_dummies(df, columns=categorical_cols)

# Features and Target
X = df.drop(columns=["Rockfall_Event"])
y = df["Rockfall_Event"]

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train Random Forest
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Predictions
y_pred = model.predict(X_test)

# Evaluation
accuracy = accuracy_score(y_test, y_pred)
print("✅ Model trained successfully!")
print(f"🎯 Accuracy: {accuracy:.4f}")
print("\n📊 Classification Report:\n", classification_report(y_test, y_pred))
print("🧩 Confusion Matrix:\n", confusion_matrix(y_test, y_pred))

# Save model
model_path = r"C:/Users/dhrit/Downloads/rockfall_prototype/model/rockfall_model.pkl"
os.makedirs(os.path.dirname(model_path), exist_ok=True)  # create folder if not exists
joblib.dump(model, model_path)

print("\n💾 Model saved at:", model_path)
print("🔑 Features used:", X.columns.tolist())
