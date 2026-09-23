import DataTable from "./DataTable";


function MessageBubble({ message }) {
  const isUser = message.role === "user";
  const isAssistant = message.role === "assistant";

  return (
    <article
      className={`message-row ${message.role}`}
    >
      <div className="avatar">
        {isUser ? "You" : "AI"}
      </div>

      <div className="message-content">
        <p className="message-role">
          {isUser
            ? "You"
            : "Supply Chain Copilot"}
        </p>

        <div
          className={
            `message-bubble ${message.role}`
          }
        >
          <p className="message-text">
            {message.text}
          </p>

          {isAssistant && (
            <>
              <div className="message-metadata">
                <span>
                  Status:
                  <strong>
                    {message.status || "unknown"}
                  </strong>
                </span>

                <span>
                  Intent:
                  <strong>
                    {message.intent || "unknown"}
                  </strong>
                </span>

                <span>
                  Source:
                  <strong>
                    {message.answerSource || "unknown"}
                  </strong>
                </span>

                <span>
                  Time:
                  <strong>
                    {message.responseTime
                      ? `${message.responseTime}s`
                      : "N/A"}
                  </strong>
                </span>
              </div>

              {message.generatedSql && (
                <details className="details-panel">
                  <summary>
                    View generated SQL
                  </summary>

                  <pre>
                    {message.generatedSql}
                  </pre>
                </details>
              )}

              {Array.isArray(message.data)
                && message.data.length > 0 && (
                  <details className="details-panel">
                    <summary>
                      View returned data
                    </summary>

                    <DataTable data={message.data} />
                  </details>
                )}
            </>
          )}
        </div>
      </div>
    </article>
  );
}


export default MessageBubble;