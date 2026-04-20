# 🚀 SwiftDocs (WIP)
**A Multi-tenant Document Management System (DMS)**

SwiftDocs is a high-performance, scalable document management platform designed to handle secure file storage and organization across multiple isolated tenants. 

> **Note:** This project is currently a **Work In Progress**. Core architecture for multi-tenancy and database migrations is implemented, with storage currently handled via a local SeaweedFS instance.

---

## 🏗️ Architecture & Core Features

* **Multi-Tenancy:** Engineered with a tenant-isolation strategy to ensure data security and privacy between different organizations.
* **Automated Migrations:** Utilizes **Alembic** for robust database version control, supporting complex schema updates for both public and tenant-specific scopes.
* **Asynchronous Backend:** Built with **FastAPI** for high-concurrency performance and automated OpenAPI (Swagger) documentation.
* **Hybrid Storage Strategy:** Currently utilizing **SeaweedFS** for local development to simulate high-performance distributed storage. Designed with an S3-compatible API layer to allow seamless transition to **AWS S3** for production.
* **Type-Safe Frontend:** A modern **React + TypeScript** interface using Vite for rapid development and strict type checking.

---

## 🛠️ Technical Stack

### **Backend**
* **Framework:** FastAPI (Python)
* **ORM:** SQLAlchemy
* **Migrations:** Alembic
* **Storage:** SeaweedFS (Local S3-compatible) / AWS S3 (Planned)
* **Database:** PostgreSQL (Multi-tenant schema support)

### **Frontend**
* **Framework:** React 18
* **Language:** TypeScript
* **Build Tool:** Vite

---

## 📂 Project Structure

```text
SwiftDocs/
├── backendFiles/
│   ├── migrations-public/   # Shared system migrations
│   ├── migrations-tenant/   # Individual tenant migrations
│   ├── src/                 # FastAPI routes, schemas, and models
│   └── alembic.ini
├── frontendFiles/           # React + TypeScript source
├── ProjectDetails/          # Architecture diagrams (.drawio)
└── .env.example             # Template for DB/S3/SeaweedFS credentials