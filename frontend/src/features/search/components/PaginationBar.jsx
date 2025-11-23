import { Box, Pagination } from "@mui/material";

function PaginationBar({ page, totalPages, onChange, disabled = false }) {
  if (!totalPages || totalPages <= 1) return null;

  return (
    <Box sx={{ display: "flex", justifyContent: "center", mt: 3 }}>
      <Pagination
        count={totalPages}
        page={page}
        onChange={onChange}
        disabled={disabled}
        color="primary"
      />
    </Box>
  );
}

export default PaginationBar;
