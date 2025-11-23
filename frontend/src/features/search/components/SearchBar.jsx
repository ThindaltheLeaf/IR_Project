// src/features/search/components/SearchBar.jsx
import {
  Box,
  TextField,
  IconButton,
  InputAdornment,
  CircularProgress,
} from "@mui/material";
import SearchIcon from "@mui/icons-material/Search";

function SearchBar({ query, onQueryChange, onSubmit, loading }) {
  const handleSubmit = (e) => {
    e.preventDefault();
    onSubmit();
  };

  return (
    <Box component="form" onSubmit={handleSubmit} sx={{ mb: 3 }}>
      <TextField
        fullWidth
        variant="outlined"
        placeholder="Search IKEA hacks..."
        value={query}
        onChange={(e) => onQueryChange(e.target.value)}
        InputProps={{
          endAdornment: (
            <InputAdornment position="end">
              <IconButton type="submit" edge="end" aria-label="search">
                {loading ? <CircularProgress size={22} /> : <SearchIcon />}
              </IconButton>
            </InputAdornment>
          ),
        }}
      />
    </Box>
  );
}

export default SearchBar;
