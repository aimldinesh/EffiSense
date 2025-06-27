import pandas as pd
import numpy as np
import joblib
import os
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, StandardScaler
from src.logger import get_logger
from src.custom_exception import CustomException

# Initialize logger
logger = get_logger(__name__)


class DataProcessing:
    """
    A class to handle data loading, preprocessing, encoding, scaling,
    and saving processed artifacts for machine learning workflow.
    """

    def __init__(self, input_path, output_path):
        self.input_path = input_path
        self.output_path = output_path
        self.df = None
        self.features = None

        # Create output directory if not exists
        os.makedirs(self.output_path, exist_ok=True)
        logger.info("Data Processing initialized...")

    def load_data(self):
        """Load dataset from CSV file"""
        try:
            self.df = pd.read_csv(self.input_path)
            logger.info(f"Data loaded successfully with shape: {self.df.shape}")
        except Exception as e:
            logger.error(f"Error while loading data: {e}")
            raise CustomException("Failed to load data", e)

    def preprocess(self):
        """Preprocess the dataset: clean, encode, and extract time features"""
        try:
            # Convert Timestamp to datetime
            self.df["Timestamp"] = pd.to_datetime(self.df["Timestamp"], errors="coerce")

            # Convert relevant columns to category type
            categorical_cols = ["Operation_Mode", "Efficiency_Status"]
            for col in categorical_cols:
                self.df[col] = self.df[col].astype("category")

            # Extract time-based features
            self.df["Year"] = self.df["Timestamp"].dt.year
            self.df["Month"] = self.df["Timestamp"].dt.month
            self.df["Day"] = self.df["Timestamp"].dt.day
            self.df["Hour"] = self.df["Timestamp"].dt.hour

            # Drop unnecessary columns
            self.df.drop(columns=["Timestamp", "Machine_ID"], inplace=True)

            # Encode categorical columns using Label Encoding
            columns_to_encode = ["Efficiency_Status", "Operation_Mode"]
            for col in columns_to_encode:
                le = LabelEncoder()
                self.df[col] = le.fit_transform(self.df[col])

            logger.info("data preprocessing completed.")

        except Exception as e:
            logger.error(f"Error while preprocessing data: {e}")
            raise CustomException("Failed to preprocess data", e)

    def split_and_scale_and_save(self):
        """Split the dataset, scale features, and save train/test sets and scaler"""
        try:
            # Define features
            self.features = [
                "Operation_Mode",
                "Temperature_C",
                "Vibration_Hz",
                "Power_Consumption_kW",
                "Network_Latency_ms",
                "Packet_Loss_%",
                "Quality_Control_Defect_Rate_%",
                "Production_Speed_units_per_hr",
                "Predictive_Maintenance_Score",
                "Error_Rate_%",
                "Year",
                "Month",
                "Day",
                "Hour",
            ]

            # Separate features and target
            X = self.df[self.features]
            y = self.df["Efficiency_Status"]

            # Scale features using StandardScaler
            scaler = StandardScaler()
            X_scaled = scaler.fit_transform(X)

            # Split into training and testing sets (80/20)
            X_train, X_test, y_train, y_test = train_test_split(
                X_scaled, y, test_size=0.2, random_state=42, stratify=y
            )

            # Save the processed data
            joblib.dump(X_train, os.path.join(self.output_path, "X_train.pkl"))
            joblib.dump(X_test, os.path.join(self.output_path, "X_test.pkl"))
            joblib.dump(y_train, os.path.join(self.output_path, "y_train.pkl"))
            joblib.dump(y_test, os.path.join(self.output_path, "y_test.pkl"))
            joblib.dump(scaler, os.path.join(self.output_path, "scaler.pkl"))

            logger.info("Data successfully split, scaled and saved.")

        except Exception as e:
            logger.error(f"Error while splitting/scaling/saving data: {e}")
            raise CustomException("Failed to split, scale, and save data", e)

    def run(self):
        """Run the full data processing pipeline"""
        self.load_data()
        self.preprocess()
        self.split_and_scale_and_save()


# Entry point for script execution
if __name__ == "__main__":
    processor = DataProcessing("artifacts/raw/data.csv", "artifacts/processed")
    processor.run()
