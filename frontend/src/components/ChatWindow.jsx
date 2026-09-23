import MessageBubble from "./MessageBubble";


function ChatWindow({
  messages,
  loading,
}) {
  return (
    <section className="chat-window">
      {messages.length === 0 && !loading && (
        <div className="empty-state">
          <h2>Start a conversation</h2>

          <p>
            Try asking:
            “Which supplier has the longest average
            lead time?”
          </p>
        </div>
      )}

      {messages.map((message) => (
        <MessageBubble
          key={message.id}
          message={message}
        />
      ))}

      {loading && (
        <article className="message-row assistant">
          <div className="avatar">
            AI
          </div>

          <div className="message-content">
            <p className="message-role">
              Supply Chain Copilot
            </p>

            <div className="message-bubble assistant">
              <p className="thinking-message">
                Analyzing supply-chain data...
              </p>
            </div>
          </div>
        </article>
      )}
    </section>
  );
}


export default ChatWindow;