import { useCallback, useState } from "react";
import { getHacksByCategory } from "../api/getHacksByCategory";

export function useHacksByCategory(categoryName, options = {}) {
  const { pageSize = 10, autoFetch = false } = options;
  const [result, setResult] = useState({
    hits: [],
    total: 0,
    page: 1,
    totalPages: 0,
    pageSize: pageSize,
  });
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [hasFetched, setHasFetched] = useState(false);

  const fetchHacks = useCallback(
    async (page = 1, force = false) => {
      if (!categoryName) return;
      if (hasFetched && !force && page === result.page) return;

      setLoading(true);
      setError(null);

      try {
        const data = await getHacksByCategory({
          categoryName,
          page,
          pageSize,
        });

        setResult({
          hits: data.hits || [],
          total: data.total || 0,
          page: data.page || 1,
          totalPages: data.total_pages || 0,
          pageSize: data.page_size || pageSize,
        });
        setHasFetched(true);
      } catch (err) {
        setError(err?.message || "Failed to load hacks by category");
        setResult((prev) => ({ ...prev, hits: [] }));
      } finally {
        setLoading(false);
      }
    },
    [categoryName, pageSize, hasFetched, result.page]
  );

  const goToPage = useCallback(
    (page) => {
      fetchHacks(page);
    },
    [fetchHacks]
  );

  const refresh = useCallback(() => {
    setHasFetched(false);
    fetchHacks(1, true);
  }, [fetchHacks]);

  return {
    ...result,
    loading,
    error,
    hasFetched,
    fetchHacks,
    goToPage,
    refresh,
  };
}
