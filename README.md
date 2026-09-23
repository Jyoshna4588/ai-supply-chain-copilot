\# 🚀 AI-Powered Supply Chain Copilot



An end-to-end AI-powered decision-support application for supply chain operations that combines structured ERP-style data with unstructured business documents through a conversational interface.



The application enables users to ask natural-language questions about inventory, supplier performance, demand forecasting, procurement, purchase orders, supplier contracts, SOPs, and policies.



\---



\## 📌 Project Overview



Supply chain professionals often need to work across multiple systems, dashboards, spreadsheets, supplier contracts, SOPs, and procurement policies to make operational decisions.



The AI-Powered Supply Chain Copilot brings these information sources together into a single conversational application.



For example, a user can ask:



> "Which supplier has the highest delay rate, and based on its contract and our procurement policy, what action should we take?"



The application can analyze structured supply chain data in BigQuery, retrieve relevant information from business documents using RAG and Vector Search, and use Gemini to generate a contextual response.



\---



\## ✨ Key Features



\- Natural-language supply chain analytics

\- Inventory analysis and replenishment insights

\- Supplier performance analysis

\- Demand forecasting analysis

\- Procurement and purchase-order analysis

\- Supplier contract retrieval

\- Procurement policy and SOP retrieval

\- Retrieval-Augmented Generation (RAG)

\- Vertex AI Vector Search

\- Multi-agent orchestration using LangGraph

\- Contextual conversation memory

\- Interactive React dashboard

\- FastAPI backend

\- Containerized deployment with Docker

\- Cloud deployment using Google Cloud Run



\---



\## 🤖 Multi-Agent Architecture



The application uses a supervisor-based multi-agent architecture to route supply chain questions to specialized workflows.



Specialized capabilities include:



\- Inventory Agent

\- Supplier Agent

\- Demand Forecasting Agent

\- Procurement Agent

\- Document Retrieval Agent



The supervisor coordinates these capabilities depending on the user's question and can combine structured analytics with document retrieval when necessary.



\---



\## 🧠 RAG Pipeline



The Retrieval-Augmented Generation pipeline enables the Copilot to answer questions using unstructured supply chain documents such as:



\- Supplier contracts

\- Procurement policies

\- Inventory management SOPs

\- Supplier management policies

\- Warehouse operations SOPs



Documents are processed into chunks, converted into embeddings, and retrieved using Vertex AI Vector Search.



Relevant document context is then combined with the user's question to generate grounded responses.



\---


## 🏗️ Architecture

```text
                    React Dashboard
                           |
                           v
                    FastAPI Backend
                           |
                           v
                  LangGraph Supervisor
                           |
        +------------------+------------------+
        |                  |                  |
        v                  v                  v
 Inventory Agent     Supplier Agent     Procurement Agent
        |                  |                  |
        +------------------+------------------+
                           |
              +------------+------------+
              |                         |
              v                         v
           BigQuery             Document Retrieval
                                        |
                                        v
                              Vertex AI Vector Search
                                        |
                                        v
                                     Gemini
```

The architecture supports both structured-data analytics and retrieval from unstructured supply chain documents.
```



The architecture supports both structured-data analytics and retrieval from unstructured supply chain documents.



\---



\## 🛠️ Technology Stack



\### AI / Generative AI

\- Google Gemini

\- Vertex AI

\- Vertex AI Vector Search

\- LangGraph

\- LangChain

\- Retrieval-Augmented Generation (RAG)



\### Backend

\- Python

\- FastAPI

\- Pydantic

\- Uvicorn



\### Data \& Analytics

\- Google BigQuery

\- SQL

\- Synthetic ERP-style supply chain datasets



\### Frontend

\- React

\- Vite

\- Recharts



\### Cloud \& Deployment

\- Google Cloud Platform

\- Google Cloud Run

\- Docker

\- Nginx



\---



\## 📊 Supply Chain Domains



The Copilot supports analytics and decision support across areas including:



\- Inventory Management

\- Supplier Performance

\- Demand Forecasting

\- Procurement

\- Purchase Orders

\- Replenishment

\- Supplier Risk

\- Warehouse Operations

\- Supply Chain Policies

\- Supplier Contracts



\---



\## 💬 Example Questions



```text

Which supplier has the highest delay rate?



Which products currently have the highest inventory risk?



Which products have the highest forecasted demand?



Which purchase orders require procurement attention?



What are the delivery requirements in the Apex Packaging supplier contract?



According to our procurement policy, what actions should be taken when a supplier has repeated delivery delays?



Which supplier has the highest delay rate, and based on its contract and our procurement policy, what action should we take?

```



The application also supports contextual follow-up questions using conversation memory.



Example:



```text

User: Which supplier has the highest delay rate?



User: What does their contract say about late deliveries?



User: Based on our procurement policy, what should we do next?

```



\---



\## 📁 Project Structure



```text

SupplyChainAI/

|

├── backend/

│   ├── app/

│   │   ├── ai/

│   │   ├── api/

│   │   ├── config/

│   │   ├── core/

│   │   ├── graph/

│   │   ├── langchain/

│   │   ├── models/

│   │   ├── repositories/

│   │   ├── schemas/

│   │   └── services/

│   ├── Dockerfile

│   └── requirements.txt

|

├── frontend/

│   ├── src/

│   ├── Dockerfile

│   ├── nginx.conf

│   └── package.json

|

├── data/

├── documents/

├── deployment/

├── docs/

├── notebooks/

├── scripts/

├── tests/

├── .env.example

├── .gitignore

└── README.md

```



\---



\## ⚙️ Environment Configuration



Create a `.env` file based on the provided `.env.example`.



Example:



```env

GCP\_PROJECT\_ID=your-gcp-project-id

BIGQUERY\_DATASET=your-bigquery-dataset

VERTEX\_REGION=us-central1

GEMINI\_MODEL=gemini-2.5-flash



RAG\_GCS\_BUCKET=your-gcs-bucket

RAG\_INDEX\_ID=your-vector-search-index-id

RAG\_INDEX\_ENDPOINT\_ID=your-vector-search-endpoint-id

RAG\_DEPLOYED\_INDEX\_ID=your-deployed-index-id

```



Do not commit your real `.env` file or Google Cloud credentials to source control.



\---



\## ▶️ Running the Backend Locally



Create and activate a Python virtual environment and install the required dependencies.



```bash

pip install -r backend/requirements.txt

```



Start the FastAPI application:



```bash

uvicorn app.main:app --reload

```



\---



\## ▶️ Running the Frontend Locally



Navigate to the frontend directory:



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



\---



\## ☁️ Deployment



The application architecture supports containerized deployment to Google Cloud Run.



The backend and frontend are deployed as separate Cloud Run services.



\- Backend: FastAPI container

\- Frontend: React/Vite application served through Nginx

\- Structured analytics: BigQuery

\- Generative AI: Gemini / Vertex AI

\- Document retrieval: Vertex AI Vector Search



\---



\## 🔐 Security



Sensitive configuration is excluded from source control using `.gitignore`.



Files such as the following should never be committed:



```text

.env

Google Cloud credentials

Service-account keys

Local virtual environments

node\_modules

```



\---



\## ⚠️ Data Disclaimer



This project was developed independently for learning and portfolio purposes.



All data, supplier information, contracts, policies, operational metrics, and business scenarios used in this application are synthetic/sample data created specifically for demonstration purposes.



No confidential, proprietary, personal, or internal data from any company or organization was used.



\---



\## 🎯 Project Purpose



This project demonstrates how Generative AI, data analytics, cloud technologies, and supply chain domain knowledge can be combined to build an end-to-end AI decision-support application.



The project covers the complete workflow from structured-data analytics and document retrieval to multi-agent orchestration, conversational AI, frontend development, containerization, and cloud deployment.

