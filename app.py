from flask import Flask, render_template, request
import joblib
import numpy as np
import datetime

app = Flask(__name__)

MODEL_PATH = "artifacts/models/model.pkl"
SCALER_PATH = "artifacts/processed/scaler.pkl"

model = joblib.load(MODEL_PATH)
scaler = joblib.load(SCALER_PATH)

FEATURES = [
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

LABELS = {0: "High", 1: "Low", 2: "Medium"}


@app.route("/", methods=["GET", "POST"])
def index():
    prediction = None
    error = None
    default_values = {}

    # Current date/time defaults
    now = datetime.datetime.now()
    default_values["Year"] = now.year
    default_values["Month"] = now.month
    default_values["Day"] = now.day
    default_values["Hour"] = now.hour

    if request.method == "POST":
        try:
            input_data = []

            for feature in FEATURES:
                value = request.form.get(feature)
                if feature == "Operation_Mode":
                    input_data.append(int(value))
                elif feature in ["Year", "Month", "Day", "Hour"]:
                    input_data.append(int(value))
                else:
                    try:
                        input_data.append(float(value))
                    except ValueError:
                        raise ValueError(
                            f"Invalid input for {feature}. Please enter a number."
                        )

            input_array = np.array(input_data).reshape(1, -1)
            scaled_array = scaler.transform(input_array)
            pred = model.predict(scaled_array)[0]
            prediction = LABELS.get(pred, "Unknown")

        except Exception as e:
            error = str(e)

    return render_template(
        "index.html",
        prediction=prediction,
        error=error,
        features=FEATURES,
        default_values=default_values,
    )


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
