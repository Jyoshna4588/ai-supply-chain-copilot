import {
  Bar,
  BarChart,
  CartesianGrid,
  LabelList,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
} from "recharts";

import ChartState from "./ChartState";


function SupplierChart({
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
            SUPPLIER RISK
          </p>

          <h3>
            Highest supplier delay rates
          </h3>
        </div>

        <span className="chart-badge">
          Top 5
        </span>
      </div>

      <p className="chart-description">
        Suppliers with the highest recorded delay
        percentages require the closest attention.
      </p>

      {(loading || !hasData) ? (
        <ChartState
          loading={loading}
          hasData={hasData}
          loadingText="Loading supplier performance..."
          emptyText="No supplier delay data is available."
        />
      ) : (
        <div className="chart-canvas chart-canvas-large">
          <ResponsiveContainer
            width="100%"
            height="100%"
          >
            <BarChart
              data={data}
              layout="vertical"
              margin={{
                top: 8,
                right: 60,
                bottom: 8,
                left: 20,
              }}
            >
              <CartesianGrid
                strokeDasharray="3 3"
                horizontal={false}
              />

              <XAxis
                type="number"
                domain={[0, "dataMax + 5"]}
                tickFormatter={(value) => (
                  `${value}%`
                )}
              />

              <YAxis
                dataKey="supplier_name"
                type="category"
                width={160}
                tickLine={false}
                axisLine={false}
              />

              <Tooltip
                formatter={(value) => [
                  `${Number(value).toFixed(2)}%`,
                  "Delay rate",
                ]}
              />

              <Bar
                dataKey="delay_rate"
                fill="#2563eb"
                radius={[0, 7, 7, 0]}
                barSize={32}
              >
                <LabelList
                  dataKey="delay_rate"
                  position="right"
                  formatter={(value) => (
                    `${Number(value).toFixed(2)}%`
                  )}
                />
              </Bar>
            </BarChart>
          </ResponsiveContainer>
        </div>
      )}
    </article>
  );
}


export default SupplierChart;