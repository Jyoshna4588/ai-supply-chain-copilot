# Project Architecture

## High-Level Architecture

User
↓
React Frontend
↓
FastAPI Backend
↓
LangGraph Supervisor Agent
↓
Specialized Agents:
- Inventory Agent
- Supplier Agent
- Forecast Agent
- Document Retrieval Agent
↓
Structured Data:
- BigQuery
↓
Unstructured Documents:
- Cloud Storage
- Vertex AI Embeddings
- Vertex AI Vector Search
↓
LLM:
- Google Gemini
↓
Response to User

## Technology Stack

### Frontend
- React
- TypeScript

### Backend
- Python
- FastAPI
- Uvicorn

### Data
- CSV files for local development
- BigQuery for cloud data warehouse

### AI
- Google Gemini
- Vertex AI
- Vertex AI Embeddings
- Vertex AI Vector Search
- LangChain
- LangGraph
- RAG

### Deployment
- Docker
- Cloud Run
- Cloud Build
- Artifact Registry

## Design Decision
This project uses simulated ERP data because real ERP systems such as SAP and Oracle contain confidential enterprise data. The simulated ERP tables represent common supply chain entities including inventory, suppliers, purchase orders, forecasts, warehouses, shipments, and returns.