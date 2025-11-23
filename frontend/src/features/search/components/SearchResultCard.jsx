// src/features/search/components/SearchResultCard.jsx
import { Paper, Box, Typography, Link } from "@mui/material";

function highlightText(text, query) {
  if (!text || !query) return text;
  const escaped = query.replace(/[.*+?^${}()|[\]\\]/g, "\\$&");
  const regex = new RegExp(`(${escaped})`, "gi");
  const parts = text.split(regex);
  return parts.map((part, idx) =>
    idx % 2 === 1 ? (
      <mark key={idx} style={{ backgroundColor: "#fff59d" }}>
        {part}
      </mark>
    ) : (
      part
    )
  );
}

function buildSnippet(result) {
  const base =
    result.excerpt || result.content || "No description available yet.";
  if (base.length <= 300) return base;
  return base.slice(0, 300) + "…";
}

function SearchResultCard({ result, query }) {
  const snippet = buildSnippet(result);

  return (
    <Paper
      variant="outlined"
      sx={{
        p: 2,
        borderRadius: 2,
        "&:hover": { boxShadow: 2 },
      }}
    >
      <Box>
        <Typography variant="caption" color="text.secondary">
          {result.source && `${result.source} · `}
          {result.url}
        </Typography>

        <Typography
          variant="h6"
          component={Link}
          href={result.url}
          target="_blank"
          rel="noopener noreferrer"
          underline="hover"
          sx={{ display: "block", mt: 0.5 }}
        >
          {highlightText(result.title || "Untitled hack", query)}
        </Typography>

        <Typography
          variant="body2"
          color="text.secondary"
          sx={{
            mt: 0.5,
            display: "-webkit-box",
            WebkitLineClamp: 3,
            WebkitBoxOrient: "vertical",
            overflow: "hidden",
          }}
        >
          {highlightText(snippet, query)}
        </Typography>

        <Typography variant="caption" color="text.secondary" sx={{ mt: 0.5 }}>
          {result.author && `${result.author} · `}
          {result.date}
        </Typography>
      </Box>
    </Paper>
  );
}

export default SearchResultCard;
