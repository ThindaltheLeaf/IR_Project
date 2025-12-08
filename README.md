# IKEA Hacks Search Engine

A full-stack search engine for discovering and exploring IKEA hacks from multiple sources including dedicated websites and Reddit's r/ikeahacks community.

## Project Structure

```
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

```bash
cd backend
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
pip install -r requirements.txt

# Create .env file
cp .env.example .env
# Edit .env with your MongoDB URI and other settings

# Start the server
uvicorn app.main:app --reload
```

Backend runs on `http://localhost:8000`

### 3. Set up the Frontend

```bash
cd frontend
npm install

# Create .env file
cp .env.example .env
# Edit .env with your backend URL

# Start the dev server
npm run dev
```

Frontend runs on `http://localhost:5173`

### 4. Run the Crawler (Optional)

```bash
cd crawler
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# Create .env file with MongoDB credentials
cp .env.example .env

# Run all crawlers
python scraper/run_crawlers.py
```

### 5. Tokenize Data with LLM (Optional)

```bash
cd backend
python -m app.tokenization.cli --limit 100
```


## Authors

- Sacco Francesc Jordi 
- Vavassori Theodor 


