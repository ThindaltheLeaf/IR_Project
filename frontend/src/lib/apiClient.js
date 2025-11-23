const API_BASE_URL = import.meta.env.VITE_API_BASE_URL;

async function request(path, { method = "GET", params, body, headers } = {}) {
  const url = new URL(path, API_BASE_URL);

  if (params) {
    Object.entries(params).forEach(([key, value]) => {
      if (value !== undefined && value !== null) {
        url.searchParams.set(key, String(value));
      }
    });
  }

  const init = {
    method,
    headers: {
      "Content-Type": "application/json",
      ...(headers || {}),
    },
  };

  if (body) {
    init.body = JSON.stringify(body);
  }

  const res = await fetch(url.toString(), init);

  if (!res.ok) {
    const text = await res.text().catch(() => "");
    const error = new Error(
      `HTTP ${res.status} ${res.statusText} – ${text || "Request failed"}`
    );
    error.status = res.status;
    throw error;
  }

  return res.json();
}

export const apiClient = {
  get: (path, options) => request(path, { ...options, method: "GET" }),
  post: (path, options) => request(path, { ...options, method: "POST" }),
};
