import ChartState from "./ChartState";


function InsightsPanel({
  recommendations,
  loading,
}) {
  const hasData =
    Array.isArray(recommendations)
    && recommendations.length > 0;

  return (
    <article className="chart-card insights-card">
      <div className="chart-header">
        <div>
          <p className="chart-eyebrow">
            DECISION SUPPORT
          </p>

          <h3>
            Recommended actions
          </h3>
        </div>

        <span className="chart-badge chart-badge-ai">
          AI-ready
        </span>
      </div>

      <p className="chart-description">
        Prioritized operational actions derived
        from current dashboard exceptions.
      </p>

      {(loading || !hasData) ? (
        <ChartState
          loading={loading}
          hasData={hasData}
          loadingText="Generating operational insights..."
          emptyText="No recommendations are available."
        />
      ) : (
        <div className="insights-list">
          {recommendations.map(
            (recommendation, index) => (
              <div
                className={
                  `insight-item insight-${recommendation.severity}`
                }
                key={
                  `${recommendation.title}-${index}`
                }
              >
                <span
                  className="insight-indicator"
                  aria-hidden="true"
                />

                <div>
                  <h4>
                    {recommendation.title}
                  </h4>

                  <p>
                    {recommendation.message}
                  </p>
                </div>
              </div>
            )
          )}
        </div>
      )}
    </article>
  );
}


export default InsightsPanel;