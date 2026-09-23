function KpiCard({
  label,
  value,
  description,
  icon,
  tone,
  loading,
}) {
  return (
    <article className="kpi-card">
      <div className={`kpi-icon kpi-icon-${tone}`}>
        {icon}
      </div>

      <div>
        <p className="kpi-label">
          {label}
        </p>

        <strong className="kpi-value">
          {loading ? "—" : value}
        </strong>

        <p className="kpi-description">
          {description}
        </p>
      </div>
    </article>
  );
}


export default KpiCard;