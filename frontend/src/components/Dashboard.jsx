import ForecastAccuracyChart
  from "./ForecastAccuracyChart";

import InsightsPanel
  from "./InsightsPanel";

import InventoryStatusChart
  from "./InventoryStatusChart";

import KpiCard
  from "./KpiCard";

import PurchaseOrderTrendChart
  from "./PurchaseOrderTrendChart";

import ShipmentStatusChart
  from "./ShipmentStatusChart";

import SupplierChart
  from "./SupplierChart";

import WarehouseUtilizationChart
  from "./WarehouseUtilizationChart";


function Dashboard({
  dashboard,
  loading,
  error,
  onRefresh,
}) {
  const dashboardCards = [
    {
      label: "Low-Stock Products",
      value: dashboard.low_stock_products,
      description: "Require replenishment",
      icon: "!",
      tone: "warning",
    },
    {
      label: "Total Suppliers",
      value: dashboard.total_suppliers,
      description: "Tracked suppliers",
      icon: "S",
      tone: "primary",
    },
    {
      label: "Delayed Orders",
      value: dashboard.delayed_purchase_orders,
      description: "Delayed or overdue",
      icon: "D",
      tone: "danger",
    },
    {
      label: "Open Orders",
      value: dashboard.open_purchase_orders,
      description: "Awaiting completion",
      icon: "O",
      tone: "success",
    },
    {
      label: "Monthly PO Value",
      value: `$${Number(
        dashboard.current_month_purchase_value
      ).toLocaleString(undefined, {
        maximumFractionDigits: 0,
      })}`,
      description: "Current-month purchasing",
      icon: "$",
      tone: "primary",
    },
    {
      label: "Active Shipments",
      value: dashboard.active_shipments,
      description: "Not yet delivered",
      icon: "T",
      tone: "warning",
    },
  ];

  return (
    <section className="dashboard-section">
      <div className="section-heading">
        <div>
          <p className="section-eyebrow">
            EXECUTIVE OVERVIEW
          </p>

          <h2>
            Supply-chain command center
          </h2>

          <p className="section-description">
            A unified operational view of inventory,
            suppliers, purchasing, logistics, warehouses,
            and demand planning.
          </p>
        </div>

        <button
          type="button"
          className="refresh-button"
          onClick={onRefresh}
          disabled={loading}
        >
          {loading
            ? "Refreshing..."
            : "Refresh dashboard"}
        </button>
      </div>

      {error && (
        <div className="dashboard-error">
          <span>{error}</span>

          <button
            type="button"
            onClick={onRefresh}
            disabled={loading}
          >
            Try again
          </button>
        </div>
      )}

      <div className="kpi-grid">
        {dashboardCards.map((card) => (
          <KpiCard
            key={card.label}
            label={card.label}
            value={card.value}
            description={card.description}
            icon={card.icon}
            tone={card.tone}
            loading={loading}
          />
        ))}
      </div>

      <div className="dashboard-subheading">
        <div>
          <p className="section-eyebrow">
            PERFORMANCE & RISK
          </p>

          <h3>
            Operational analytics
          </h3>
        </div>
      </div>

      <div className="dashboard-grid">
        <div className="dashboard-grid-wide">
          <SupplierChart
            data={dashboard.supplier_delay_rates}
            loading={loading}
          />
        </div>

        <InventoryStatusChart
          data={
            dashboard.inventory_status_distribution
          }
          loading={loading}
        />

        <PurchaseOrderTrendChart
          data={dashboard.purchase_order_trend}
          loading={loading}
        />

        <WarehouseUtilizationChart
          data={dashboard.warehouse_utilization}
          loading={loading}
        />

        <ShipmentStatusChart
          data={
            dashboard.shipment_status_distribution
          }
          loading={loading}
        />

        <ForecastAccuracyChart
          data={
            dashboard.forecast_accuracy_distribution
          }
          averageMape={
            dashboard.overall_average_mape
          }
          totalForecast={
            dashboard.total_forecast_quantity
          }
          totalActual={
            dashboard.total_actual_quantity
          }
          loading={loading}
        />

        <InsightsPanel
          recommendations={
            dashboard.recommendations
          }
          loading={loading}
        />
      </div>
    </section>
  );
}


export default Dashboard;