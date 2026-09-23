function ChartState({
  loading,
  hasData,
  loadingText = "Loading chart...",
  emptyText = "No chart data is available.",
}) {
  if (loading) {
    return (
      <div className="chart-state">
        <span className="chart-loader" />

        <span>{loadingText}</span>
      </div>
    );
  }

  if (!hasData) {
    return (
      <div className="chart-state">
        {emptyText}
      </div>
    );
  }

  return null;
}


export default ChartState;