from courier.data import load_parcels, build_tracking_index
from courier.parcels import find_parcel, add_parcel, update_parcel, delete_parcel
from courier.auth import setup_staff, login, load_staff

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
    print(
        f"200 - Welcome, {logged_in_user["username"]}"
        f"({logged_in_user["position"]})."
    )
else:
    print("401 - Invalid username or password.")

