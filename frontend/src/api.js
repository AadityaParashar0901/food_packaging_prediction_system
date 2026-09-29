const API_URL = import.meta.env.VITE_API_URL || "http://localhost:5000/api";

export async function getRecommendation(payload) {
  const response = await fetch(`${API_URL}/packaging/recommend`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(payload),
  });

  const data = await response.json();

  if (!response.ok) {
    const validationErrors = Array.isArray(data?.detail)
      ? data.detail
          .map((error) => {
            const location = Array.isArray(error.loc)
              ? error.loc.filter((part) => part !== "body").join(".")
              : "Input";
            return `${location}: ${error.msg}`;
          })
          .join(" ")
      : "";

    const message = validationErrors ||
      (data?.fields
        ? Object.entries(data.fields)
            .map(([field, error]) => `${field}: ${error}`)
            .join(" ")
        : data?.message || data?.detail || "Unable to get a recommendation.");

    throw new Error(message);
  }

  return data;
}
