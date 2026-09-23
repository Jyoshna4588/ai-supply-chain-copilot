import {
  Cell,
  Legend,
  Pie,
  PieChart,
  ResponsiveContainer,
  Tooltip,
} from "recharts";

import ChartState from "./ChartState";


const STATUS_COLORS = {
  Healthy: "#16a34a",
  Normal: "#16a34a",
  Available: "#16a34a",
  "Low Stock": "#f59e0b",
  Low: "#f59e0b",
  Critical: "#ef4444",
  Overstock: "#2563eb",
  "Out Of Stock": "#991b1b",
  Unknown: "#94a3b8",
};


function InventoryStatusChart({
  data,
  loading,
}) {
  const hasData =
    Array.isArray(data)
    && data.length > 0;

  const totalProducts = hasData
    ? data.reduce(
        (total, item) => (
          total
          + Number(item.product_count || 0)
        ),
        0
      )
    : 0;

  return (
    <article className="chart-card">
      <div className="chart-header">
        <div>
          <p className="chart-eyebrow">
            INVENTORY HEALTH
          </p>

          <h3>
            Stock-status distribution
          </h3>
        </div>
      </div>

      <p className="chart-description">
        Distribution of product inventory positions
        using the status stored in BigQuery.
      </p>

      {(loading || !hasData) ? (
        <ChartState
          loading={loading}
          hasData={hasData}
          loadingText="Loading inventory health..."
          emptyText="No inventory-status data is available."
        />
      ) : (
        <div className="donut-wrapper">
          <div className="chart-canvas">
            <ResponsiveContainer
              width="100%"
              height="100%"
            >
              <PieChart>
                <Pie
                  data={data}
                  dataKey="product_count"
                  nameKey="inventory_status"
                  innerRadius={70}
                  outerRadius={105}
                  paddingAngle={3}
                >
                  {data.map((entry) => (
                    <Cell
                      key={entry.inventory_status}
                      fill={
                        STATUS_COLORS[
                          entry.inventory_status
                        ] || "#64748b"
                      }
                    />
                  ))}
                </Pie>

                <Tooltip
                  formatter={(value) => [
                    Number(value).toLocaleString(),
                    "Products",
                  ]}
                />

                <Legend
                  verticalAlign="bottom"
                  height={36}
                />
              </PieChart>
            </ResponsiveContainer>
          </div>

          <div className="donut-center">
            <strong>
              {totalProducts.toLocaleString()}
            </strong>

            <span>
              Inventory rows
            </span>
          </div>
        </div>
      )}
    </article>
  );
}


export default InventoryStatusChart;