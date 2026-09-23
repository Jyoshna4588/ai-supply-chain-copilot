# 🚀 AI-Powered Supply Chain Copilot

An end-to-end **AI-powered supply chain decision-support application** that combines structured operational data, natural-language analytics, Retrieval-Augmented Generation (RAG), and multi-agent AI workflows.

The application enables supply chain professionals to monitor operational KPIs and ask natural-language questions across **inventory, supplier performance, procurement, demand forecasting, logistics, warehouse capacity, and business documents**.

The project demonstrates how **Supply Chain + Data Analytics + Generative AI** can be integrated into a practical decision-support system.

---

## 📸 Application Preview

### Executive Supply Chain Control Tower

The dashboard provides a centralized operational view of inventory, suppliers, purchasing, logistics, warehouse operations, and demand planning.

![Executive Overview](docs/screenshots/1-Executive%20Overview.png)

### Operational Analytics

Supplier risk, inventory health, and procurement trends are monitored through interactive analytics.

![Operational Analytics](docs/screenshots/2-Dashboard(1).png)

Warehouse utilization, shipment status, forecast accuracy, and recommended operational actions provide additional decision-support capabilities.

![Supply Chain Analytics](docs/screenshots/3-Dashboard(2).png)

---

## 🤖 AI Supply Chain Copilot

The AI Copilot allows users to interact with supply chain data and documents using natural language.

Depending on the question, the system can analyze structured BigQuery data, retrieve relevant business documents, or coordinate multiple AI agents to generate a contextual response.

### Supplier Performance Analysis

The Copilot can analyze supplier performance metrics and identify suppliers requiring attention.

Example:

> **Which supplier has the highest delay rate?**

The system queries operational data and identifies the supplier with the highest recorded delay percentage.

![Supplier Analysis](docs/screenshots/4-Example%20Questions.png)

### Demand Forecasting Analysis

The Demand Forecasting Agent analyzes forecast data and identifies products with the highest expected demand.

Example:

> **Which products have the highest forecasted demand?**

![Demand Forecasting](docs/screenshots/5-Example%20Questions.png)

### RAG-Based Document Retrieval

The Copilot can retrieve information from unstructured supply chain documents such as supplier contracts, procurement policies, and SOPs.

Example:

> **What are the delivery requirements in the Apex Packaging supplier contract?**

Relevant document chunks are retrieved through **Vertex AI Vector Search** and used by Gemini to generate a grounded response.

![Document Retrieval](docs/screenshots/6-Example%20Questions.png)

### Multi-Agent Decision Support

The system can also combine structured operational analytics with information retrieved from business documents.

Example:

> **Which supplier has the highest delay rate, and based on its contract and our procurement policy, what action should we take?**

For this workflow, the application combines supplier performance data with contract and procurement-policy information to generate recommended actions.

![Multi-Agent Decision Support](docs/screenshots/7-Example%20Questions.png)

---

## ✨ Key Features

- **Natural-Language Supply Chain Analytics**
- **AI-Powered Supply Chain Control Tower**
- **BigQuery-Based Operational Analytics**
- **Multi-Agent AI Orchestration with LangGraph**
- **Retrieval-Augmented Generation (RAG)**
- **Vertex AI Vector Search**
- **Supplier Contract & Policy Retrieval**
- **Inventory and Replenishment Analysis**
- **Supplier Performance Analysis**
- **Demand Forecasting Analysis**
- **Procurement Decision Support**
- **Warehouse Capacity Monitoring**
- **Logistics and Shipment Analytics**
- **Conversation Memory for Follow-Up Questions**
- **Generated SQL Transparency**
- **Containerized Cloud Deployment**

---

## 🧠 Multi-Agent Architecture

The application uses **LangGraph** to orchestrate specialized supply chain AI agents.

```text
                         React Dashboard
                                |
                                v
                         FastAPI Backend
                                |
                                v
                      LangGraph Supervisor
                                |
          +---------------------+---------------------+
          |                     |                     |
          v                     v                     v
   Inventory Agent       Supplier Agent       Procurement Agent
          |                     |                     |
          |              +------+-------+             |
          |              |              |             |
          v              v              v             v
      BigQuery    Demand Forecast   Document Retrieval
                         Agent             Agent
                           |                |
                           v                v
                       BigQuery      Vertex AI Vector Search
                                            |
                                            v
                                          Gemini
```

The supervisor interprets the user's question and coordinates the appropriate specialist workflow.

The specialist agents focus on:

- **Inventory Agent** — inventory levels, stock risk, and replenishment
- **Supplier Agent** — supplier performance, reliability, and delays
- **Demand Forecasting Agent** — forecast demand and forecast performance
- **Procurement Agent** — purchasing and procurement-related analysis
- **Document Retrieval Agent** — contracts, policies, and SOP retrieval

Complex questions can combine structured analytics and document retrieval to provide broader decision support.

---

## 📚 RAG Pipeline

The Retrieval-Augmented Generation pipeline allows the Copilot to answer questions using unstructured supply chain documents.

```text
Supplier Contracts / Procurement Policies / SOPs
                       |
                       v
                Document Ingestion
                       |
                       v
                  Text Chunking
                       |
                       v
               Gemini Embeddings
                       |
                       v
             Vertex AI Vector Search
                       |
                       v
              Relevant Document Chunks
                       |
                       v
                     Gemini
                       |
                       v
                Grounded Response
```

This enables questions involving contractual requirements, procurement procedures, supplier-management policies, and operational SOPs.

---

## 🏗️ System Architecture

```text
User
 |
 v
React / Vite Dashboard
 |
 v
FastAPI REST API
 |
 v
LangGraph Multi-Agent System
 |
 +------------------------+
 |                        |
 v                        v
Structured Data       Unstructured Documents
 |                        |
 v                        v
BigQuery              RAG Pipeline
                          |
                          v
                 Vertex AI Vector Search
                          |
                          v
                        Gemini
 |
 v
AI-Generated Decision Support
```

---

## 🛠️ Technology Stack

### Backend
- Python
- FastAPI
- Pydantic
- Uvicorn

### Generative AI
- Gemini
- Vertex AI
- LangGraph
- LangChain

### Data & Analytics
- Google BigQuery
- SQL
- Python

### RAG
- Gemini Embeddings
- Vertex AI Vector Search
- PDF document ingestion
- Semantic retrieval

### Frontend
- React
- Vite
- JavaScript
- Interactive data visualizations

### Cloud & Deployment
- Google Cloud Platform
- Google Cloud Run
- Docker
- Artifact/Cloud Build workflow

---

## 📊 Supply Chain Domains

The application supports analytics and decision-support workflows across:

- Inventory Management
- Replenishment
- Supplier Performance
- Procurement
- Purchase Orders
- Demand Forecasting
- Logistics
- Shipment Monitoring
- Warehouse Capacity
- Supply Risk
- Supplier Contracts
- Procurement Policies
- Operational SOPs

---

## 💬 Example Questions

Users can ask questions such as:

```text
Which supplier has the highest delay rate?

Which products have the highest forecasted demand?

What are the delivery requirements in the Apex Packaging supplier contract?

What does our procurement policy say about repeated supplier delays?

Which warehouses have the highest utilization?

Which purchase orders are delayed?

Which products require replenishment?

Which supplier has the highest delay rate, and based on its contract
and our procurement policy, what action should we take?
```

---

## 📁 Project Structure

```text
SupplyChainAI/
│
├── backend/
│   ├── app/
│   │   ├── agents/
│   │   ├── api/
│   │   ├── core/
│   │   ├── models/
│   │   ├── repositories/
│   │   ├── services/
│   │   └── main.py
│   │
│   ├── Dockerfile
│   └── requirements.txt
│
├── frontend/
│   ├── src/
│   ├── Dockerfile
│   └── package.json
│
├── documents/
│   └── Synthetic supply chain documents
│
├── docs/
│   └── screenshots/
│
├── scripts/
├── tests/
├── .env.example
├── .gitignore
└── README.md
```

---

## ⚙️ Environment Configuration

Create a `.env` file based on `.env.example`.

Example:

```env
APP_NAME=AI-Powered Supply Chain Copilot
APP_VERSION=1.0.0
ENVIRONMENT=development

DATA_SOURCE=bigquery

GCP_PROJECT_ID=your-gcp-project-id
BIGQUERY_DATASET=your-bigquery-dataset
VERTEX_REGION=us-central1

GEMINI_MODEL=gemini-2.5-flash

RAG_GCS_BUCKET=your-gcs-bucket
RAG_EMBEDDING_MODEL=gemini-embedding-001
RAG_EMBEDDING_DIMENSION=768

RAG_INDEX_ID=your-vector-search-index-id
RAG_INDEX_ENDPOINT_ID=your-vector-search-endpoint-id
RAG_DEPLOYED_INDEX_ID=your-deployed-index-id

RAG_TOP_K=5
RAG_METADATA_PATH=backend/rag_output/metadata.json
```

Do not commit your actual `.env` file or cloud credentials to source control.

---

## ▶️ Running the Backend Locally

Navigate to the backend:

```bash
cd backend
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Start FastAPI:

```bash
uvicorn app.main:app --reload
```

The FastAPI Swagger interface will be available locally through the `/docs` endpoint.

---

## 💻 Running the Frontend Locally

Navigate to the frontend:

```bash
cd frontend
```

Install dependencies:

```bash
npm install
```

Start the Vite development server:

```bash
npm run dev
```

---

## ☁️ Cloud Deployment

The application is containerized using **Docker** and deployed using **Google Cloud Run**.

Separate Cloud Run services are used for the frontend and backend, allowing the React application to communicate with the FastAPI API through HTTPS.

The backend integrates with:

- Google BigQuery
- Vertex AI
- Gemini
- Vertex AI Vector Search

---

## 🔐 Security

Sensitive configuration is excluded from the repository using `.gitignore`.

The repository does not intentionally include:

- `.env` files
- Service-account credentials
- Google Cloud authentication files
- Local virtual environments
- `node_modules`
- Generated vector-search artifacts

An `.env.example` file is provided to document the required configuration without exposing credentials or project-specific secrets.

---

## 🧪 Data Disclaimer

**This project was developed independently for learning and portfolio purposes.**

All data, supplier names and information, contracts, procurement policies, SOPs, operational metrics, forecasts, purchase orders, inventory records, shipments, and business scenarios used in this project are **synthetic/sample data created specifically for demonstration purposes**.

**No confidential, proprietary, personal, or internal data from any company or organization was used.**

---

## 🎯 Project Purpose

This project demonstrates the integration of:

**Supply Chain Management + Data Analytics + Generative AI + Cloud Engineering**

The objective is to show how modern AI technologies can complement traditional supply chain analytics by allowing users to interact with both structured operational data and unstructured business documents through a conversational decision-support interface.