import {
  CartesianGrid,
  Legend,
  Line,
  LineChart,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
} from "recharts";

import ChartState from "./ChartState";


function PurchaseOrderTrendChart({
  data,
  loading,
}) {
  const hasData =
    Array.isArray(data)
    && data.length > 0;

  return (
    <article className="chart-card">
      <div className="chart-header">
        <div>
          <p className="chart-eyebrow">
            PROCUREMENT TREND
          </p>

          <h3>
            Purchase orders by month
          </h3>
        </div>

        <span className="chart-badge">
          12 months
        </span>
      </div>

      <p className="chart-description">
        Monthly purchase-order volume compared with
        delayed orders.
      </p>

      {(loading || !hasData) ? (
        <ChartState
          loading={loading}
          hasData={hasData}
          loadingText="Loading purchase-order trend..."
          emptyText="No recent purchase-order data is available."
        />
      ) : (
        <div className="chart-canvas">
          <ResponsiveContainer
            width="100%"
            height="100%"
          >
            <LineChart
              data={data}
              margin={{
                top: 10,
                right: 18,
                bottom: 6,
                left: 0,
              }}
            >
              <CartesianGrid
                strokeDasharray="3 3"
                vertical={false}
              />

              <XAxis
                dataKey="month"
                tickLine={false}
              />

              <YAxis
                allowDecimals={false}
                tickLine={false}
              />

              <Tooltip />

              <Legend />

              <Line
                type="monotone"
                dataKey="total_orders"
                name="Total orders"
                stroke="#2563eb"
                strokeWidth={3}
                dot={{ r: 4 }}
              />

              <Line
                type="monotone"
                dataKey="delayed_orders"
                name="Delayed orders"
                stroke="#ef4444"
                strokeWidth={3}
                dot={{ r: 4 }}
              />
            </LineChart>
          </ResponsiveContainer>
        </div>
      )}
    </article>
  );
}


export default PurchaseOrderTrendChart;