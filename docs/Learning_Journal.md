# AI-Powered Supply Chain Copilot
## Learning Journal

---

# Module 1 – Backend Foundation

## What I learned

### FastAPI
- FastAPI is the backend framework used to build REST APIs.
- It receives HTTP requests and returns JSON responses.
- FastAPI automatically generates Swagger documentation.

---

### Layered Architecture

Our backend follows:

Browser
↓

API
↓

Service
↓

Repository
↓

Database

Each layer has a single responsibility.

---

### Separation of Concerns

Every component should perform only one job.

API:
Receives HTTP requests.

Service:
Contains business logic.

Repository:
Reads data.

Database:
Stores data.

---

### ERP Simulation

Instead of downloading public datasets, we built a simulated ERP system.

Tables include:

- Products
- Inventory
- Suppliers
- Purchase Orders
- Sales Orders
- Forecast
- Shipments
- Returns
- Supplier Performance

---

### Inventory Module

The Inventory Service identifies products below safety stock.

Formula:

Available Stock < Safety Stock

If true,

Inventory Status = Low Stock

---

## Interview Notes

Q: Why use Service Layer?

A:

The Service Layer separates business logic from request handling. This makes the application easier to maintain, test, and extend.

---

Q: Why simulate ERP data?

A:

Real ERP data is confidential. I created a realistic ERP simulation to model enterprise supply chain processes without exposing proprietary business data.

---

Q: Why use FastAPI?

A:

FastAPI provides high performance, automatic API documentation, type validation using Pydantic, and is well suited for AI and microservice applications.

---

## Git History

✔ Initial Setup

✔ Project Documentation

✔ ERP Data Generator

✔ Business Scenario Generator

✔ Inventory API

✔ Service Layer