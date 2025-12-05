import { useState } from "react";
import {
  Box,
  Button,
  Accordion,
  AccordionSummary,
  AccordionDetails,
  Typography,
} from "@mui/material";

import ExpandMoreIcon from "@mui/icons-material/ExpandMore";

function SearchTags({ categories, onCategorySearch }) {
  const [expanded, setExpanded] = useState(false);

  const handleChange = (_event, isExpanded) => {
    setExpanded(isExpanded);
  };

  const handleCategoryClick = (category) => {
    const searchQuery = `${category}`;
    onCategorySearch(searchQuery);
  };

  return (
    <Accordion
      expanded={expanded}
      onChange={handleChange}
      sx={{ mt: 1.5, boxShadow: "none" }}
    >
      <AccordionSummary expandIcon={<ExpandMoreIcon />}>
        <Typography variant="body2" sx={{ fontWeight: 500 }}>
          Show categories
        </Typography>
      </AccordionSummary>
      <AccordionDetails>
        <Box sx={{ display: "flex", gap: 1, flexWrap: "wrap" }}>
          {categories.map((category) => (
            <Button
              key={category}
              size="small"
              variant="outlined"
              disableElevation
              onClick={() => handleCategoryClick(category)}
              sx={{
                borderRadius: "999px",
                textTransform: "uppercase",
                fontWeight: 500,
                letterSpacing: 0.5,
                paddingX: 1.5,
                cursor: "pointer",
                "&:hover": {
                  backgroundColor: "primary.main",
                  color: "white",
                },
              }}
            >
              {category}
            </Button>
          ))}
        </Box>
      </AccordionDetails>
    </Accordion>
  );
}

export default SearchTags;
