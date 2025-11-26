import { Box, Typography } from "@mui/material";

function StatusLine({ page, totalPages, error, loading, results, total }) {
  if (!totalPages || totalPages <= 1) return null;

  return (
     <Box sx={{ mb: 2, minHeight: 24 }}>
        {!error && !loading && results.length > 0 && (
          <Typography variant="body2" color="text.secondary">
            About {total} result{total === 1 ? "" : "s"} (page {page} of{" "}
            {totalPages || 1})
          </Typography>
        )}
      </Box>
  );
}

export default StatusLine;
