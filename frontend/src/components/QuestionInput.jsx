function QuestionInput({
  question,
  loading,
  onQuestionChange,
  onSubmit,
}) {
  function handleKeyDown(event) {
    if (
      event.key === "Enter"
      && !event.shiftKey
    ) {
      event.preventDefault();
      onSubmit();
    }
  }

  return (
    <section className="composer">
      <label htmlFor="question">
        Ask a supply-chain question
      </label>

      <textarea
        id="question"
        value={question}
        onChange={onQuestionChange}
        onKeyDown={handleKeyDown}
        placeholder="Type your question here..."
        rows="3"
        disabled={loading}
      />

      <div className="composer-footer">
        <p>
          Press Enter to send. Use Shift + Enter
          for a new line.
        </p>

        <button
          type="button"
          onClick={onSubmit}
          disabled={
            loading
            || !question.trim()
          }
        >
          {loading
            ? "Analyzing..."
            : "Send"}
        </button>
      </div>
    </section>
  );
}


export default QuestionInput;