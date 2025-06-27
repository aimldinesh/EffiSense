# Main pipeline script to execute:
#   1. Data Processing
#   2. Model Training & Evaluation
# ───────────────────────────────────────────────

from src.data_processing import DataProcessing
from src.model_training import ModelTraining

if __name__ == "__main__":
    # Step 1: Run the data processing pipeline
    processor = DataProcessing(
        input_path="artifacts/raw/data.csv",  # Raw data location
        output_path="artifacts/processed",  # Where to save preprocessed data
    )
    processor.run()

    # Step 2: Train and evaluate model
    trainer = ModelTraining(
        processed_data_path="artifacts/processed/",  # Use preprocessed data
        model_output_path="artifacts/models/",  # Save model & metrics here
    )
    trainer.run()
