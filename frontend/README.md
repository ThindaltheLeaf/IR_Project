# IKEA Hacks Frontend

React-based frontend for searching and browsing IKEA hack projects.

## Features

- Material-UI components with custom theming
- Real-time search with pagination
- Category browsing
- Similar hacks discovery

## Setup

### Prerequisites

- Node.js 18+
- npm or yarn

### Installation

```bash
cd frontend
npm install
````

### Environment Variables

Create a `.env` file:

```env
VITE_API_BASE_URL=backend_port
```

## Running

```bash
# Development server
npm run dev

# Build for production
npm run build

# Preview production build
npm run serve
```

Dev server runs on `http://localhost:5173`

## Project Structure

```
frontend/
├── src/
│   ├── app/                    # Main app component
│   ├── features/
│   │   └── search/             # Search feature module
│   │       ├── api/            # API client functions
│   │       ├── components/     # React components
│   │       └── hooks/          # Custom React hooks
│   ├── lib/
│   │   └── apiClient.js        # Base API client
│   ├── shared/
│   │   └── components/         # Shared components
│   ├── main.jsx                # App entry point
│   └── theme.js                # MUI theme configuration
├── public/                      # Static assets
├── index.html
├── package.json
└── vite.config.js
```

## Key Components

### Search Components

- SearchPage.jsx - Main search page with state management
- SearchBar.jsx - Search input with loading state
- SearchResultList.jsx - List of search results
- SearchResultCard.jsx - Individual result card with highlighting
- TopCategoriesSection.jsx - Top 8 categories display
- PaginationBar.jsx - Page navigation
- SimilarHacksAccordion.jsx - Similar hacks for each result
- SearchTags.jsx - Category tags for each result

### Shared Components

- Header.jsx - App header with theme toggle
- Footer.jsx - App footer
- DefinitionDialog.jsx - IKEA hacks explanation dialog
- ErrorBanner.jsx - Just for error display

## Custom Hooks

- `useSearch` - Text search functionality
- `useHacksByCategory` - Category-based search
- `useSimilar` - Similar hacks discovery
- `useTopCategories` - Popular categories

## API Integration

All API calls go through `apiClient.js` which handles:

- Base URL configuration
- Request/response formatting
- Error handling

## Styling

Uses Material-UI with custom theme defined in `theme.js`:

- Noto Sans font family
- Custom color palette
- Dark/light mode support
- Persistent theme preference (localStorage)

## Building for Production

```bash
npm run build
```
