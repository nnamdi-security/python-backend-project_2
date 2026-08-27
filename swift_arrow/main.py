from courier.data import load_parcels, build_tracking_index
from courier.parcels import find_parcel, add_parcel, update_parcel, delete_parcel
from courier.auth import setup_staff, login, load_staff, create_token, validate_token, logout, active_tokens



setup_staff()

staff = load_staff()

parcels = load_parcels()

tracking_index = build_tracking_index(parcels)

print(f"{len(staff)} staff accounts loaded")

username = input("Username: ".strip())
password = input("Password: ").strip()

logged_in_user =  login(username, password, staff)

if not logged_in_user:
    print("401 - Invalid username or password.")

else:
    token = create_token(logged_in_user)

    print(
        f"200 - Welcome, {logged_in_user["username"]} "
        f"({logged_in_user["position"]})."
    )
    print(f"Your day pass: {token}")

    entered_token = input("Enter your day pass: ").strip()

    token_user = validate_token(entered_token)

    if not token_user:
        print("401 - Invalid or expired day pass.")

    else:
        code = input("Enter tracking code to delete: ").strip()

        reply = delete_parcel(code, token_user, parcels, tracking_index)

        print(reply)
