# Agentic Sales Outreach System

Autonomous B2B sales assistant with lead generation, research, and personalized email drafting using LangGraph.

## Project Structure

```
project/
├── app/
│   ├── controllers/      # API route handlers
│   ├── models/          # Database models
│   ├── schemas/         # Pydantic schemas
│   ├── services/        # Business logic
│   ├── database/        # Database connections
│   ├── utils/           # Utilities (auth, security)
│   ├── config.py        # Configuration
│   └── main.py          # FastAPI app
├── requirements.txt
├── run.py              # Run script
└── .env                # Environment variables
```

## Setup

1. Create a virtual environment:
```bash
python -m venv venv
source venv/Scripts/activate  # On Windows
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Configure environment:
```bash
cp .env.example .env
# Edit .env and add your API keys and MongoDB URL
```

4. Run MongoDB (if local):
```bash
mongod
```

5. Run the server:
```bash
python run.py
```

Or with uvicorn directly:
```bash
uvicorn app.main:app --reload
```

6. Open your browser at http://127.0.0.1:8000

## API Endpoints

### Authentication
- `POST /api/auth/register` - Register new user
- `POST /api/auth/login` - Login (form data)
- `POST /api/auth/login/json` - Login (JSON)

### Users
- `GET /api/users/me` - Get current user info

### Leads
- `POST /api/leads/` - Create new lead
- `GET /api/leads/` - Get all leads
- `GET /api/leads/{id}` - Get specific lead
- `PATCH /api/leads/{id}` - Update lead
- `DELETE /api/leads/{id}` - Delete lead

## API Documentation

- Interactive docs: http://127.0.0.1:8000/docs
- Alternative docs: http://127.0.0.1:8000/redoc

## Tech Stack

- FastAPI - Web framework
- MongoDB - Database
- Motor - Async MongoDB driver
- JWT - Authentication
- Tavily - Web search
- Firecrawl - Web scraping
- LangGraph - Agent orchestration (coming soon)
