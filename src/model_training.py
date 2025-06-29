import os
import joblib
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    accuracy_score,
    recall_score,
    precision_score,
    f1_score,
    classification_report,
)

from src.logger import get_logger
from src.custom_exception import CustomException

logger = get_logger(__name__)


class ModelTraining:
    """
    Train a model on pre-processed data, save the model,
    and log + persist evaluation metrics.
    """

    def __init__(self, processed_data_path: str, model_output_path: str):
        self.processed_path = processed_data_path
        self.model_path = model_output_path
        self.clf = None
        self.X_train = self.X_test = self.y_train = self.y_test = None

        os.makedirs(self.model_path, exist_ok=True)
        logger.info("Model Training initialized...")

    # -------------------------------------------------
    def load_data(self):
        """Load train/test splits generated by the preprocessing step"""
        try:
            self.X_train = joblib.load(os.path.join(self.processed_path, "X_train.pkl"))
            self.X_test = joblib.load(os.path.join(self.processed_path, "X_test.pkl"))
            self.y_train = joblib.load(os.path.join(self.processed_path, "y_train.pkl"))
            self.y_test = joblib.load(os.path.join(self.processed_path, "y_test.pkl"))
            logger.info("Processed data loaded successfully.")
        except Exception as e:
            logger.error(f"Error while loading data: {e}")
            raise CustomException("Failed to load processed data", e)

    # -------------------------------------------------
    def train_model(self):
        """Fit a Logistic Regression classifier and persist it"""
        try:
            self.clf = LogisticRegression(max_iter=1000, random_state=42)
            self.clf.fit(self.X_train, self.y_train)

            joblib.dump(self.clf, os.path.join(self.model_path, "model.pkl"))
            logger.info("Model trained and saved successfully.")
        except Exception as e:
            logger.error(f"Model training failed: {e}")
            raise CustomException("Failed to train model", e)

    # -------------------------------------------------
    def evaluate_model(self):
        """Evaluate the trained model, log metrics, and save them to CSV"""
        try:
            y_pred = self.clf.predict(self.X_test)

            # ── Core metrics ─────────────────────────────────────────────
            accuracy = accuracy_score(self.y_test, y_pred)
            precision = precision_score(self.y_test, y_pred, average="weighted")
            recall = recall_score(self.y_test, y_pred, average="weighted")
            f1 = f1_score(self.y_test, y_pred, average="weighted")

            # ── Classification report (text) ────────────────────────────
            class_report = classification_report(self.y_test, y_pred)
            logger.info("\n" + class_report)

            # ── Persist metrics to CSV ───────────────────────────────────
            metrics_df = pd.DataFrame(
                {
                    "metric": ["accuracy", "precision", "recall", "f1_score"],
                    "value": [accuracy, precision, recall, f1],
                }
            )
            metrics_csv_path = os.path.join(self.model_path, "evaluation_metrics.csv")
            metrics_df.to_csv(metrics_csv_path, index=False)

            # ── Log concise summary ─────────────────────────────────────
            logger.info(f"Accuracy : {accuracy:.4f}")
            logger.info(f"Precision: {precision:.4f}")
            logger.info(f"Recall   : {recall:.4f}")
            logger.info(f"F1 Score : {f1:.4f}")
            logger.info(f"Metrics saved to {metrics_csv_path}")

        except Exception as e:
            logger.error(f"Error during evaluation: {e}")
            raise CustomException("Failed to evaluate model", e)

    # -------------------------------------------------
    def run(self):
        """Execute full workflow: load → train → evaluate"""
        self.load_data()
        self.train_model()
        self.evaluate_model()


# Script entry point
if __name__ == "__main__":
    trainer = ModelTraining("artifacts/processed/", "artifacts/models/")
    trainer.run()
