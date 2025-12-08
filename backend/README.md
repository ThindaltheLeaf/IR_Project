# IKEA Hacks Backend

FastAPI-based backend providing search and retrieval APIs for IKEA hack projects.

## Features

- Full-text search with MongoDB Atlas Search
- Similar hacks recommendation using vector similarity
- Category-based browsing
- LLM-powered automatic tagging and categorization


## Setup

### Prerequisites

- Python 3.9+
- MongoDB Atlas account with Search index configured
- Ollama (for LLM tagging)

### Installation

```bash
cd backend
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
````

### Environment Variables

Create a `.env` file:

```env
MONGO_URI=mongodb+srv://username:password@cluster.mongodb.net/
MONGO_DB_NAME=ikea_hacks_ir
MONGO_COLLECTION_NAME=hacks_all
MONGO_SEARCH_INDEX=default
CORS_ALLOW_ORIGINS=http://localhost:5173,http://localhost:3000
```

### MongoDB Atlas Search Index

Create a search index named `default` on the `hacks_all` collection:

```json
{
  "mappings": {
    "dynamic": false,
    "fields": {
      "title": { "type": "string", "analyzer": "lucene.english" },
      "content": { "type": "string", "analyzer": "lucene.english" },
      "excerpt": { "type": "string", "analyzer": "lucene.english" },
      "categories": { "type": "string" },
      "tags": { "type": "string" },
      "author": { "type": "string" },
      "source": { "type": "string" },
      "url": { "type": "string" },
      "image_url": { "type": "string" },
      "date": { "type": "date" }
    }
  }
}
```

## Running

```bash
uvicorn app.main:app --reload
```

Server runs on `http://localhost:8000`

## API Endpoints

### Search

```
GET /api/search?query={query}&page={page}&page_size={size}
```

Search across all IKEA hacks.

### Similar Hacks

```
GET /api/search/similar/{hack_id}?limit={limit}
```

Get similar hacks to a specific hack.

### Top Categories

```
GET /api/search/categories/top?limit={limit}
```

Get most popular categories.

### Category Hacks

```
GET /api/search/categories/{category_name}/hacks?page={page}&page_size={size}
```

Get all hacks in a category.

## LLM Tokenization

The backend includes an LLM-powered tokenization system using Ollama for automatic categorization and tagging.

### Setup Ollama

```bash
# Install Ollama
curl -fsSL https://ollama.com/install.sh | sh

# Pull the model
ollama pull llama3.2:3b
```

### Run Tokenization

```bash
# Process all hacks
python -m app.tokenization.cli

# Process limited number
python -m app.tokenization.cli --limit 100
```

## Project Structure

```
backend/
├── app/
│   ├── core/              # CORS configuration
│   ├── routers/           # API routes
│   ├── services/          # MongoDB connection
│   ├── tokenization/      # LLM tagging system
│   ├── models.py          # Pydantic models
│   ├── utils.py           # Helper functions
│   └── main.py            # FastAPI app
├── requirements.txt
└── .env
```

## API Documentation

Interactive API docs available at:

- Swagger UI: `http://localhost:8000/docs`
