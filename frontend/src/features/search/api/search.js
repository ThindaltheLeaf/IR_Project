import { apiClient } from "../../../lib/apiClient";

export async function searchHacks({ query, page = 1, pageSize = 10 }) {
  if (!query || !query.trim()) {
    return { total: 0, hits: [], page: 1, page_size: pageSize, total_pages: 0 };
  }

  const data = await apiClient.get("/api/search", {
    params: {
      query: query.trim(),
      page,
      page_size: pageSize,
    },
  });

  return data;
}
