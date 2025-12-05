import {
  Box,
  Button,
  Typography,
  CircularProgress,
  Alert,
} from "@mui/material";
import { useTopCategories } from "../hooks/useTopCategories";

function TopCategoriesSection({ onCategorySearch, show = true }) {
  const { categories, loading, error } = useTopCategories({
    limit: 8,
    autoFetch: true,
  });

  const handleCategoryClick = (category) => {
    if (onCategorySearch) {
      const searchQuery = `${category}`;
      onCategorySearch(searchQuery);
    }
  };

  // Don't show if explicitly hidden or no categories
  if (!show || (!loading && !error && categories.length === 0)) {
    return null;
  }

  return (
    <Box sx={{ mb: 4 }}>
      <Typography
        variant="h6"
        component="h2"
        sx={{ mb: 2, fontWeight: 500, textAlign: "center" }}
      >
        Popular Categories
      </Typography>

      {loading && (
        <Box sx={{ display: "flex", justifyContent: "center", py: 3 }}>
          <CircularProgress size={24} />
        </Box>
      )}

      {error && (
        <Alert severity="error" sx={{ mb: 2 }}>
          Failed to load categories: {error}
        </Alert>
      )}

      {!loading && !error && categories.length > 0 && (
        <Box
          sx={{
            display: "flex",
            gap: 1.5,
            flexWrap: "wrap",
            justifyContent: "center",
          }}
        >
          {categories.map((item) => (
            <Button
              key={item.category}
              size="medium"
              variant="outlined"
              disableElevation
              onClick={() => handleCategoryClick(item.category)}
              sx={{
                borderRadius: "999px",
                textTransform: "capitalize",
                fontWeight: 500,
                letterSpacing: 0.5,
                paddingX: 2,
                paddingY: 0.75,
                cursor: "pointer",
                minWidth: "auto",
                "&:hover": {
                  backgroundColor: "primary.main",
                  color: "white",
                },
              }}
            >
              {item.category}
              <Typography
                variant="caption"
                component="span"
                sx={{
                  ml: 1,
                  opacity: 0.7,
                  fontSize: "0.7rem",
                }}
              >
                ({item.count})
              </Typography>
            </Button>
          ))}
        </Box>
      )}
    </Box>
  );
}

export default TopCategoriesSection;
