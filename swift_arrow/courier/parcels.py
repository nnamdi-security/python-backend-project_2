import time
from courier.data import save_parcels

def find_parcel(code, parcels, tracking_index):
    start_time = time.perf_counter()

    if code not in tracking_index:
        end_time = time.perf_counter()
        time_taken = (end_time - start_time) * 1000

        return f"404 - There is no parcel {code}. Search took {time_taken:.4f} ms"

    position = tracking_index[code]
    parcel = parcels[position]

    end_time = time.perf_counter()
    time_taken = (end_time - start_time) * 1000

    return (
        f"200 - Found in {time_taken:.4f} ms\n"
        f"{parcel["tracking_code"]} | "
        f"{parcel["sender"]} -> {parcel["receiver"]}\n"
        f"{parcel["origin"]} -> {parcel["destination"]} | "
        f"{parcel["status"]} | "
        f"{parcel["weight_kg"]} kg | "
        f" shipped {parcel["date_shipped"]}"
    )



def add_parcel(parcels, tracking_index):
    print("\n--- Register New Parcel")

    tracking_code = input("Enter the percel tracking code: ").strip()

    if tracking_code == "":
        return "400 - Tracking code cannot be empty"

    if tracking_code in tracking_index:
        return f"400 - Parcel {tracking_code} already exists."

    sender = input("Enter sender's name: ").strip()
    receiver = input("Enter receiver's name ").strip()
    origin = input("Enter parcel's origin: ").strip()
    destination = input("Enter parcel's destination: ").strip()
    status = input("Enter parcel's status: ").strip()
    weight_input = input("Enter parcel's weight in kg: ").strip()
    date_shipped = input("Enter date shipped (YYYY-MM-DD): ").strip()

    if (
        sender == ""
        or receiver == ""
        or origin == ""
        or destination == ""
        or status == ""
        or weight_input == ""
        or date_shipped == ""
    ):
        return "400 - All parcels details are required."

    try:
        weight_kg = float(weight_input)

    except ValueError:
        return "400 -  Weight must be a number."

    new_parcel = {
        "tracking_code": tracking_code,
        "sender": sender,
        "receiver": receiver,
        "origin": origin,
        "destination": destination,
        "status": status,
        "weight_kg": weight_kg,
        "date_shipped": date_shipped
    }

    parcels.append(new_parcel)

    position = len(parcels) - 1
    tracking_index[tracking_code] = position

    saved = save_parcels(parcels)

    if not saved:
        parcels.pop()
        del tracking_index[tracking_code]

        return "400 - Parcel could not be saved."

    return f"201 - Parcel {tracking_code} registered successfully."



def update_parcel(code, parcels, tracking_index):
    if code not in tracking_index:
        return f"404 - There is no parcel {code}."

    position = tracking_index[code]
    parcel = parcels[position]

    print("\n--- Update Parcel ---")
    print(f"Tracking code: {parcel["tracking_code"]}")
    print(f"Current status: {parcel["status"]}")

    new_status = input("New status: ").strip()

    if new_status == "":
        return "400 - status cannot be empty."
    
    old_status = parcel["status"]

    parcel["status"] = new_status

    saved = save_parcels(parcels)

    if not saved:
        parcel["status"] = old_status
        return "400 - Parcel could not be updated"

    return f"200 - Parcel {code} updated successfully."


def delete_parcel(code, role, parcels, tracking_index):
    if role != "Station Master":
        return "403 - Clerks may not delete parcels. Speak to the Station Master."

    if code not in tracking_index:
        return f"404 - There is no parcel {code}"

    position = tracking_index[code]
    deleted_parcel = parcels.pop(position)
    saved = save_parcels(parcels)

    if not saved:
        parcels.insert(position, deleted_parcel)
        return "400 - Parcel could not be deleted."

    tracking_index.clear()

    for new_position in range(len(parcels)):
        tracking_code = parcels[new_position]["tracking_code"]
        tracking_index[tracking_code] = new_position

    return f"200 - Parcel {code} deleted successfully"

