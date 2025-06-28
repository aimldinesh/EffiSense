![Python](https://img.shields.io/badge/Python-3.10-blue?logo=python)
![Flask](https://img.shields.io/badge/Flask-Web_App-lightgrey?logo=flask)
![Docker](https://img.shields.io/badge/Docker-Container-blue?logo=docker)
![Kubernetes](https://img.shields.io/badge/Kubernetes-Orchestration-blue?logo=kubernetes)
![CI/CD](https://img.shields.io/badge/CI/CD-Jenkins%20%7C%20ArgoCD-success?logo=githubactions)

## EffiSense: End-to-End MLOps Pipeline for Machine Efficiency Prediction

EffiSense is a complete MLOps pipeline that predicts the **efficiency status (High | Medium | Low)** of industrial machines using intelligent manufacturing data.

It features a fully automated CI/CD setup using **Jenkins**, **ArgoCD**, **Docker**, **Kubernetes**, and **GitHub Webhooks** for seamless deployment.

---
## 📚 Table of Contents

- [🏛️ Project Structure](#-project-structure)
- [🔁 Project Workflow](#-project-workflow)
- [🛠️ Tech Stack](#-tech-stack)
- [📦 Installation & Setup](#-installation--setup)
- [🤖 Model Details](#-model-details)
- [🚀 CI/CD Pipeline](#-cicd-pipeline)
- [📌 Future Improvements](#-future-improvements)
- [🙌 Author](#-author)
- [🤝 Contributing](#-contributing)

---

## 🏛️ Project Structure
```
EffiSense/
├── app.py                  # Flask app with prediction logic
├── src/
│   ├── data_processing.py   # Preprocessing pipeline
│   ├── model_training.py    # Model training & evaluation
│   ├── logger.py
│   └── custom_exception.py
├── templates/
│   └── index.html          # Flask frontend template
├── static/
│   └── style.css           # Web UI styling
├── manifests/
│   ├── deployment.yml
│   └── service.yml
├── artifacts/
│   ├── raw/data.csv
│   ├── processed/*.pkl
│   └── models/*.pkl
├── Dockerfile
├── Jenkinsfile
└── README.md
```
---

## 🔁 Project Workflow

```mermaid
%% EffiSense MLOps Workflow (3-row layout)
flowchart TB
    %% ──────────────── 1️⃣ Development & Experimentation ────────────────
    subgraph DEV [Development & Experiment]
        direction LR
        A[Project Setup] --> B[Jupyter Notebook Testing] --> C[Data Processing] --> D[Model Training]
    end

    %% ──────────────── 2️⃣ Packaging & Infrastructure ────────────────
    subgraph PKG [Packaging & Infrastructure]
        direction LR
        D --> E[User App Building] --> F[Dockerfile & K8s Manifests] --> G[Data & Code Versioning] --> H[VM Instance Setup]
    end

    %% ──────────────── 3️⃣ CI / CD Pipeline ────────────────
    subgraph CICD [CI / CD Pipeline]
        direction LR
        H --> I[Jenkins Setup] --> J[GitHub ↔ Jenkins] --> K[CI Pipeline] --> L[ArgoCD Install & Config] --> M[CD Code & Automation] --> N[ArgoCD Deployment]
    end

    %% Optional style tweaks (colors, borders)
    classDef stage fill:#E8F7FF,stroke:#0366D6,stroke-width:2px;
    class A,B,C,D,E,F,G,H,I,J,K,L,M,N stage;
```

---
## 🛠️ Tech Stack

EffiSense integrates a modern MLOps toolchain combining machine learning, web app development, containerization, orchestration, and CI/CD automation.

| Layer              | Tools & Technologies                                      |
|--------------------|-----------------------------------------------------------|
| **Programming**     | Python 3.10                                               |
| **ML Libraries**    | scikit-learn, pandas, numpy, joblib                      |
| **Web Framework**   | Flask (with HTML & CSS)                                  |
| **Containerization**| Docker                                                   |
| **Orchestration**   | Kubernetes (Minikube for local)                          |
| **CI/CD**           | Jenkins, GitHub Webhooks, ArgoCD                         |
| **Infrastructure**  | GCP VM (Ubuntu 20.04, Minikube, Docker, kubectl)        |
| **Version Control** | Git + GitHub                                              |
| **Scripting & Config** | YAML, Bash                                             |

---
## 📊 Data Information

The dataset used for training EffiSense is sourced from the **[Intelligent Manufacturing Process Data](https://www.kaggle.com/datasets)**.

### 🧾 Features Include:
- `Type`: Machine type (categorical)
- `Air temperature [K]`
- `Process temperature [K]`
- `Rotational speed [rpm]`
- `Torque [Nm]`
- `Tool wear [min]`
- `Failure Type`: Encoded into efficiency status (`High`, `Medium`, `Low`)

### 🎯 Target:
- `Efficiency Label`: Multi-class label derived from machine performance and failure conditions.

> Raw data is stored in: `artifacts/raw/data.csv`

---
## 📦 Installation & Setup

### 🔧 Local Development

```bash
# 1. Clone the repository
git clone https://github.com/aimldinesh/EffiSense.git
cd EffiSense

# 2. (Optional) Create a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run the Flask app
python app.py
# Then open http://localhost:5000 in your browser.
```
---
## 📊 Dataset Information

This dataset provides a comprehensive simulation of data from an intelligent manufacturing environment, encompassing industrial IoT sensor readings, operational modes, 6G network performance metrics, and various production and quality control indicators.

It is designed to support research in areas such as **predictive maintenance**, **quality control**, **resource optimization**, and **real-time anomaly detection** within Industry 4.0 and 6G-enabled smart factories.

---

### 📁 Data Source

This is a simulated dataset representing intelligent manufacturing systems, originally hosted on **Kaggle** (notably by Ziya). It mimics real-world industrial sensor streams and network metrics for research and development use.

---

### 🧾 Feature Overview

Each row represents a real-time snapshot of machine operations and production metrics. Below is a summary of key features:

| Feature                         | Description                                                       | Type        | Unit / Typical Range      |
|---------------------------------|-------------------------------------------------------------------|-------------|---------------------------|
| `Timestamp`                    | Date and time of data recording                                   | Datetime    | `YYYY-MM-DD HH:MM:SS`     |
| `Machine_ID`                   | Unique machine identifier                                         | Integer     | 1–50                      |
| `Operation_Mode`              | Current machine status (`Idle`, `Active`, etc.)                   | Categorical | -                         |

**Industrial IoT Sensor Data:**

| `Temperature_C`                | Machine temperature                                               | Float       | °C                         |
| `Vibration_Hz`                 | Detected vibration level                                          | Float       | Hz                         |
| `Power_Consumption_kW`         | Electrical power consumption                                      | Float       | kW                         |

**6G Network Performance Metrics:**

| `Network_Latency_ms`           | Delay in data transmission                                        | Float       | ms                         |
| `Packet_Loss_%`                | Lost data packets percentage                                      | Float       | %                          |

**Production & Quality Indicators:**

| `Quality_Control_Defect_Rate_%`| Product defect rate                                               | Float       | %                          |
| `Production_Speed_units_per_hr`| Production speed                                                  | Float       | units/hour                 |
| `Predictive_Maintenance_Score` | Maintenance urgency score                                         | Float       | 0–1                        |
| `Error_Rate_%`                 | General production error rate                                     | Float       | %                          |

**🔚 Target Variable:**

| `Efficiency_Status`            | Efficiency label (`High`, `Medium`, `Low`) — **Target for ML**    | Categorical | -                         |

---

### 🔍 Potential Use Cases

- **Predictive Maintenance** — Forecasting when machines need servicing
- **Real-time Anomaly Detection** — Spotting operational faults instantly
- **Quality Control** — Reducing defective product output
- **Performance Optimization** — Boosting machine speed or energy efficiency
- **Network Impact Analysis** — Studying how latency affects production
- **Root Cause Analysis** — Tracing inefficiencies back to their source
- **6G-Aware Applications** — Designing future-proof, real-time control systems

---

### 🙏 Acknowledgements

This dataset is a simulated representation designed for research.  
Please acknowledge the original creator (**Ziya on Kaggle**) if used in publications or production.

> 🔗 [Kaggle Dataset Link ](https://www.kaggle.com/datasets/ziya07/intelligent-manufacturing-dataset)

---
## 🤖 Model Details

EffiSense applies a supervised ML model to classify machine efficiency as **High**, **Medium**, or **Low** using preprocessed industrial data.

### 🧠 Problem Type
- Multiclass Classification

### 🧮 ML Pipeline Overview

1. **Data Preprocessing**
   - Encode categorical features
   - Scale numeric features using `StandardScaler`
   - Split dataset into training and test sets (80/20)

2. **Model Training**
   - Algorithm: **Logistic Regression** (scikit-learn)
   - Input: Preprocessed `X_train` and `y_train`
   - Output: `model.pkl` (final trained model)

3. **Model Evaluation**
   - Evaluated on `X_test`, `y_test`
   - Metrics: Accuracy, Precision, Recall, F1-score
   - Results saved to `evaluation_metrics.csv`

### 📁 Model Artifacts
```
artifacts/
├── raw/
│ └── data.csv # Original dataset
├── processed/
│ ├── X_train.pkl # Processed training features
│ ├── X_test.pkl # Processed testing features
│ ├── y_train.pkl # Training labels
│ ├── y_test.pkl # Testing labels
│ └── scaler.pkl # StandardScaler object
├── models/
│ ├── model.pkl # Trained Logistic Regression model
│ └── evaluation_metrics.csv # Model evaluation metrics (CSV)

```
---

## 🚀 CI/CD Pipeline

EffiSense uses a robust CI/CD pipeline to automate the build, test, and deployment process using **Jenkins** and **ArgoCD**.

The pipeline is divided into three major phases as shown in the MLOps workflow:

---

### ⚙️ 1. Development & Experimentation

- **Project Setup**: Organize codebase and folder structure
- **Notebook Testing**: Validate logic using Jupyter notebooks
- **Data Processing**: Handle preprocessing, encoding, scaling
- **Model Training**: Train and evaluate ML model

---

### 📦 2. Packaging & Infrastructure

- **User App Building**: Develop Flask app for prediction
- **Dockerfile & K8s Manifests**: Create deployment-ready infrastructure files
- **Data & Code Versioning**: Store models and preprocessing artifacts in versioned directories
- **VM Instance Setup**: Use GCP VM with Minikube to simulate production environment

---

### 🔄 3. CI/CD Pipeline Automation

- **Jenkins Setup**: Jenkins is installed and configured on the VM
- **GitHub ↔ Jenkins Integration**: GitHub Webhooks trigger Jenkins on every push
- **CI Pipeline**: Jenkins runs `Jenkinsfile` to build Docker image and run tests
- **ArgoCD Setup**: ArgoCD is installed on the cluster for GitOps-based deployment
- **CD Code & Automation**: ArgoCD monitors Git repo for Kubernetes manifest changes
- **Production Deployment**: New app version is automatically deployed to K8s via ArgoCD
  
> ✅ This setup ensures that **every code push** is automatically tested, containerized, and deployed to the cluster within seconds — achieving true MLOps automation.
---
## 📌 Future Improvements

Here are a few planned enhancements and stretch goals to take EffiSense to the next level:

- 🔍 **Monitoring Integration**: Add Prometheus + Grafana for real-time app and model monitoring
- 📈 **Model Experiment Tracking**: Integrate MLflow or DVC to track model performance and metadata
- 🧪 **AutoML Pipeline**: Extend model training to support multiple algorithms + hyperparameter tuning
- 📊 **Analytics Dashboard**: Build a Streamlit-based dashboard to visualize efficiency trends
- 🔐 **Authentication**: Add user login and access control to the web interface
- ☁️ **Cloud-Native Deployment**: Move from local Minikube to managed GKE/EKS cluster

---
## 🙌 Author

**Dinesh Kumar**  
- 🧑‍💻 [GitHub](https://github.com/aimldinesh)  
- 📝 [Medium](https://medium.com/@aimldinesh) 
- 📫 Email: 

> If you found this project useful or learned something from it, feel free to ⭐ the repo and connect!

---

## 🤝 Contributing

Contributions, issues, and feature requests are welcome!  

