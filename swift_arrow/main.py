from courier.data import load_parcels, build_tracking_index, build_destination_index
from courier.parcels import find_parcel, add_parcel, update_parcel, delete_parcel
from courier.auth import setup_staff, login, load_staff, create_token, validate_token, logout



# #----------------------
# # LOAD PROGRAM DATA
# #----------------------


# setup_staff()

# staff = load_staff()
# parcels = load_parcels()
# tracking_index = build_tracking_index(parcels)


# #-----------------------
# # SIGN IN
# #-----------------------

# print("=" * 50)
# print(" SWIFT ARROW CAOURIERS - TRACKING WINDOW ")
# print("=" * 50)

# print("\n--- THE GRILLE (sign in first) ---")

# username = input("Enter Username: ").strip()
# password = input("Enter password: ").strip()

# logged_in_user = login(username, password, staff)

# if not logged_in_user:
#     print("401 - Invalid username or password")

# else:
#     token = create_token(logged_in_user)

#     print(
#         f"\n200 - Welcome, {logged_in_user["username"]} "
#         f"({logged_in_user["position"]})."
#     )

#     print(f"Your day pass: {token}")
#     print("Show this pass with every slip. It expires in 5 minutes")


#     #-----------------
#     # WINDOW LOOP
#     #-----------------

#     while True:
#         print("\n" + "-" * 50)
#         print("WINDOW MENU")
#         print("-" * 50)

#         print("1. GET parcel <code>")
#         print("2. POST parcel")
#         print("3. PUT parcel <code>")
#         print("4. DELETE parcel <code>")
#         print("5. sign out")
#         print("6. Close the window")

#         print("-" * 50)

#         slip = input("Pass slip: ").strip()

#         if slip == "":
#             print("400 - Empty slips cannot be processed.")
#             continue

#         #------------------
#         # SIGN OUT
#         #------------------

#         if slip.lower() == "sign out" or slip == "5":
#             logout(token)

#             print("200 - Signed out successfully")
#             break

#         #------------------
#         # CLOSE WINDOW
#         #------------------

#         if slip.lower() == "close" or slip == "6":
#             print("200 - Tracking window closed")
#             break


#         #------------------
#         # ASK FOR DAY PASS
#         #------------------

#         entered_token = input("Enter your day pass: ").strip()

#         token_user = validate_token(entered_token)

#         if not token_user:
#             print("401 - Invalid or expired day pass.")
#             continue

#         #-------------------
#         # GET PARCEL
#         #-------------------

#         if slip.lower().startswith("get parcel "):

#             parts = slip.split()

#             if len(parts) != 3:
#                 print('400 - Use: GET parcel <tracking_code>')
#                 continue

#             code = parts[2]

#             reply = find_parcel(code, parcels, tracking_index)

#             print(reply)


#         #-------------------
#         # POST PERCEL
#         #-------------------

#         elif slip.lower() == "post parcel":
#             reply = add_parcel(parcels, tracking_index)

#             print(reply)


#         #-------------------
#         # PUT PARCEL
#         #-------------------

#         elif slip.lower().startswith("put parcel "):

#             parts = slip.split()

#             if len(parts) != 3:
#                 print("400 - Use: PUT parcel <tracking_code>")
#                 continue

#             code = parts[2]

#             reply = update_parcel(code, parcels, tracking_index)

#             print(reply)


#         #----------------------
#         # DELETE PARCEL
#         #----------------------

#         elif slip.lower().startswith("delete parcel "):
#             parts = slip.split()

#             if len(parts) != 3:
#                 print("400 - USE: DELETE parcels <tracking_code>")
#                 continue

#             code = parts[2]

#             reply = delete_parcel(code, token_user, parcels, tracking_index)

#             print(reply)



#         #---------------------
#         # NUMBERED SHORTCUT
#         #---------------------

#         elif slip == "1":
#             code = input("Enter tracking code: ").strip()

#             reply = find_parcel(code, parcels, tracking_index)

#             print(reply)

#         elif slip == "2":

#             reply = add_parcel(parcels, tracking_index)

#             print(reply)

#         elif slip == "3":

#             code = input("Enter trackig code to update: ").strip()

#             reply = update_parcel(code, parcels, tracking_index)

#             print(reply)

#         elif slip == "4":

#             code = input("Enter tracking code to delete: ").strip()

#             reply = delete_parcel(code, token_user, parcels, tracking_index)

#             print(reply)


#         #------------------
#         # INVALID SLIP
#         #------------------

#         else:
#             print(
#                 "400 - I cannot read this slip. "
#                 "The verbs are GET, POST, PUT, DELETE."
#             )




parcels = load_parcels()

tracking_index = build_tracking_index(parcels)
destination_index = build_destination_index(parcels)
