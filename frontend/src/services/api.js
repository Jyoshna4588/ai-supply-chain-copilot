const API_BASE_URL =
  import.meta.env.VITE_API_BASE_URL ||
  "https://supply-chain-ai-620610885141.us-central1.run.app";

async function parseResponse(response) {
  let data;

  try {
    data = await response.json();
  } catch {
    throw new Error(
      "The backend returned an invalid response."
    );
  }

  if (!response.ok) {
    throw new Error(
      data.error
      || data.detail
      || data.message
      || "The backend returned an error."
    );
  }

  return data;
}


export async function fetchDashboardSummary() {
  const response = await fetch(
    `${API_BASE_URL}/dashboard/summary`
  );

  return parseResponse(response);
}


export async function submitAIQuestion(
  question,
  threadId = null
) {
  const requestBody = {
    question,
  };

  /*
   * Send the conversation thread ID only when one already exists.
   *
   * First question:
   * {
   *   "question": "Which supplier has the highest delay rate?"
   * }
   *
   * Follow-up question:
   * {
   *   "question": "Why is that risky?",
   *   "thread_id": "existing-thread-id"
   * }
   */
  if (threadId) {
    requestBody.thread_id = threadId;
  }

  const response = await fetch(
    `${API_BASE_URL}/ai/query`,
    {
      method: "POST",

      headers: {
        "Content-Type": "application/json",
      },

      body: JSON.stringify(requestBody),
    }
  );

  return parseResponse(response);
}