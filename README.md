# API THING
Get stock data with a script and host an API service that can retrieve sets of data to your specifications.

## Developed On
  - OS: Arch Linux
  - **Python Version**: 3.11.2

## Tech Stack
  - FastAPI for framework
  - Async SQLAlchemy for ORM
  - SQLite for database
  - Alembic for migrations
  - Docker Compose for containerization

## Setup
0. Add to `.env` in project root:

```
VANTAGE_API_KEY=YOUR_API_KEY
DATABASE_CONNECTIONSTRING="sqlite+aiosqlite:///database.db"
```

  - Replace YOUR_API_KEY with your own vantage api key
1. Activate venv: `python -m venv venv`
2. `source venv/bin/activate`
    - Mac: probably the same as linux
    - Windows: venv\somewhere in here
3. `pip install -r requirements.txt`
4. Migrate DB: `./rundb migrate`
    - Windows: `bash rundb migrate` (i think windows should have bash now)
5. Get Vantage data: `./get_raw_data.py`
    - Windows: `python get_raw_data.py`
    - Adjust the list of tickers `symbols` in here if different tickers are needed, and `days_back` if a different duration is needed
6. `docker-compose up`
7. Ping the API

## Maintain API key
Add your key in the .env file as `VANTAGE_API_KEY=YOUR_API_KEY`, this is also added to the docker-compose to ensure that the env is there.
The app and docker will throw an error, telling you that the env does not have the required data, if you do not have any of the specified envs anyways.
