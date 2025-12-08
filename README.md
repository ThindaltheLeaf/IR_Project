# IKEA Hacks Search Engine

A full-stack search engine for the project of the course "Information Retrieval" of Università della Svizzera Italiana

The goal was discovering and exploring IKEA hacks from multiple sources including dedicated websites and Reddit's r/ikeahacks community.

## Project Structure

```bash
├── frontend/          # React + Vite frontend application
├── backend/           # FastAPI backend with MongoDB
├── crawler/           # Scrapy web crawlers
└── README.md          # This file
```

## Features

- **Full-text search** across thousands of IKEA hack projects
- **Smart categorization** using LLM-powered tagging
- **Similar hacks** discovery using MongoDB Atlas Search
- **Category browsing** with popular categories
- **Multi-source aggregation** from ikeahackers.net, loveproperty.com, tosize.it, and Reddit
- **Responsive UI** with dark mode support

## Tech Stack

- **Frontend**: React, Material-UI, Vite
- **Backend**: FastAPI, Python 3.x
- **Database**: MongoDB Atlas (with Search indexes)
- **Web Scraping**: Scrapy
- **LLM Tagging**: Ollama (local LLM inference)

## Quick Start

### Prerequisites

- Node.js 18+ and npm
- Python 3.9+
- MongoDB Atlas account
- Ollama (for LLM tagging)

### 1. Clone the repository

```bash
git clone git@github.com:sccjrd/ir-project.git
cd ir-project
```

### 2. Set up the Backend

See the [Backend README](backend/README.md) for detailed setup instructions.

```bash
cd backend
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
pip install -r requirements.txt

# Create .env file with your MongoDB credentials
# See backend/README.md for required environment variables

# Start the server
uvicorn app.main:app --reload
```

Backend runs on `http://localhost:8000`

### 3. Set up the Frontend

See the [Frontend README](frontend/README.md) for detailed setup instructions.

```bash
cd frontend
npm install

# Create .env file with backend URL
# See frontend/README.md for required environment variables

# Start the dev server
npm run dev
```

Frontend runs on `http://localhost:5173`

### 4. Run the Crawler (Optional)

See the [Crawler README](crawler/README.md) for detailed crawler documentation.

```bash
cd crawler
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# Create .env file with MongoDB credentials
# See crawler/README.md for configuration details

# Run all crawlers
python scraper/run_crawlers.py

# Build combined collection
python scraper/build_hacks_all.py
```

### 5. Tokenize Data with LLM (Optional)

See the [Backend README - LLM Tokenization](backend/README.md#llm-tokenization) section for Ollama setup.

```bash
cd backend
python -m app.tokenization.cli --limit 100
```

## Authors

- Sacco Francesc Jordi
- Vavassori Theodor

## License

Academic project for Information Retrieval 2025 course.

---

For detailed setup and usage instructions, please refer to the individual component READMEs:

- [Frontend Setup](frontend/README.md)
- [Backend Setup](backend/README.md)
- [Crawler Setup](crawler/README.md)
