SWIFT ARROW COURIERS — TRACKING WINDOW
======================================

PROJECT OVERVIEW
----------------

This project is a simple Python console application for Swift Arrow Couriers.

It manages a ledger containing parcel records and allows authorised staff members to:

1. Find a parcel using its tracking code.
2. Find parcels going to a particular destination.
3. Register a new parcel.
4. Update an existing parcel.
5. Delete a parcel.
6. Sign in using a username and password.
7. Receive and use a temporary day pass after signing in.
8. Sign out and destroy the day pass.

The project was built using simple Python functions, dictionaries, lists, JSON files and built-in Python modules.

No classes or external frameworks are used.


PROJECT STRUCTURE
-----------------

The project is organised into separate rooms/modules so that each part of the program has a clear responsibility.

The main structure is:

swift_arrow/
|
|-- main.py
|-- parcels.json
|-- staff.json
|-- README.txt
|
`-- courier/
    |-- __init__.py
    |-- data.py
    |-- auth.py
    |-- parcels.py
    `-- cache.py


WHAT EACH ROOM DOES
-------------------

1. main.py

main.py is the tracking window.

It is responsible for interacting with the user.

It:

- starts the program,
- loads the required data,
- asks staff members to sign in,
- displays the day pass,
- shows the tracking-window menu,
- receives slips from the user,
- checks the day pass,
- sends the request to the correct function,
- and prints the reply.

Most of the actual parcel, authentication and cache logic is kept outside main.py.


2. courier/data.py

data.py handles the parcel ledger and indexes.

It is responsible for:

- loading parcels from parcels.json,
- saving parcels back to parcels.json,
- building the tracking-code index,
- and building the destination index.

This room is what connects the program to the permanent parcel data.


3. courier/auth.py

auth.py handles staff authentication.

It is responsible for:

- password hashing,
- loading the staff register,
- checking usernames and passwords,
- generating day passes,
- validating day passes,
- checking the five-minute expiry,
- and signing staff members out.

The day passes are kept only in memory and are not written to a file.


4. courier/parcels.py

parcels.py contains the main parcel operations.

It handles:

- GET parcel <code>
- GET parcels to <city>
- POST parcel
- PUT parcel <code>
- DELETE parcel <code>

It also works with the indexes, persistence system and cache where necessary.


5. courier/cache.py

cache.py is the tray.

It stores the ten most recently used answers.

If the same question is asked again while its answer is still in the tray, the saved answer is returned instead of rebuilding it.

The cache also keeps track of which answer is the oldest so that the oldest answer can be removed when the tray contains more than ten entries.


HOW TO RUN THE PROGRAM
----------------------

Python 3 is required.

The program should be run from the root of the project folder.

For example:

python main.py

The parcels.json file must be in the project root.

On startup, the program loads the parcel ledger, builds the required indexes and prepares the staff authentication system.

The user is then asked to sign in.

Example:

Username: kemi_dispatch
Password: parcels4kemi

After a successful login, the program gives the user a day pass.

Example:

200 — Welcome, kemi_dispatch (Clerk).
Your day pass: <generated token>

The day pass must then be presented when making parcel requests.


STAFF ACCOUNTS
--------------

The supplied staff accounts have the following usernames:

oga_musty       - Station Master
kemi_dispatch   - Clerk
ibrahim_k       - Clerk
ngozi_front     - Clerk

Readable passwords are not stored in staff.json.

Only password hashes are stored.


PASSWORD HASHING
----------------

A password should not be stored in a form that somebody can simply open and read.

For that reason, this project uses hashing.

When a password is hashed, Python produces a fingerprint of that password.

For example, instead of storing:

password: mypassword

the program stores something similar to:

password_hash: 8f14e45f...

When a staff member signs in, the program does not try to recover the original password from the stored hash.

Instead:

1. The user enters a password.
2. The entered password is hashed.
3. The new hash is compared with the stored hash.
4. If the hashes match, the password is accepted.
5. If they do not match, login is rejected.

This means the program can verify the password without needing to store a readable copy of it.

Hashing is suitable for this job because the same input produces the same fingerprint, making comparison possible, while the original value does not need to be recovered.


THE DIFFERENT JOBS OF HASHING
-----------------------------

Hashing in this project is mainly used to protect staff passwords.

Its job is to turn the password into a fingerprint that can be stored and compared safely.

The important idea is that we compare fingerprints rather than readable secret values.

This same general idea is useful whenever a program needs a repeatable representation of some information without needing to recover the original secret from that representation.

In this project, passwords demonstrate that use directly.


THE TRACKING-CODE INDEX
-----------------------

The parcels.json ledger contains a very large number of parcels.

Searching for one parcel by looping through every parcel each time would become slower as the ledger grows.

To solve this, the program builds a tracking-code index when it starts.

The index works like a notebook.

For example:

{
    "SA-1998500-IY": 0,
    "SA-9840186-LA": 1,
    "SA-5271957-FG": 2
}

The tracking code is the key and the number is the parcel's position in the parcel list.

When a customer asks for:

GET parcel SA-1998500-IY

the program does not read through all 50,000 parcels.

It uses the tracking code to get the parcel position directly from the index, then retrieves that parcel.

This makes parcel lookup extremely fast.

The program also measures the lookup using time.perf_counter() and reports the result in milliseconds.


THE DESTINATION INDEX
---------------------

A second index is used for destination searches.

For example:

{
    "kano": [2, 7, 21, 43],
    "lagos": [1, 9, 18],
    "enugu": [6, 14]
}

Each destination points to the positions of parcels going to that city.

Therefore:

GET parcels to Kano

does not require the program to inspect all 50,000 parcels one by one.

The destination index immediately tells the program which parcel positions belong to Kano.


THE CACHE / TRAY
----------------

The cache solves a different problem from the indexes.

Indexes make finding data fast.

The cache avoids doing the same work again when an answer was recently calculated.

For example, a customer may ask:

GET parcels to Kano

and shortly afterwards ask the exact same question again.

After the first request, the answer is stored in the tray.

The second request can therefore return the stored answer and include:

(from the tray)

The tray keeps only ten recent answers.

When an eleventh different answer is added, the oldest answer is removed.


INDEX VS CACHE
--------------

The index and cache solve different problems.

The index answers:

"Where is the information?"

It helps the program locate records quickly.

The cache answers:

"Have I already calculated this answer recently?"

It allows the program to reuse a recent result.

A request can therefore miss the cache but still be fast because it uses an index.


STALE CACHE PREVENTION
----------------------

Cached information can become incorrect when parcel data changes.

For example:

1. A parcel has status "in transit".
2. GET parcel <code> stores that answer in the tray.
3. PUT parcel <code> changes the status to "delivered".
4. The old cached answer still says "in transit".

Returning the old answer would be incorrect.

For this reason, the program removes affected cache entries after successful changes.

PUT removes the cached parcel answer and the affected destination answer.

POST removes the affected destination answer because the city now has another parcel.

DELETE removes both the parcel answer and the affected destination answer.

The next GET therefore calculates a fresh answer before caching it again.


DAY-PASS / TOKEN SIGN-IN
------------------------

The program does not require staff members to enter their password for every operation.

A staff member signs in once using a username and password.

After successful login, the program creates a random day pass using Python's secrets module.

The pass is stored in memory with information about the staff member.

For example, internally the program may associate a pass with:

{
    "username": "kemi_dispatch",
    "position": "Clerk",
    "created_at": ...
}

When a slip is submitted, the pass is checked.

If the pass does not exist, the program returns:

401 — Invalid or expired day pass.

A pass expires five minutes after it is created.

Five minutes equals 300 seconds.

The program compares the current time with the time at which the token was created.

If the token is older than 300 seconds, it is deleted and the request receives a 401 reply.

Signing out also deletes the token immediately.

Day passes are not saved in a JSON file and are not intended to be pushed to GitHub.


AUTHENTICATION AND AUTHORISATION
--------------------------------

Authentication answers:

"Who are you?"

A correct username, password and valid day pass establish the staff member's identity.

Authorisation answers:

"What are you allowed to do?"

Both Clerks and the Station Master may perform normal parcel operations.

DELETE is restricted to the Station Master.

If a Clerk tries to delete a parcel, the program returns:

403 — Clerks may not delete parcels. Speak to the Station Master.

A missing, forged or expired pass instead results in:

401.


STATUS CODES
------------

Every response begins with a status code.

The program uses:

200 - Successful request

201 - A new parcel was successfully created

400 - The request or supplied data is invalid

401 - Authentication failed, or the day pass is invalid or expired

403 - The user is authenticated but does not have permission

404 - The requested parcel or resource could not be found


SUPPORTED PARCEL OPERATIONS
---------------------------

GET parcel <code>

Finds one parcel using the tracking-code index.

Example:

GET parcel SA-1998500-IY


GET parcels to <city>

Finds parcels going to a destination using the destination index.

Example:

GET parcels to Kano


POST parcel

Registers a new parcel.

The program asks for the parcel details and saves them into parcels.json.

The tracking and destination indexes are updated so the parcel can be found immediately.


PUT parcel <code>

Updates the status of an existing parcel.

The updated information is written back to parcels.json.

Affected cached answers are removed so stale information is not returned.


DELETE parcel <code>

Deletes an existing parcel.

Only the Station Master may perform this operation.

The parcel is removed from the ledger and the indexes are rebuilt.

Affected cached answers are also removed.


DATA PERSISTENCE
----------------

Changes made to parcels are not kept only in memory.

POST, PUT and DELETE write the changed parcel list back into parcels.json.

This means changes survive when the program is closed and started again.


WHAT HAPPENS FROM THE MOMENT A SLIP ARRIVES
-------------------------------------------

The complete flow of a normal parcel request is:

1. The staff member first signs in using a username and password.

2. The entered password is hashed.

3. The hash is compared with the hash stored for that staff member.

4. If login succeeds, the program creates an unguessable day pass.

5. The staff member submits a slip such as:

   GET parcel SA-1998500-IY

6. The staff member presents the day pass.

7. The program checks whether the pass exists.

8. The program checks whether the pass has expired.

9. If the pass is invalid or expired, the request stops and a 401 reply is returned.

10. If the pass is valid, the program determines which command was requested.

11. For a GET request, the program first checks the tray/cache.

12. If the answer is already in the tray, the cached answer is returned and marked:

    (from the tray)

13. If the answer is not cached, the correct index is used.

14. A single parcel uses the tracking-code index.

15. A destination query uses the destination index.

16. The required parcel data is obtained.

17. The program measures the operation time in milliseconds.

18. A successful GET answer is placed into the cache for possible reuse.

19. The program builds the final reply.

20. The reply begins with the appropriate status code.

21. main.py prints the reply at the tracking window.

For POST, PUT and DELETE requests, the relevant parcel operation is performed and the changed parcel list is saved back into parcels.json.

If the change makes any cached answer stale, that cached answer is removed.


WHY THE PROGRAM USES SEPARATE ROOMS
-----------------------------------

The project is divided into modules so that each file has one main responsibility.

main.py handles the window.

data.py handles data and indexes.

auth.py handles passwords, login and day passes.

parcels.py handles parcel operations.

cache.py handles recently used answers.

This makes the project easier to understand, test and maintain than placing the whole program in one large file.


SECURITY NOTE
-------------

The project does not intentionally store active day passes in a file.

Active passes exist only while the Python program is running.

Readable staff passwords are not stored in staff.json.

The stored staff records contain password hashes instead.


END
