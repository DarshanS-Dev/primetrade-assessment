# Primetrade Assessment
 
A scalable REST API with JWT authentication, role-based access control, and a crypto watchlist feature. Built with FastAPI and async PostgreSQL.
 
## Tech Stack
 
- FastAPI (async)
- PostgreSQL via SQLAlchemy 2.0 async
- Alembic for migrations
- pydantic-settings for config
- python-jose for JWT
- passlib[bcrypt] for password hashing
- httpx for CoinGecko live price integration
## Project Structure
 
```
app/
  routers/
    auth.py
    watchlist.py
  models.py
  schemas.py
  database.py
  config.py
  auth.py
main.py
alembic/
.env
requirements.txt
```
 
## Getting Started
 
### 1. Clone the repo
 
```bash
git clone https://github.com/yourusername/primetrade-assessment.git
cd primetrade-assessment
```
 
### 2. Create a virtual environment
 
```bash
python -m venv venv
source venv/bin/activate
```
 
### 3. Install dependencies
 
```bash
pip install -r requirements.txt
```
 
### 4. Set up environment variables
 
Create a `.env` file in the root:
 
```env
DATABASE_URL=postgresql+asyncpg://user:password@localhost:5432/primetrade
SECRET_KEY=your-secret-key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```
 
### 5. Run migrations
 
```bash
alembic upgrade head
```
 
### 6. Start the server
 
```bash
uvicorn main:app --reload
```
 
API is available at `http://localhost:8000`
Swagger docs at `http://localhost:8000/docs`
 
## API Reference
 
### Auth
 
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | /api/v1/auth/register | Register a new user |
| POST | /api/v1/auth/login | Login and receive JWT token |
 
### Watchlist (authenticated)
 
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | /api/v1/watchlist | Add a crypto symbol |
| GET | /api/v1/watchlist | Get your watchlist with live prices |
| PUT | /api/v1/watchlist/{item_id} | Update a symbol |
| DELETE | /api/v1/watchlist/{item_id} | Delete a symbol |
 
### Admin only
 
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | /api/v1/admin/watchlist | Get all users' watchlists |
 
## Authentication Flow
 
1. Register via `/auth/register`
2. Login via `/auth/login` to receive a JWT access token
3. Pass the token in the `Authorization` header as `Bearer <token>` on all protected routes
## Role-Based Access
 
There are two roles: `user` and `admin`.
 
Users can only read, create, update, and delete their own watchlist items. Admin accounts can call `/admin/watchlist` to see every item across all users. The `is_admin` flag is set directly in the database.
 
## Live Price Integration
 
Watchlist responses include real-time prices fetched from the CoinGecko public API via `httpx`. Prices are fetched asynchronously and appended to each symbol in the response.
 
## Scalability Notes
 
**Stateless JWT auth** means any number of API server instances can verify tokens without sharing session state. Horizontal scaling requires no sticky sessions.
 
**Async throughout** means the server does not block on I/O. Database queries and external HTTP calls (CoinGecko) are all awaited, so a single worker handles many concurrent requests efficiently.
 
**Separation of concerns** is maintained across routers, models, schemas, and auth utilities. Adding new entities or endpoints does not require touching existing logic.
 
**Database indexing** on frequently queried columns (user_id on watchlist_items) keeps query performance stable as data grows.
 
**Alembic migrations** version-control the schema, making it safe to evolve the database in production without data loss.