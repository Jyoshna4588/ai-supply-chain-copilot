import {
  Bar,
  BarChart,
  CartesianGrid,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
} from "recharts";

import ChartState from "./ChartState";


function PurchaseOrderStatusChart({
  data,
  loading,
}) {
  const hasData =
    Array.isArray(data)
    && data.length > 0;

  const chartState = (
    <ChartState
      loading={loading}
      hasData={hasData}
      loadingText={
        "Loading purchase-order status..."
      }
      emptyText={
        "No purchase-order status data is available."
      }
    />
  );

  return (
    <article className="chart-card">
      <div className="chart-header">
        <div>
          <p className="chart-eyebrow">
            ORDER PIPELINE
          </p>

          <h3>
            Purchase-order status
          </h3>
        </div>
      </div>

      <p className="chart-description">
        Current distribution of open, delayed,
        and completed purchase orders.
      </p>

      {chartState || (
        <div className="chart-canvas">
          <ResponsiveContainer
            width="100%"
            height="100%"
          >
            <BarChart
              data={data}
              margin={{
                top: 12,
                right: 20,
                bottom: 6,
                left: 0,
              }}
            >
              <CartesianGrid
                strokeDasharray="3 3"
                vertical={false}
              />

              <XAxis
                dataKey="order_status"
                tickLine={false}
              />

              <YAxis
                allowDecimals={false}
                tickLine={false}
              />

              <Tooltip
                formatter={(value) => [
                  Number(value).toLocaleString(),
                  "Orders",
                ]}
              />

              <Bar
                dataKey="order_count"
                name="Orders"
                fill="#0f766e"
                radius={[7, 7, 0, 0]}
                maxBarSize={70}
              />
            </BarChart>
          </ResponsiveContainer>
        </div>
      )}
    </article>
  );
}


export default PurchaseOrderStatusChart;