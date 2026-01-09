# System Management Platform (RBAC + Docker + Local Setup + Kubernetes/Minikube)

> 🇹🇷 **Kısa Türkçe özet:** Bu repo, aynı platformun hem **Docker Compose** ile container tabanlı kurulumu hem de **lokal kurulum** (PostgreSQL + servisler host üzerinde) senaryosunu içerir. Ayrıca **RBAC**, **log yönetimi**, ve **Kubernetes (Minikube)** deployment denemeleri bulunmaktadır.

A system management platform designed with **Role-Based Access Control (RBAC)** where users have different permissions (add, edit, delete, view).
This repository includes **two setup approaches** to demonstrate both containerized and local deployments.

---

## 🚀 Features

- ✅ User login system
- ✅ Role-Based Access Control (RBAC)
  - Admin
  - Adder (add-only)
  - Editor (edit-only)
  - Deleter (delete-only)
  - Viewer (read-only)
- ✅ PostgreSQL database
- ✅ Docker Compose setup (containerized deployment)
- ✅ Local installation setup (manual/host deployment)
- ✅ Kubernetes manifests included (`ymlconfig/`)
- ✅ Logs mounted on host machine for persistent log storage
- ✅ Operational tooling experience:
  - pgAdmin4 (DB administration)
  - Portainer (container management)

---

## 🛠 Tech Stack

- **Backend:** Python (Flask)
- **Database:** PostgreSQL
- **Containerization:** Docker / Docker Compose
- **Kubernetes:** YAML manifests (tested with **Minikube**)
- **Operational tools:** pgAdmin4, Portainer

---

## 📦 Repository Structure

```bash
.
├── app/                     # Dockerized Flask application (Project 1)
│   ├── templates/           # HTML templates (login + index)
│   ├── app.py               # Flask entrypoint
│   └── Dockerfile           # App Dockerfile
├── docker-compose.yml       # Docker Compose setup (web + postgres)
├── postgres/
│   └── init-users.sql       # Seed users + roles (Docker version)
├── project-2-local/         # Project 2 (Local installation + RBAC + services on host)
├── ymlconfig/               # Kubernetes manifests
│   ├── flask-deployment.yaml
│   └── postgres-deployment.yaml
├── requirements.txt
└── *.py                     # DB utility scripts (CRUD)




1) Run with Docker Compose (Project 1 - Containerized Setup)
✅ Requirements

- Docker

- Docker Compose

Verify:

docker --version
docker compose version

▶️ Start the system

From the repository root:

docker-compose up --build


Services:

- Flask Web UI: http://localhost:5000

- PostgreSQL: localhost:5432

🧾 Persistent logs

Logs are mounted to the host machine:

- Host path: ~/project_app_logs

- Container path: /logs

👤 Demo Credentials (Docker Setup)

These are demo accounts for testing RBAC behavior.

- Admin: admin / admin123

- Adder: adder / adder123

- Editor: editor / editor123

- Deleter: deleter / deleter123

- Viewer: viewer / viewer123

Users/roles are seeded via: postgres/init-users.sql

2) Local Setup (Project 2 - Host Installation)

This setup demonstrates running the same platform without Docker, by installing and running required services on the host environment (WSL/Linux).

✅ Requirements

- Python 3.x

- PostgreSQL installed locally

- pip / venv

▶️ Install
cd project-2-local
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

▶️ Run
python3 app.py


If Project 2 requires a running PostgreSQL service, make sure DB connection settings are configured (e.g., environment variables or config file).

👤 Demo Credentials (Local Setup)

If your local version uses different demo users, list them here (recommended).

- Example:

- local_admin / local_admin123

- local_viewer / local_viewer123

3) Kubernetes Deployment (Tested with Minikube)

Kubernetes manifests are available in ymlconfig/.
This deployment was tested locally using Minikube.

✅ Requirements

- Minikube

- kubectl

▶️ Start Minikube
minikube start

▶️ Apply manifests
kubectl apply -f ymlconfig/
kubectl get pods


If you are using a Service/Ingress, you can expose the service using:

minikube service <service-name>

📌 Notes

- Secrets and local config files are excluded via .gitignore (e.g., .env)

- PostgreSQL runtime data should not be committed (e.g., postgres/data/)

- If you want to improve security, move DB credentials into .env and reference them in docker-compose.yml

✅ Future Improvements (Optional)

- Add CI pipeline (GitHub Actions) for lint + build

- Add unit tests and coverage

- Add a dedicated monitoring/ directory for Prometheus + Grafana configs

- Provide API documentation (Swagger/OpenAPI)

📷 Screenshots (Recommended)

Add screenshots for:

- Login page

- RBAC permission behavior (e.g., Viewer cannot delete)

- Docker services running (docker ps)

- Optional: Grafana dashboard (if monitoring is available)
