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


function WarehouseUtilizationChart({
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
            WAREHOUSE CAPACITY
          </p>

          <h3>
            Warehouse utilization
          </h3>
        </div>
      </div>

      <p className="chart-description">
        Utilization percentages for the busiest
        warehouse locations.
      </p>

      {(loading || !hasData) ? (
        <ChartState
          loading={loading}
          hasData={hasData}
          loadingText="Loading warehouse utilization..."
          emptyText="No warehouse utilization data is available."
        />
      ) : (
        <div className="chart-canvas">
          <ResponsiveContainer
            width="100%"
            height="100%"
          >
            <BarChart
              data={data}
              layout="vertical"
              margin={{
                top: 8,
                right: 56,
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
                domain={[0, 100]}
                tickFormatter={(value) => (
                  `${value}%`
                )}
              />

              <YAxis
                type="category"
                dataKey="warehouse_name"
                width={135}
                tickLine={false}
                axisLine={false}
              />

              <Tooltip
                formatter={(value) => [
                  `${Number(value).toFixed(2)}%`,
                  "Utilization",
                ]}
              />

              <Bar
                dataKey="utilization_percent"
                fill="#0f766e"
                radius={[0, 7, 7, 0]}
                barSize={27}
              >
                <LabelList
                  dataKey="utilization_percent"
                  position="right"
                  formatter={(value) => (
                    `${Number(value).toFixed(1)}%`
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


export default WarehouseUtilizationChart;