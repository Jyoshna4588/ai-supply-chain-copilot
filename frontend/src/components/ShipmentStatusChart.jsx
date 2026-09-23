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


function ShipmentStatusChart({
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
            LOGISTICS
          </p>

          <h3>
            Shipment status
          </h3>
        </div>
      </div>

      <p className="chart-description">
        Current shipment distribution across
        logistics stages.
      </p>

      {(loading || !hasData) ? (
        <ChartState
          loading={loading}
          hasData={hasData}
          loadingText="Loading shipment status..."
          emptyText="No shipment-status data is available."
        />
      ) : (
        <div className="chart-canvas">
          <ResponsiveContainer
            width="100%"
            height="100%"
          >
            <BarChart
              data={data}
              margin={{
                top: 12,
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
                dataKey="shipment_status"
                tickLine={false}
              />

              <YAxis
                allowDecimals={false}
                tickLine={false}
              />

              <Tooltip
                formatter={(value) => [
                  Number(value).toLocaleString(),
                  "Shipments",
                ]}
              />

              <Bar
                dataKey="shipment_count"
                name="Shipments"
                fill="#7c3aed"
                radius={[7, 7, 0, 0]}
                maxBarSize={65}
              />
            </BarChart>
          </ResponsiveContainer>
        </div>
      )}
    </article>
  );
}


export default ShipmentStatusChart;