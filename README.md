# System Management Platform (RBAC + Docker + Kubernetes)

A system management platform designed with **Role-Based Access Control (RBAC)** where users have different permissions (add, edit, delete, view).
The project is containerized with **Docker Compose**, uses **PostgreSQL** as database, and includes Kubernetes manifests for deployment.

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
- ✅ Docker Compose ready setup
- ✅ Kubernetes manifests included (`ymlconfig/`)
- ✅ Logs mounted on host machine for persistent log storage

---

## 🛠 Tech Stack

- **Backend:** Python (Flask)
- **Database:** PostgreSQL
- **Containerization:** Docker / Docker Compose
- **Kubernetes:** Deployment YAML manifests
- **Operational tools used:**
  - pgAdmin4 (DB administration)
  - Portainer (container management)

---

## 📦 Project Structure

```bash
.
├── app/                     # Flask application
│   ├── templates/           # HTML templates (login + index)
│   ├── app.py               # Flask entrypoint
│   └── Dockerfile           # App Dockerfile
├── docker-compose.yml       # Docker Compose setup (web + postgres)
├── postgres/
│   └── init-users.sql       # User + role setup script
├── ymlconfig/               # Kubernetes manifests
│   ├── flask-deployment.yaml
│   └── postgres-deployment.yaml
├── requirements.txt
└── *.py                     # DB utility scripts (CRUD)
