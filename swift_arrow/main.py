from courier.data import load_parcels, build_tracking_index
from courier.parcels import find_parcel, add_parcel, update_parcel, delete_parcel

parcels = load_parcels()

print(f"{len(parcels)} parcels loaded successfully.")

tracking_index = build_tracking_index(parcels)

print(f"{len(tracking_index)} tracking codes indexed.")


code = input("Enter tracking code : ").strip()
reply = find_parcel(code, parcels, tracking_index)

print(reply)

# reply = add_parcel(parcels, tracking_index)

# print(reply)


# reply = find_parcel("SA-TEST001-AA", parcels, tracking_index)

# print(reply)


