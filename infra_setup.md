# 🔧 Infrastructure Setup Guide for EffiSense

This guide outlines the complete infrastructure setup used to build, deploy, and run the **EffiSense** MLOps project. It includes:

* Dockerfile and Kubernetes manifests
* GCP VM instance setup
* Docker, Minikube, kubectl installation
* Jenkins and ArgoCD configuration
* GitHub Webhooks for automation

---

## 🐳 Dockerfile

```Dockerfile
FROM python:3.10
WORKDIR /app
COPY . /app
RUN pip install --no-cache-dir -e .
EXPOSE 5000
ENV FLASK_APP=app.py
CMD ["python", "app.py"]
```

---

## ☸️ Kubernetes Manifests

### `./manifests/deployment.yml`

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: mlops-app
spec:
  replicas: 2
  selector:
    matchLabels:
      app: mlops-app
  template:
    metadata:
      labels:
        app: mlops-app
    spec:
      containers:
      - name: mlops-app
        image: dkc12345/gitops-project:latest
        ports:
        - containerPort: 5000
```

### `./manifests/service.yml`

```yaml
apiVersion: v1
kind: Service
metadata:
  name: my-service
spec:
  selector:
    app: mlops-app
  ports:
    - port: 80
      targetPort: 5000
  type: NodePort
```

---

## ☁️ GCP VM Setup & Configuration

### 🧱 VM Configuration

* **Machine Type**: e2-standard-4 (4 vCPU, 16 GB)
* **OS**: Ubuntu 20.04 LTS
* **Disk**: 128 GB

### 🔧 Commands

```bash
# Clone repo
git clone https://github.com/aimldinesh/EffiSense.git
cd EffiSense
ls
```

---

## 🐳 Install Docker

Follow official guide: [Docker on Ubuntu](https://docs.docker.com/engine/install/ubuntu/)

### Commands Summary

```bash
sudo apt-get update
sudo apt-get install ca-certificates curl
...
sudo docker run hello-world
```

To run docker without sudo:

```bash
sudo groupadd docker
sudo usermod -aG docker $USER
newgrp docker
docker run hello-world
```

---

## 🚀 Install Minikube

[Minikube Docs](https://minikube.sigs.k8s.io/docs/start/)

```bash
curl -LO https://github.com/kubernetes/minikube/releases/latest/download/minikube-linux-amd64
sudo install minikube-linux-amd64 /usr/local/bin/minikube
minikube start
```

## 🔧 Install kubectl

```bash
sudo snap install kubectl --classic
kubectl version --client
```

---

## 🔧 Jenkins Installation (Dockerized)

```bash
docker run -d --name jenkins \
  -p 8080:8080 -p 50000:50000 \
  -v /var/run/docker.sock:/var/run/docker.sock \
  -v $(which docker):/usr/bin/docker \
  -u root \
  -e DOCKER_GID=$(getent group docker | cut -d: -f3) \
  --network minikube \
  jenkins/jenkins:lts
```

### Setup Jenkins

* Visit `http://<EXTERNAL-IP>:8080`
* Install suggested plugins: Docker, Docker Pipeline, Kubernetes
* Create admin user
* Install Python inside Jenkins container:

```bash
docker exec -it jenkins bash
apt update && apt install -y python3 python3-pip python3-venv
```

---

## 🔁 GitHub Integration with Jenkins

* Create GitHub **Personal Access Token**
* Add credentials in Jenkins: `Manage Jenkins > Credentials > Global`
* Create new pipeline: `Pipeline from SCM > Git`
* Setup repository and credentials

### Sample `Jenkinsfile`

```groovy
pipeline {
    agent any
    stages {
        stage('Checkout Github') {
            steps {
                checkout scm
            }
        }
        stage('Build Docker Image') {
            steps {
                echo 'Build logic here'
            }
        }
        stage('Push Docker Image') {
            steps {
                echo 'Push logic here'
            }
        }
    }
}
```

---

## 🚀 ArgoCD Setup

```bash
kubectl create ns argocd
kubectl apply -n argocd -f https://raw.githubusercontent.com/argoproj/argo-cd/stable/manifests/install.yaml
kubectl get svc -n argocd
kubectl edit svc argocd-server -n argocd  # Change type to NodePort
kubectl port-forward svc/argocd-server -n argocd 30315:80
```

### Login to ArgoCD

```bash
# Get admin password
kubectl get secret -n argocd argocd-initial-admin-secret -o jsonpath="{.data.password}" | base64 -d
```

* Open `http://<EXTERNAL-IP>:30315`
* Username: `admin`, Password: (output from above)

### Connect ArgoCD to GitHub

* Go to `Settings > Repositories > Connect Repo via HTTPS`
* Provide repo URL and GitHub credentials (PAT)

### Create Application

* Go to `Applications > New Application`
* Source: GitHub repo, Path: `manifests/`, Branch: `main`
* Destination: in-cluster, Namespace: `argocd`

---

## 🔁 GitHub Webhooks

* GitHub Repo > Settings > Webhooks > Add Webhook
* Payload URL: `http://<EXTERNAL-IP>:8080/github-webhook/`
* Content type: `application/json`

Jenkins: `Configure > GitHub hook trigger for GITScm polling`

---

## ✅ Final App Deployment

```bash
# Forward app port (e.g., for port 80 to 9090)
kubectl port-forward svc/my-service -n argocd --address 0.0.0.0 9090:80
```

Now open: `http://<EXTERNAL-IP>:9090` to use your app!

---

For any issues, check `kubectl get pods`, `docker ps`, `jenkins logs`, or `argocd dashboard`.
