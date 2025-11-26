import * as React from "react";
import { Box, Alert } from "@mui/material";

function ErrorBanner({ error }) {
  if (!error) return null;
  return (
    <Box sx={{ mb: 2 }}>
      <Alert severity="error" variant="filled">
        {error}
      </Alert>
    </Box>
  );
}

export default ErrorBanner;
