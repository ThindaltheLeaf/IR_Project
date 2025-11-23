import { Container, Box, Typography } from "@mui/material";
import SearchBar from "./SearchBar.jsx";
import SearchResultList from "./SearchResultList.jsx";
import PaginationBar from "./PaginationBar.jsx";
import StatusLine  from "./StatusLine.jsx";
import { useSearch } from "../hooks/useSearch.js";

function SearchPage() {
  const {
    query,
    setQuery,
    results,
    total,
    page,
    pageSize,
    totalPages,
    loading,
    error,
    search,
  } = useSearch(10);

  const handlePageChange = (_event, newPage) => {
    // Ask the hook to run the search for the new page
    search(newPage);
  };

  return (
    <Container maxWidth="md" sx={{ py: 6 }}>
      <Box sx={{ textAlign: "center", mb: 4 }}>
        <Typography variant="h3" component="h1" sx={{ fontWeight: 600 }}>
          IKEA Hacks Search
        </Typography>
        <Typography variant="subtitle1" color="text.secondary">
          Search across IKEA hacks from multiple websites and <a href="https://www.reddit.com/r/ikeahacks/">r/ikeahacks</a>
        </Typography>
      </Box>

      <SearchBar
        query={query}
        onQueryChange={setQuery}
        onSubmit={() => search(1)}
        loading={loading}
      />

      <StatusLine
        page={page}
        total={total}
        totalPages={totalPages}
        pageSize={pageSize}
        error={error}
        loading={loading}
        results={results}
      />
 
      <SearchResultList
        results={results}
        query={query}
        loading={loading}
        error={error}
      />

      <PaginationBar
        page={page}
        totalPages={totalPages}
        onChange={handlePageChange}
        disabled={loading}
      />
    </Container>
  );
}

export default SearchPage;
