import {
  Cell,
  Pie,
  PieChart,
  ResponsiveContainer,
  Tooltip,
} from "recharts";

import ChartState from "./ChartState";


const FORECAST_COLORS = [
  "#16a34a",
  "#2563eb",
  "#f59e0b",
  "#ef4444",
  "#7c3aed",
  "#64748b",
];


function ForecastAccuracyChart({
  data,
  averageMape,
  totalForecast,
  totalActual,
  loading,
}) {
  const hasData =
    Array.isArray(data)
    && data.length > 0;

  return (
    <article className="chart-card forecast-card">
      <div className="chart-header">
        <div>
          <p className="chart-eyebrow">
            DEMAND PLANNING
          </p>

          <h3>
            Forecast accuracy
          </h3>
        </div>

        <span className="chart-badge">
          MAPE {Number(averageMape).toFixed(1)}%
        </span>
      </div>

      <p className="chart-description">
        Forecast-performance categories and the
        overall forecast error.
      </p>

      {(loading || !hasData) ? (
        <ChartState
          loading={loading}
          hasData={hasData}
          loadingText="Loading forecast accuracy..."
          emptyText="No forecast-accuracy data is available."
        />
      ) : (
        <>
          <div className="forecast-layout">
            <div className="forecast-chart">
              <ResponsiveContainer
                width="100%"
                height="100%"
              >
                <PieChart>
                  <Pie
                    data={data}
                    dataKey="forecast_count"
                    nameKey="accuracy_status"
                    innerRadius={52}
                    outerRadius={82}
                    paddingAngle={3}
                  >
                    {data.map((entry, index) => (
                      <Cell
                        key={
                          `${entry.accuracy_status}-${index}`
                        }
                        fill={
                          FORECAST_COLORS[
                            index
                            % FORECAST_COLORS.length
                          ]
                        }
                      />
                    ))}
                  </Pie>

                  <Tooltip
                    formatter={(value) => [
                      Number(value).toLocaleString(),
                      "Forecast records",
                    ]}
                  />
                </PieChart>
              </ResponsiveContainer>
            </div>

            <div className="forecast-summary">
              <div>
                <span>
                  Average MAPE
                </span>

                <strong>
                  {Number(averageMape).toFixed(2)}%
                </strong>
              </div>

              <div>
                <span>
                  Forecast quantity
                </span>

                <strong>
                  {Number(
                    totalForecast
                  ).toLocaleString()}
                </strong>
              </div>

              <div>
                <span>
                  Actual quantity
                </span>

                <strong>
                  {Number(
                    totalActual
                  ).toLocaleString()}
                </strong>
              </div>
            </div>
          </div>

          <div className="forecast-legend">
            {data.map((entry, index) => (
              <div
                className="forecast-legend-item"
                key={
                  `${entry.accuracy_status}-${index}`
                }
              >
                <span
                  className="forecast-legend-dot"
                  style={{
                    backgroundColor:
                      FORECAST_COLORS[
                        index
                        % FORECAST_COLORS.length
                      ],
                  }}
                />

                <span>
                  {entry.accuracy_status}
                </span>

                <strong>
                  {Number(
                    entry.forecast_count
                  ).toLocaleString()}
                </strong>
              </div>
            ))}
          </div>
        </>
      )}
    </article>
  );
}


export default ForecastAccuracyChart;