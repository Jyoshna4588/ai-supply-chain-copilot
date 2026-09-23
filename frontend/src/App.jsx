import { useEffect, useState } from "react";

import ChatWindow from "./components/ChatWindow";
import Dashboard from "./components/Dashboard";
import QuestionInput from "./components/QuestionInput";

import {
  fetchDashboardSummary,
  submitAIQuestion,
} from "./services/api";

import "./App.css";


const EMPTY_DASHBOARD = {
  low_stock_products: 0,
  total_suppliers: 0,
  delayed_purchase_orders: 0,
  open_purchase_orders: 0,
  current_month_purchase_value: 0,
  active_shipments: 0,
  overall_average_mape: 0,
  total_forecast_quantity: 0,
  total_actual_quantity: 0,
  supplier_delay_rates: [],
  inventory_status_distribution: [],
  purchase_order_trend: [],
  warehouse_utilization: [],
  shipment_status_distribution: [],
  forecast_accuracy_distribution: [],
  recommendations: [],
};


function createMessageId() {
  if (
    typeof crypto !== "undefined"
    && typeof crypto.randomUUID === "function"
  ) {
    return crypto.randomUUID();
  }

  return `${Date.now()}-${Math.random()}`;
}


function normalizeDashboard(data) {
  return {
    low_stock_products:
      data.low_stock_products ?? 0,

    total_suppliers:
      data.total_suppliers ?? 0,

    delayed_purchase_orders:
      data.delayed_purchase_orders ?? 0,

    open_purchase_orders:
      data.open_purchase_orders ?? 0,

    current_month_purchase_value:
      data.current_month_purchase_value ?? 0,

    active_shipments:
      data.active_shipments ?? 0,

    overall_average_mape:
      data.overall_average_mape ?? 0,

    total_forecast_quantity:
      data.total_forecast_quantity ?? 0,

    total_actual_quantity:
      data.total_actual_quantity ?? 0,

    supplier_delay_rates:
      Array.isArray(data.supplier_delay_rates)
        ? data.supplier_delay_rates
        : [],

    inventory_status_distribution:
      Array.isArray(
        data.inventory_status_distribution
      )
        ? data.inventory_status_distribution
        : [],

    purchase_order_trend:
      Array.isArray(data.purchase_order_trend)
        ? data.purchase_order_trend
        : [],

    warehouse_utilization:
      Array.isArray(data.warehouse_utilization)
        ? data.warehouse_utilization
        : [],

    shipment_status_distribution:
      Array.isArray(
        data.shipment_status_distribution
      )
        ? data.shipment_status_distribution
        : [],

    forecast_accuracy_distribution:
      Array.isArray(
        data.forecast_accuracy_distribution
      )
        ? data.forecast_accuracy_distribution
        : [],

    recommendations:
      Array.isArray(data.recommendations)
        ? data.recommendations
        : [],
  };
}


function App() {
  const [question, setQuestion] = useState("");
  const [messages, setMessages] = useState([]);

  /*
   * LangGraph conversation identifier.
   *
   * The first request sends null.
   * The backend creates a thread_id and returns it.
   * Every follow-up request sends that same thread_id.
   */
  const [threadId, setThreadId] = useState(null);

  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const [dashboard, setDashboard] = useState(
    EMPTY_DASHBOARD
  );

  const [dashboardLoading, setDashboardLoading] =
    useState(true);

  const [dashboardError, setDashboardError] =
    useState("");


  useEffect(() => {
    loadDashboardSummary();
  }, []);


  async function loadDashboardSummary() {
    setDashboardLoading(true);
    setDashboardError("");

    try {
      const data = await fetchDashboardSummary();

      setDashboard(
        normalizeDashboard(data)
      );
    } catch (requestError) {
      setDashboardError(
        requestError.message
        || "Unable to load dashboard summary."
      );
    } finally {
      setDashboardLoading(false);
    }
  }


  function handleQuestionChange(event) {
    setQuestion(event.target.value);
  }


  async function handleSubmit() {
    const cleanedQuestion = question.trim();

    if (!cleanedQuestion || loading) {
      return;
    }

    const userMessage = {
      id: createMessageId(),
      role: "user",
      text: cleanedQuestion,
    };

    setMessages((currentMessages) => [
      ...currentMessages,
      userMessage,
    ]);

    setQuestion("");
    setLoading(true);
    setError("");

    const requestStartTime = performance.now();

    try {
      /*
       * IMPORTANT:
       *
       * threadId is sent with every request.
       *
       * First question:
       *     threadId = null
       *
       * Backend creates:
       *     thread_id = UUID
       *
       * Follow-up questions:
       *     same UUID is sent back.
       */
      const data = await submitAIQuestion(
        cleanedQuestion,
        threadId
      );

      /*
       * Store the thread_id returned by FastAPI.
       *
       * This is what connects future questions to the
       * LangGraph conversation history.
       */
      if (data.thread_id) {
        setThreadId(data.thread_id);
      }

      const requestEndTime = performance.now();

      const responseTime = (
        (requestEndTime - requestStartTime) / 1000
      ).toFixed(2);

      const assistantMessage = {
        id: createMessageId(),

        role: "assistant",

        text:
          data.answer
          || "The request completed, but no answer was returned.",

        status:
          data.status
          || "success",

        intent:
          data.intent
          || "analytics",

        answerSource:
          data.answer_source
          || "workflow",

        responseTime,

        generatedSql:
          data.generated_sql
          || null,

        data:
          Array.isArray(data.data)
            ? data.data
            : [],
      };

      setMessages((currentMessages) => [
        ...currentMessages,
        assistantMessage,
      ]);
    } catch (requestError) {
      const errorMessageText =
        requestError.message
        || "Unable to connect to the backend.";

      setError(errorMessageText);

      const errorMessage = {
        id: createMessageId(),
        role: "assistant",
        text: errorMessageText,
        status: "error",
        intent: "request_error",
        answerSource: "frontend",
        responseTime: null,
        generatedSql: null,
        data: [],
      };

      setMessages((currentMessages) => [
        ...currentMessages,
        errorMessage,
      ]);
    } finally {
      setLoading(false);
    }
  }


  function handleClearConversation() {
    /*
     * Clearing the UI must also clear the thread ID.
     *
     * Otherwise the screen would look like a new conversation
     * while LangGraph would still remember the previous one.
     */
    setMessages([]);
    setThreadId(null);
    setError("");
    setQuestion("");
  }


  return (
    <main className="app">
      <section className="copilot-shell">

        <header className="header">
          <div>
            <p className="eyebrow">
              SUPPLY CHAIN CONTROL TOWER
            </p>

            <h1>
              AI-Powered Supply Chain Copilot
            </h1>

            <p className="subtitle">
              Monitor inventory, purchasing, supplier
              reliability, logistics, warehouse capacity,
              and demand forecasting from one command center.
            </p>
          </div>

          <button
            type="button"
            className="clear-button"
            onClick={handleClearConversation}
            disabled={
              loading
              || messages.length === 0
            }
          >
            Clear conversation
          </button>
        </header>


        <Dashboard
          dashboard={dashboard}
          loading={dashboardLoading}
          error={dashboardError}
          onRefresh={loadDashboardSummary}
        />


        <section className="copilot-section">

          <div className="copilot-section-heading">
            <div>
              <p className="section-eyebrow">
                AI COPILOT
              </p>

              <h2>
                Ask your supply-chain data
              </h2>
            </div>

            <p>
              Investigate exceptions, compare suppliers,
              inspect inventory, evaluate forecasts, and
              explore operational data using natural language.
            </p>
          </div>


          <ChatWindow
            messages={messages}
            loading={loading}
          />


          {error && (
            <div className="error-banner">
              {error}
            </div>
          )}


          <QuestionInput
            question={question}
            loading={loading}
            onQuestionChange={handleQuestionChange}
            onSubmit={handleSubmit}
          />

        </section>

      </section>
    </main>
  );
}


export default App;