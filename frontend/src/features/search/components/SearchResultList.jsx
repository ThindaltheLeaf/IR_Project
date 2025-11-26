import { Stack, Typography } from "@mui/material";
import SearchResultCard from "./SearchResultCard.jsx";

function SearchResultList({ results, query, loading }) {

  if (!loading && results.length === 0 && query) {
    return (
      <Typography variant="body2" color="text.secondary">
        No results found. Try a different query.
      </Typography>
    );
  }

  return (
    <>
      <Stack spacing={2}>
        {results.map((res) => (
          <SearchResultCard
            key={res.id || res.url}
            result={res}
            query={query}
          />
        ))}
      </Stack>
    </>
  );
}

export default SearchResultList;
