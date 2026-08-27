import json

FILE_PATH = "C:/Users/ILEH/Documents/GITHUB/python-backend-project_2/swift_arrow/parcels.json"
def load_parcels():
    try:
        with open(FILE_PATH, "r") as file:
            parcels = json.load(file)

            return parcels

    except FileNotFoundError:
        print("parcels.json was not found.")
        return []

    except json.JSONDecodeError:
        print("parcels.json contain invalid JSON")
        return []


def save_parcels(parcels):
    try:
        with open(FILE_PATH, "w") as file:
            json.dump(parcels, file, indent=4)
        return True                             # This means saving worked

    except Exception:
        print("Could not save parcels.")
        return False


def build_tracking_index(parcels):
    index = {}

    for position in range(len(parcels)):
        parcel = parcels[position]
        tracking_code = parcel["tracking_code"]

        index[tracking_code] = position

    return index


def build_destination_index(parcels):
    destination_index = {}

    for position in range(len(parcels)):
        parcel = parcels[position]
        destination = parcel["destination"]

        if destination not in destination_index:
            destination_index[destination] = []

        destination_index[destination].append(position)

    return destination_index





