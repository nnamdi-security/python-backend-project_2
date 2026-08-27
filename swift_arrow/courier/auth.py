import json
import hashlib
import os
import secrets
import time

STAFF_FILE = "staff.json"


# default_staff = [
#     {
#         "username": "oga_musty",
#         "password": "stationmaster1",
#         "position": "Station Master"
#     },
#     {
#         "username": "kemi_dispatch",
#         "password": "parcels4kemi",
#         "position": "Clerk"
#     },
#     {
#         "username": "ibrahim_k",
#         "password": "fastdelivery",
#         "position": "Clerk"
#     },
#     {
#         "username": "ngozi_front",
#         "password": "desk2026",
#         "position": "Clerk"
#     }
# ]


default_staff = [
    {
        "username": "oga_musty",
        "password_hash": "bcd2e1bed4c03318d006c0b08e017245b679aa7266dff2b7cd6fa55056225f0d",
        "position": "Station Master"
    },
    {
        "username": "kemi_dispatch",
        "password_hash": "f75df730688b9583f7fce182caaa7dedd0dc2e0e740f0daf18852208fc6d14ab",
        "position": "Clerk"
    },
    {
        "username": "ibrahim_k",
        "password_hash": "9d6abb3a1de292f015e81db73c17528c3535639021c8001b91903ea0d5801805",
        "position": "Clerk"
    },
    {
        "username": "ngozi_front",
        "password_hash": "bb56acd76a29825a57eac35cacdf947e130bdeb99245d8dee914537e7eeda287",
        "position": "Clerk"
    }
]


def hash_password(password):
    password_bytes = password.encode("utf-8")

    hashed_password = hashlib.sha256(password_bytes).hexdigest()

    return hashed_password


# def setup_staff():
#     if os.path.exists(STAFF_FILE):
#         return

#     staff_to_save = []

#     for staff in default_staff:
#         hashed_staff = {
#             "username": staff["username"],
#             "password_hash": hash_password(staff["password"]),
#             "position": staff["position"]
#         }

#         staff_to_save.append(hashed_staff)

#     with open(STAFF_FILE, "w") as file:
#         return json.dump(staff_to_save, file, indent=4)

def setup_staff():
    if os.path.exists(STAFF_FILE):
        return

    with open(STAFF_FILE, "w") as file:
        json.dump(default_staff, file, indent=4)


def load_staff():
    try:
        with open(STAFF_FILE, "r") as file:
            staff = json.load(file)
            return staff

    except FileNotFoundError:
        return []


def login(username, password, staff):
    password_hash = hash_password(password)

    for staff_member in staff:
        if staff_member["username"] == username:
            if staff_member["password_hash"] == password_hash:
                return staff_member

            return None
        
    return None


active_tokens = {}

def create_token(staff_member):
    token = secrets.token_urlsafe(24)

    active_tokens[token] = {
        "username": staff_member["username"],
        "position": staff_member["position"],
        "created_at": time.time()
    }

    return token






def validate_token(token):
    if token not in active_tokens:
        return None

    token_data = active_tokens[token]

    current_time = time.time()

    token_age = current_time - token_data["created_at"]

    if token_age > 300:
        del active_tokens[token]
        return None

    return token_data



def logout(token):
    if token in active_tokens:
        return True

    return False


