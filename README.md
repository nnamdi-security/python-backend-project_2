# Swift Arrow Couriers  | [![wakatime](https://wakatime.com/badge/user/55f2e7d8-e681-415e-ba87-93dc727f5023/project/0ec0238d-7cf8-4ddd-8c4f-3c4cc8684165.svg)](https://wakatime.com/badge/user/55f2e7d8-e681-415e-ba87-93dc727f5023/project/0ec0238d-7cf8-4ddd-8c4f-3c4cc8684165)

A lightweight Python console application for managing and tracking parcels at scale.

Swift Arrow Couriers was built around a 50,000-record parcel ledger and demonstrates practical backend fundamentals using only core Python: fast indexing, caching, JSON persistence, password hashing, token-based authentication, role-based authorization, and CRUD operations.

The project intentionally avoids frameworks and classes so the underlying logic remains easy to understand and explain.



---

## What the Project Does

Authenticated staff can:

- Track a parcel by tracking code
- Find all parcels going to a destination
- Register new parcels
- Update parcel status
- Delete parcels when authorized
- Sign in once and use a temporary day-pass token
- Reuse recent query results from a small in-memory cache
- Keep parcel changes persistent across restarts

---

## Core Engineering Ideas

### 1. Tracking-code index

Instead of scanning all 50,000 parcels for every lookup, the application builds a dictionary index when it starts.

```python
{
    "SA-1998500-IY": 0,
    "SA-9840186-LA": 1,
    "SA-5271957-FG": 2
}
```

Each tracking code points directly to the parcel's position in the ledger.

This makes:

```text
GET parcel <tracking_code>
```

very fast and allows lookup time to be reported in milliseconds.

---

### 2. Destination index

A second index supports fast destination searches.

```python
{
    "kano": [2, 18, 24, 51],
    "lagos": [5, 11, 37],
    "enugu": [9, 22]
}
```

A query such as:

```text
GET parcels to Kano
```

can therefore jump directly to the matching parcel positions instead of scanning the whole ledger.

---

### 3. 10-entry cache

The application keeps the ten most recently used answers in memory.

Repeated queries can be returned directly from the cache and are marked:

```text
(from the tray)
```

The cache keeps a simple usage order so that when an eleventh answer is added, the oldest one is removed.

---

### 4. Cache invalidation

The project also handles stale-cache problems.

When parcel data changes:

- `POST` clears the affected destination cache
- `PUT` clears the affected parcel and destination caches
- `DELETE` clears the affected parcel and destination caches

This ensures old answers are never served after the underlying data changes.

---

### 5. Password hashing

Readable passwords are not stored in `staff.json`.

During login:

1. The user enters a password
2. The entered password is hashed
3. The new hash is compared with the stored hash
4. Login succeeds only when the hashes match

The application therefore verifies passwords without storing them in readable form.

---

### 6. Day-pass token authentication

After a successful login, the application generates a random token using Python's `secrets` module.

The token represents the authenticated session and stores information such as:

```python
{
    "username": "kemi_dispatch",
    "position": "Clerk",
    "created_at": ...
}
```

Tokens:

- Exist only in memory
- Expire after 5 minutes
- Are destroyed on logout
- Are not written to source-controlled files

---

### 7. Role-based authorization

The application distinguishes between authentication and authorization.

Clerks can perform normal parcel operations, but only the **Station Master** can delete parcels.

A Clerk attempting a delete receives:

```text
403 — Clerks may not delete parcels. Speak to the Station Master.
```

---

## Supported Commands

### Track one parcel

```text
GET parcel <tracking_code>
```

Example:

```text
GET parcel SA-1998500-IY
```

### Find parcels going to a city

```text
GET parcels to <city>
```

Example:

```text
GET parcels to Kano
```

### Register a parcel

```text
POST parcel
```

### Update a parcel

```text
PUT parcel <tracking_code>
```

### Delete a parcel

```text
DELETE parcel <tracking_code>
```

Deletion is restricted to the Station Master.

---

## Response Codes

The console uses API-style response codes:

| Code | Meaning |
|---|---|
| `200` | Request completed successfully |
| `201` | New parcel created successfully |
| `400` | Invalid request or input |
| `401` | Authentication failed or token invalid/expired |
| `403` | Authenticated but not authorized |
| `404` | Parcel or requested resource not found |

---

## Project Structure

```text
swift_arrow/
│
├── main.py
├── parcels.json
├── staff.json
├── README.md
├── README.txt
│
└── courier/
    ├── __init__.py
    ├── data.py
    ├── auth.py
    ├── parcels.py
    └── cache.py
```

### `main.py`

Handles the terminal interface, sign-in flow, token presentation, menu, command parsing, and output.

### `courier/data.py`

Handles:

- Loading parcel data
- Saving parcel data
- Building the tracking-code index
- Building the destination index

### `courier/auth.py`

Handles:

- Password hashing
- Staff loading
- Login
- Token generation
- Token validation
- Token expiry
- Logout

### `courier/parcels.py`

Handles:

- Single-parcel lookup
- Destination lookup
- Parcel creation
- Parcel updates
- Parcel deletion

### `courier/cache.py`

Handles:

- Cached answers
- Cache order
- 10-entry limit
- Cache removal

---

## Technologies Used

- Python 3
- JSON
- `hashlib`
- `secrets`
- `time`
- `os`

No external packages are required.

---

## Running the Project

Clone the repository:

```bash
git clone <your-repository-url>
```

Enter the project directory:

```bash
cd swift_arrow
```

Run:

```bash
python main.py
```

---

## Example Session

```text
==================================================
 SWIFT ARROW COURIERS — TRACKING WINDOW
==================================================

--- THE GRILLE (sign in first) ---

Username: kemi_dispatch
Password: ********

200 — Welcome, kemi_dispatch (Clerk).

Your day pass: <generated-token>
(Show this pass with every slip. It expires in 5 minutes.)

--------------------------------------------------
WINDOW MENU
--------------------------------------------------

1. GET parcel <code>
2. GET parcels to <city>
3. POST parcel
4. PUT parcel <code>
5. DELETE parcel <code>
6. Sign out
7. Close the window

Pass slip: GET parcel SA-1998500-IY
Day pass: <generated-token>

200 — Found in 0.0042 ms

SA-1998500-IY | Danladi Danjuma -> Uche Igwe
Ibadan -> Aba | delivered | 35.3 kg | shipped 2026-08-25
```

A repeated query can be served from the cache:

```text
200 — Found in 0.0011 ms (from the tray)
```

---

## What I Practiced

This project gave me hands-on practice with:

- Dictionary-based indexing
- Secondary indexes
- Caching
- LRU-style cache behavior
- Cache invalidation
- CRUD operations
- JSON persistence
- Password hashing
- Token-based authentication
- Token expiry
- Role-based access control
- Command parsing
- Input validation
- Error handling
- Performance measurement
- Separation of responsibilities across modules

---

## What I Learned

One of the biggest lessons from this project was the difference between making a program work and making it efficient, safe, and maintainable.

I learned how an index and a cache solve different problems:

- An index helps the program find data quickly
- A cache helps the program avoid repeating recently completed work

I also practiced separating authentication from authorization, keeping data persistent without a database, and organizing a small Python project into focused modules.

---

## Possible Improvements

This version intentionally focuses on core Python fundamentals.

Future improvements could include:

- SQLite or PostgreSQL persistence
- Flask, FastAPI, or Django REST API
- Automated tests with `pytest`
- `bcrypt` or Argon2 for production-grade password hashing
- Pagination for large destination results
- Structured logging
- Environment-based configuration
- Docker support
- Web or mobile frontend
- More detailed parcel-history events

---

## Background

This project was originally developed from a software-development assignment for a fictional courier company with a 50,000-parcel ledger.

I used the assignment to practice backend design fundamentals while keeping the implementation intentionally lightweight and understandable.

---

## Author

**Michael Erastus**  
Software Engineer

GitHub: Add your GitHub profile URL  
LinkedIn: Add your LinkedIn profile URL
