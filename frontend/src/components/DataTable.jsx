function formatColumnName(columnName) {
  return columnName
    .replaceAll("_", " ")
    .replace(
      /\b\w/g,
      (letter) => letter.toUpperCase()
    );
}


function formatCellValue(value) {
  if (
    value === null
    || value === undefined
    || value === ""
  ) {
    return "—";
  }

  if (typeof value === "object") {
    return JSON.stringify(value);
  }

  return String(value);
}


function DataTable({ data }) {
  if (!Array.isArray(data) || data.length === 0) {
    return (
      <p className="empty-table-message">
        No data was returned.
      </p>
    );
  }

  const columns = Object.keys(data[0]);

  return (
    <div className="table-wrapper">
      <table className="data-table">
        <thead>
          <tr>
            {columns.map((columnName) => (
              <th key={columnName}>
                {formatColumnName(columnName)}
              </th>
            ))}
          </tr>
        </thead>

        <tbody>
          {data.map((row, rowIndex) => (
            <tr key={rowIndex}>
              {columns.map((columnName) => (
                <td
                  key={`${rowIndex}-${columnName}`}
                >
                  {formatCellValue(
                    row[columnName]
                  )}
                </td>
              ))}
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}


export default DataTable;