# AI-Powered Supply Chain Copilot

I built this project to explore how Generative AI can be used alongside traditional supply chain analytics.

In most supply chain environments, operational data lives in systems and databases, while information such as supplier terms, procurement policies, and SOPs lives in separate documents. I wanted to build one application where a user could ask a supply chain question in plain English and get an answer using either operational data, business documents, or both.

The application currently covers inventory, supplier performance, procurement, demand forecasting, logistics, warehouse capacity, and document-based questions.

## What the application does

The project has two main parts.

The first is a supply chain dashboard that gives an overview of KPIs such as low-stock products, supplier delays, open purchase orders, shipment status, warehouse utilization, and forecast accuracy.

The second is the AI Copilot. A user can ask questions such as:

- Which supplier has the highest delay rate?
- Which products have the highest forecasted demand?
- What are the delivery requirements in the Apex Packaging supplier contract?
- Which supplier has the highest delay rate, and based on its contract and our procurement policy, what action should we take?

Depending on the question, the backend can query BigQuery, retrieve information from documents through RAG, or use multiple agents together.

## Application

### Supply Chain Control Tower

This is the main dashboard I built to bring the major supply chain KPIs into one view.

![Executive Overview](docs/screenshots/1-Executive%20Overview.png)

The operational analytics section shows supplier delay rates, inventory status, and purchase-order trends.

![Operational Analytics](docs/screenshots/2-Dashboard(1).png)

I also added warehouse utilization, shipment status, forecast accuracy, and recommended actions.

![Dashboard Analytics](docs/screenshots/3-Dashboard(2).png)

## AI Copilot

The Copilot sits on top of the supply chain data and lets the user work with it through natural-language questions.

For structured questions, the application generates SQL, validates it, queries BigQuery, and returns the result in a business-friendly format.

### Supplier analysis

For example, I can ask which supplier currently has the highest delay rate.

![Supplier Analysis](docs/screenshots/4-Example%20Questions.png)

### Demand forecasting

The Copilot can also work with forecast data and identify products with the highest forecasted demand.

![Demand Forecasting](docs/screenshots/5-Example%20Questions.png)

### Supplier contracts and policies

I also wanted the application to work with information that normally would not be stored in a database.

I created sample supplier contracts, procurement policies, and SOPs and built a RAG pipeline using Gemini embeddings and Vertex AI Vector Search.

This allows questions such as:

> What are the delivery requirements in the Apex Packaging supplier contract?

![Contract Retrieval](docs/screenshots/6-Example%20Questions.png)

### Combining data and documents

One of the main workflows I wanted to test was whether the application could combine an operational issue with the relevant business documents.

For example:

> Which supplier has the highest delay rate, and based on its contract and our procurement policy, what action should we take?

For this question, the system first identifies the supplier from the operational data and then uses the relevant contract and procurement-policy information to provide the next actions.

![Multi-Agent Analysis](docs/screenshots/7-Example%20Questions.png)

## How I built it

The frontend is built with React and Vite, and the backend is built with FastAPI.

I used BigQuery as the structured data layer. Gemini is used for the GenAI parts of the application, while Vertex AI Vector Search supports document retrieval.

For orchestration, I used LangGraph with separate agents for inventory, suppliers, demand forecasting, procurement, and document retrieval. The supervisor routes the question to the appropriate workflow and can use more than one agent when a question requires both structured data and document context.

The application is containerized with Docker and the frontend and backend are deployed separately on Google Cloud Run.

## Architecture

```text
                         React Dashboard
                                |
                                v
                         FastAPI Backend
                                |
                                v
                      LangGraph Supervisor
                                |
       +------------+-----------+-----------+------------+
       |            |           |           |            |
       v            v           v           v            v
   Inventory     Supplier     Demand    Procurement    Document
     Agent        Agent      Forecast      Agent       Retrieval
                              Agent                     Agent
       |            |           |           |            |
       +------------+-----------+-----------+            |
                    |                                    |
                    v                                    v
                 BigQuery                      Vertex AI Vector Search
                                                         |
                                                         v
                                                       Gemini
```

## Tech stack

**Backend:** Python, FastAPI, Pydantic  
**Frontend:** React, Vite, JavaScript  
**Data:** Google BigQuery, SQL  
**AI:** Gemini, Vertex AI, LangGraph, LangChain  
**RAG:** Gemini Embeddings, Vertex AI Vector Search  
**Deployment:** Docker, Google Cloud Run

## Project structure

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
│   ├── Dockerfile
│   └── requirements.txt
│
├── frontend/
│   ├── src/
│   ├── Dockerfile
│   └── package.json
│
├── documents/
├── docs/
│   └── screenshots/
├── scripts/
├── tests/
├── .env.example
└── README.md
```

## Running locally

Clone the repository and create a `.env` file using `.env.example` as the reference.

For the backend:

```bash
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload
```

For the frontend:

```bash
cd frontend
npm install
npm run dev
```

The Google Cloud and Vertex AI resources also need to be configured for BigQuery and RAG functionality.

## About the data

I built this project independently as a portfolio and learning project.

All supplier names, inventory records, purchase orders, forecasts, shipments, contracts, policies, SOPs, and other business data used in the application are synthetic/sample data created for the project.

No confidential, proprietary, personal, or internal company data is used in this repository.