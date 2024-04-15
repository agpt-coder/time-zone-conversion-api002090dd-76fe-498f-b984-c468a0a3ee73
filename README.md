---
date: 2024-04-15T13:22:16.725929
author: AutoGPT <info@agpt.co>
---

# Time Zone Conversion API

To build a system that accepts a timestamp and its source time zone, then converts it to a specified target time zone while handling Daylight Saving Time (DST) adjustments, and returns the converted timestamp in ISO 8601 format, follow these steps with the specified tech stack:

1. **Programming Language:** Python
- Python is versatile and widely supported, ideal for datetime and timezone manipulations.

2. **API Framework:** FastAPI
- FastAPI will serve as the backend framework to receive timestamp conversion requests via API calls. It's fast, easy to use, and automatically generates interactive API documentation.

3. **Database:** PostgreSQL
- Although this task might not require database storage, PostgreSQL is chosen for potential future enhancements like logging or storing conversion histories.

4. **ORM:** Prisma
- Prisma will manage our PostgreSQL database interactions. Even though it's not essential for the timestamp conversion itself, it's included for potential future database-related features.

**Implementation Steps:**
- Install the required packages (`fastapi`, `uvicorn` for serving the app, `pytz` for timezone handling).

- Define a FastAPI endpoint to accept `timestamp`, `source timezone`, and `target timezone` as input. Ensure inputs are validated.

- Use Python's `datetime` and `pytz` libraries to handle the actual conversion:
  - Parse the input timestamp and source timezone.
  - Localize the timestamp to the source timezone making it aware.
  - Convert the aware timestamp to the target timezone.
  - Apply DST adjustments automatically with `pytz`'s transition rules.
  - Format the converted timestamp into ISO 8601 format using `datetime.isoformat()`.

- Return the converted timestamp in ISO format as the API response.

Here's a simplified Python snippet representing the core functionality:

```python
from fastapi import FastAPI
from datetime import datetime
import pytz

app = FastAPI()

@app.post('/convert-timestamp/')
def convert_timestamp(source_timestamp: str, source_tz: str, target_tz: str):
    # Parse the timestamp
    dt = datetime.fromisoformat(source_timestamp)
    # Localize to source timezone
    source_timezone = pytz.timezone(source_tz)
    dt_source_tz = source_timezone.localize(dt)
    # Convert to target timezone
    target_timezone = pytz.timezone(target_tz)
    dt_target_tz = dt_source_tz.astimezone(target_timezone)
    # Return the converted timestamp in ISO 8601 format
    return {'converted_timestamp': dt_target_tz.isoformat()}
```

- To serve the FastAPI app, run `uvicorn main:app --reload` where `main` is the file name.

This setup accomplishes the task of converting timestamps between time zones with DST adjustment and returns the converted timestamp in ISO 8601 format.

## What you'll need to run this
* An unzipper (usually shipped with your OS)
* A text editor
* A terminal
* Docker
  > Docker is only needed to run a Postgres database. If you want to connect to your own
  > Postgres instance, you may not have to follow the steps below to the letter.


## How to run 'Time Zone Conversion API'

1. Unpack the ZIP file containing this package

2. Adjust the values in `.env` as you see fit.

3. Open a terminal in the folder containing this README and run the following commands:

    1. `poetry install` - install dependencies for the app

    2. `docker-compose up -d` - start the postgres database

    3. `prisma generate` - generate the database client for the app

    4. `prisma db push` - set up the database schema, creating the necessary tables etc.

4. Run `uvicorn project.server:app --reload` to start the app

## How to deploy on your own GCP account
1. Set up a GCP account
2. Create secrets: GCP_EMAIL (service account email), GCP_CREDENTIALS (service account key), GCP_PROJECT, GCP_APPLICATION (app name)
3. Ensure service account has following permissions: 
    Cloud Build Editor
    Cloud Build Service Account
    Cloud Run Developer
    Service Account User
    Service Usage Consumer
    Storage Object Viewer
4. Remove on: workflow, uncomment on: push (lines 2-6)
5. Push to master branch to trigger workflow
