from courier.data import load_parcels, build_tracking_index
from courier.parcels import find_parcel, add_parcel, update_parcel, delete_parcel
from courier.auth import setup_staff, login, load_staff, create_token, validate_token, logout, active_tokens

# parcels = load_parcels()

# print(f"{len(parcels)} parcels loaded successfully.")

# tracking_index = build_tracking_index(parcels)

# print(f"{len(tracking_index)} tracking codes indexed.")


# code = input("Enter tracking code : ").strip()
# reply = find_parcel(code, parcels, tracking_index)

# print(reply)

# reply = add_parcel(parcels, tracking_index)

# print(reply)


# reply = find_parcel("SA-TEST001-AA", parcels, tracking_index)

# print(reply)

setup_staff()

staff = load_staff()


print(f"{len(staff)} staff accounts loaded")

username = input("Username: ".strip())
password = input("Password: ").strip()

logged_in_user =  login(username, password, staff)

if logged_in_user:
    token = create_token(logged_in_user)

    # print(
    #     f"200 - Welcome, {logged_in_user["username"]}"
    #     f"({logged_in_user["position"]})."
    # )

    print(f"200 - Login successfully")
    print(f"Your day pass: {token}")


    token_user = validate_token(token)

    if token_user:
        print("200 - Day pass is valid.")
    else:
        print("401 - Your day pass has expired. Please sign in again.")

   
else:
    print("401 - Invalid username or password.")




entered_token = input("Enter your day pass: ").strip()

token_user = validate_token(entered_token)

if token_user:
    print(
        f"200 - Token accepted for "
        f"{token_user["username"]} ({token_user["position"]})"
    )
else:
    print("401- Your day pass is invalid")