import { useState, useEffect } from "react";
import { Container, Box, Typography, Chip, Link } from "@mui/material";
import CloseIcon from "@mui/icons-material/Close";
import SearchBar from "./SearchBar.jsx";
import SearchResultList from "./SearchResultList.jsx";
import PaginationBar from "./PaginationBar.jsx";
import StatusLine from "./StatusLine.jsx";
import TopCategoriesSection from "./TopCategoriesSection.jsx";
import { useSearch } from "../hooks/useSearch.js";
import { useHacksByCategory } from "../hooks/useHacksByCategory.js";
import ErrorBanner from "../../../shared/components/ErrorBanner.jsx";
import DefinitionDialog from "../../../shared/components/DefinitionDialog.jsx";

function SearchPage() {
  const [selectedCategory, setSelectedCategory] = useState(null);
  const [definitionOpen, setDefinitionOpen] = useState(false);

  // Text search hook
  const textSearch = useSearch(10);

  // Category search hook - only active when category is selected
  const categorySearch = useHacksByCategory(selectedCategory, {
    pageSize: 10,
    autoFetch: false,
  });

  // Determine active mode
  const isCategoryMode = !!selectedCategory;

  // Use the appropriate search state
  // Note: textSearch returns 'results', categorySearch returns 'hits'
  const results = isCategoryMode ? categorySearch.hits : textSearch.results;
  const total = isCategoryMode ? categorySearch.total : textSearch.total;
  const page = isCategoryMode ? categorySearch.page : textSearch.page;
  const pageSize = isCategoryMode
    ? categorySearch.pageSize
    : textSearch.pageSize;
  const totalPages = isCategoryMode
    ? categorySearch.totalPages
    : textSearch.totalPages;
  const loading = isCategoryMode ? categorySearch.loading : textSearch.loading;
  const error = isCategoryMode ? categorySearch.error : textSearch.error;

  // Fetch category hacks when category is selected
  useEffect(() => {
    if (selectedCategory) {
      categorySearch.fetchHacks(1, true);
    }
  }, [selectedCategory]);

  const handlePageChange = (_event, newPage) => {
    if (isCategoryMode) {
      categorySearch.goToPage(newPage);
    } else {
      textSearch.search(newPage);
    }
  };

  const handleCategorySearch = (categoryName) => {
    // Clear text search and switch to category mode
    textSearch.setQuery("");
    setSelectedCategory(categoryName);
  };

  const handleTextSearch = () => {
    // Clear category and do text search
    setSelectedCategory(null);
    textSearch.search(1);
  };

  const handleClearCategory = () => {
    setSelectedCategory(null);
  };

  const showCategories =
    !isCategoryMode &&
    !textSearch.query.trim() &&
    textSearch.results.length === 0;

  return (
    <Container maxWidth="md" sx={{ py: 6 }}>
      <Box sx={{ textAlign: "center", mb: 4 }}>
        <Typography
          variant="h3"
          component="h1"
          sx={{
            fontWeight: 600,
            display: "flex",
            alignItems: "center",
            justifyContent: "center",
            mb: 1,
          }}
        >
          <Box
            component="img"
            src="/ikea-logo.jpg"
            alt="IKEA"
            sx={{ height: "1.5em", verticalAlign: "middle", mr: 1 }}
          />
          Hacks Search
        </Typography>
        <Typography variant="subtitle1" color="text.secondary">
          Search across{" "}
          <Link
            variant="subtitle1"
            onClick={() => setDefinitionOpen(true)}
            sx={{
              cursor: "pointer",
              textDecoration: "underline",
              textDecorationStyle: "dotted",
              textUnderlineOffset: 2,
              "&:hover": {
                textDecorationStyle: "solid",
              },
            }}
          >
            IKEA hacks
          </Link>{" "}
          from multiple websites and{" "}
          <Link
            target="_blank"
            rel="noopener noreferrer"
            href="https://www.reddit.com/r/ikeahacks/"
          >
            r/ikeahacks
          </Link>
        </Typography>
      </Box>

      <SearchBar
        query={textSearch.query}
        onQueryChange={textSearch.setQuery}
        onSubmit={handleTextSearch}
        loading={!isCategoryMode && loading}
        disabled={isCategoryMode}
      />

      {isCategoryMode && (
        <Box sx={{ mb: 2, display: "flex", justifyContent: "center" }}>
          <Chip
            label={`Category: ${selectedCategory}`}
            onDelete={handleClearCategory}
            deleteIcon={<CloseIcon />}
            color="primary"
            variant="outlined"
          />
        </Box>
      )}

      <ErrorBanner error={error} />

      <TopCategoriesSection
        show={showCategories}
        onCategorySearch={handleCategorySearch}
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
        query={isCategoryMode ? "" : textSearch.query}
        loading={loading}
        error={error}
        onCategorySearch={handleCategorySearch}
      />

      <PaginationBar
        page={page}
        totalPages={totalPages}
        onChange={handlePageChange}
        disabled={loading}
      />

      <DefinitionDialog
        open={definitionOpen}
        onClose={() => setDefinitionOpen(false)}
      />
    </Container>
  );
}

export default SearchPage;
