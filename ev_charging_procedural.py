# Name: ANDRIANARIVONY
# First name: NANTENAINA MIALY
# Student ID: 0399103
# ITS72604 Principles of Programming (202609)
# Assessment 1 - Task 2
# Single file procedural Python program


import math

# Global variables
# CONSTANT VARIABLES
# These determine the rules

MEMBER_TYPES = {
  1: "STAFF",
  2: "STUDENT",
  3: "GUEST"
}

CHARGER_TYPES= {
  1 : {
    "name" : "AC Fast Charger (7kW)",
    "rate" : [4.00, 6.00, 8.00, 12.00],
    "max": 80.00
  },
  2 : {
    "name" : "DC Ultra-Fast Charger (50kW)",
    "rate" : [10.00, 15.00, 20.00, 30.00],
    "max": 150.00
  },
}

DISCOUNTS = {
  1 : {
    "name" : "First-Time User (New Registration) (100%)",
    "amount": "100%"
  },
  2 : {
    "name" : "Staff Discount (50%)",
    "amount": "50%"
  },
  3 : {
    "name" : "Student Discount (AC Charger ONLY) (25%)",
    "amount": "25%"
  },
  4 : {
    "name" : "Green Eco-Pass Holder (Certified EV)",
    "amount": 2.00
  },
}

SURCHARGES = {
  1 : {
      "name" : "Peak Hour Charging (12 PM - 4 PM)",
      "amount": 5.00
    },
  2: {
      "name" : "Idle Parking",
      "amount": 15.00
    },
  3: {
      "name" : "Lost RFID Access Card Replacement Fee",
      "amount": 30.00
    }
}

# Loop the entire program without exiting
# Attendant can exit after completing each session
while True:
  # discount flags
  is_new_user, is_cert_ev  = False, False
  # surcharge flags
  is_peak_hour, is_idle_park, has_lost_card = False, False, False

  # User input
  user_id = str(input("Enter User ID: "))
  vehicle_number = str(input("Enter Vehicle number: "))
  session_duration = float(input("Enter session duration: "))
  member_type = int(input("1 for STAFF, 2 for STUDENT, 3 for GUEST: "))
  charger_type = int(input("1 for AC FAST CHARGER, 2 FOR DC Ultra-Fast Charger: "))

  # ROUND up to get the part thereof of hour
  session_duration = math.ceil(float(session_duration))

  # answer each question to determine discounts and surcharges to be applied to bill
  new_user = input("[DISCOUNT] Is member a new user? (Y/N): ")
  if new_user == "Y":
    is_new_user = True
  cert_ev = input("[DISCOUNT] Certified EV? (Y/N): ")
  if cert_ev == "Y":
    is_cert_ev = True

  peak_hour = input("[SURCHARGE] Is it peak hour (12 PM - 4 PM)? (Y/N): ")
  if peak_hour == "Y":
    is_peak_hour = True
  idle_park = input("[SURCHARGE] Idle Parking? (Y/N): ")
  if cert_ev == "Y":
    is_idle_park = True
  lost_card = input("[SURCHARGE] Access Card Replacement? (Y/N): ")
  if lost_card == "Y":
    has_lost_card = True

  # determine the applicable hourly rate depending on the duration of the session
  def charged_tier(session_dur):
    tier = 0  # default
    if session_dur < 3:
      tier = 0
    elif session_dur < 5:
      tier = 1
    elif session_dur < 7:
      tier = 2
    elif session_dur > 6:
      tier = 3
    return tier

  # Calculate gross fee based on charger type and duration
  # if gross fee is more than maximum for charger type, change gross fee to maximum
  def gross_fee():
    this_tier = charged_tier(session_duration)
    this_rate = CHARGER_TYPES[charger_type]["rate"][this_tier]
    maximum = CHARGER_TYPES[charger_type]["max"]
    this_gross_fee = float(session_duration * this_rate)

    if this_gross_fee > maximum:
      this_gross_fee = maximum

    return this_gross_fee

  # New user will be the ONLY discount possible if new user flag is True
  # Return tuple(int, list, list)
  def apply_new_user(gross_fee_amount):
    discount_list = []
    discount_items = []
    discount_total = gross_fee_amount
    discount_items.append(gross_fee_amount)
    discount_list.append(DISCOUNTS[1]['name'])
    return discount_total, discount_list, discount_items

  # Calculate percentage-based discount
  def calculate_discount_perc(perc, amount):
    return amount * (perc / 100)

  # Apply all other discounts (not NEW USER)
  # Return tuple(int, list, list)
  def apply_discount(gross_fee_amount):
    discount_total = 0
    discount_list = []
    discount_items = []
    # if staff
    if member_type == 1:
      this_discount = calculate_discount_perc(50, gross_fee_amount)
      discount_total += this_discount
      discount_items.append(this_discount)
      discount_list.append(DISCOUNTS[2]['name'])
    # if student and using AC charger
    elif member_type == 2 and charger_type == 1:
      this_discount = calculate_discount_perc(25, gross_fee_amount)
      discount_total += this_discount
      discount_items.append(this_discount)
      discount_list.append(DISCOUNTS[3]['name'])

    return discount_total, discount_list, discount_items

  # check against the surcharge flags and apply surcharge amount
  # append surcharge to list for receipt
  def apply_surcharge():
    surcharge_list = []
    surcharge_items = []
    surcharge_total = 0
    if is_peak_hour:
      surcharge_total += SURCHARGES[1]['amount']
      surcharge_list.append(SURCHARGES[1]['name'])
      surcharge_items.append(SURCHARGES[1]['amount'])
    if is_idle_park:
      surcharge_total += SURCHARGES[2]['amount']
      surcharge_list.append(SURCHARGES[2]['name'])
      surcharge_items.append(SURCHARGES[2]['amount'])
    if has_lost_card:
      surcharge_total += SURCHARGES[3]['amount']
      surcharge_list.append(SURCHARGES[3]['name'])
      surcharge_items.append(SURCHARGES[3]['amount'])
    return surcharge_total, surcharge_list, surcharge_items

  # this function will call other functions
  # Print receipt based on the rules, discounts and surcharges
  # Receipt will include all add and deducted amounts
  # ALL numbers are rounded to 2 decimal points (Currency)
  def bill_output():
    line_separator = "=" * 70
    # gross will not be modified from this point on
    gross_fee_amount = gross_fee()

    # Net payable = total bill
    net_payable = gross_fee_amount

    # If the member is a new user, apply ONLY the 100% waiver for discounts
    if is_new_user:
      discount_total, discount_list, discount_items = apply_new_user(gross_fee_amount)
    else:
      discount_total, discount_list, discount_items = apply_discount(gross_fee_amount)

    # Get Net payable after percentage discounts
    net_payable -= float(discount_total)

    # Apply certified EV on net payable
    if is_cert_ev:
      net_payable -= float(DISCOUNTS[4]['amount'])
      discount_items.append(DISCOUNTS[4]['amount'])
      discount_list.append(DISCOUNTS[4]['name'])

    # Apply surcharge only after all discounts have been deducted from net
    surcharge_total, surcharge_list, surcharge_items = apply_surcharge()
    net_payable += float(surcharge_total)

    # Print an itemized bill for every user
    print(line_separator)
    print(f"{'Member Type: ':>20} \t{MEMBER_TYPES[member_type]}")
    print(f"{'UserID: ':>20} \t{user_id}")
    print(f"{'Vehicle Number: ':>20} \t{vehicle_number}")
    print(f"{'Charger Used: ':>20} \t{CHARGER_TYPES[charger_type]["name"]}")
    print(f"{'Session Duration: ':>20} \t{session_duration} hour(s)")
    print(f"{'GROSS FEE: ':>50} \tRM {gross_fee_amount:<20.2f}") # {gross_fee_amount:.2f}
    print(line_separator)
    print(f"{'DISCOUNTS/WAIVER':^68}")
    for d_name, d_price in zip(discount_list, discount_items):
      print(f"{d_name:>50} \t-RM {d_price:<20.2f}")

    print(line_separator)
    print(f"{'SURCHARGES':^68}")
    for s_name, s_price in zip(surcharge_list, surcharge_items):
      print(f"{s_name:>50} \t+RM {s_price:<20.2f}")

    print(line_separator)
    print(f"{'NET PAYABLE':>50}")
    print(f"{'TOTAL':>50} \tRM {net_payable:<20.2f}")
    print(line_separator)
    return 0

  # CALL to start all functions
  bill_output()


  # exit program
  want_exit = str(input("Do you want to exit system? (Y/N): "))
  if want_exit == "Y":
    # break if attendant wants to close/ exit the system
    break
  else:
    # any other answer would continue the system
    continue

