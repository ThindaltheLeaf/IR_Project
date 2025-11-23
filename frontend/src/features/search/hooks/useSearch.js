// src/features/search/hooks/useSearch.js
import { useState } from "react";
import { searchHacks } from "../api/search";

export function useSearch(initialPageSize = 10) {
  const [query, setQuery] = useState("");
  const [results, setResults] = useState([]);
  const [total, setTotal] = useState(0);
  const [page, setPage] = useState(1);
  const [pageSize] = useState(initialPageSize);
  const [totalPages, setTotalPages] = useState(0);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const runSearch = async (overridePage) => {
    const effectivePage = overridePage ?? page;
    if (!query.trim()) return;

    try {
      setLoading(true);
      setError(null);

      const data = await searchHacks({
        query,
        page: effectivePage,
        pageSize,
      });

      setResults(data.hits || []);
      setTotal(data.total || 0);
      setPage(data.page || effectivePage);
      setTotalPages(
        data.total_pages || (data.total ? Math.ceil(data.total / pageSize) : 0)
      );
    } catch (err) {
      console.error(err);
      setError(err.message || "Search failed");
      setResults([]);
      setTotal(0);
      setTotalPages(0);
    } finally {
      setLoading(false);
    }
  };

  const updateQuery = (value) => {
    setQuery(value);
    setPage(1);
  };

  return {
    query,
    setQuery: updateQuery,
    results,
    total,
    page,
    pageSize,
    totalPages,
    loading,
    error,
    search: runSearch,
  };
}
