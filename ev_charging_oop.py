# Name: ANDRIANARIVONY
# First name: NANTENAINA MIALY
# Student ID: 0399103
# ITS72604 Principles of Programming (202609)
# Assessment 1 - Task 4
# Object-Oriented Programming (OOP) Python program

from abc import ABC, abstractmethod
import math


# Relationship: User HAS-A ChargingSession
# User is an Abstract Class that cannot be instantiated alone
# User needs one of its children to be called
class User(ABC):
    def __init__(self, user_id, vehicle_number, charger_type):
        self.__user_id = user_id
        self.__vehicle_number = vehicle_number
        self._charger_type = charger_type

    @property
    # getter
    def user_id(self):
        return self.__user_id

    @property
    def vehicle_number(self):
        return self.__vehicle_number

    @property
    def charger_type(self):
        return self._charger_type

    # each child has to call this abstract method
    @abstractmethod
    def get_waiver(self, gross_fee):
        pass

# Child of User - called when user is a Staff member
class StaffUser(User):
    def __init__(self, user_id, vehicle_number, charger_type):
        super().__init__(user_id, vehicle_number, charger_type)

    # Polymorphism
    def get_waiver(self, gross_fee):
        # automatic 50% waiver
        amount = float(gross_fee * 0.5)
        return amount , "Taylor's Staff Member"

# Child of User - called when user is a Student member
class StudentUser(User):
    def __init__(self, user_id, vehicle_number, charger_type):
        super().__init__(user_id, vehicle_number, charger_type)

    # Polymorphism
    def get_waiver(self, gross_fee):
        # AC charger only, apply 25 % to the gross fee
        if super().charger_type == "AC":
            amount = float(gross_fee * 0.25)
            return amount, "Taylor's Student Member (AC Only)"
        else:
            return None

# Child of User - called when user is a Guest
class GuestUser(User):
    def __init__(self, user_id, vehicle_number, charger_type):
        super().__init__(user_id, vehicle_number, charger_type)
    # no waiver rules for guest
    # Polymorphism
    def get_waiver(self, gross_fee):
        pass

# Charger - does gross charging calculations
# stores charger tier rules and calculate based on these rules
class Charger:
    def __init__(self, charger_type, duration):
        self._charger_type = charger_type
        self._duration = duration
        self._tier = 0

        self._ac_rates = [4.00, 6.00, 8.00, 12.00]
        self._ac_max = 80.00

        self._dc_rates = [10.00, 15.00, 20.00, 30.00]
        self._dc_max = 150.00

        self._gross_fee = 0
        self.this_gross_fee()

    @property
    def charger_type(self):
        return self._charger_type
    @property
    def duration(self):
        return self._duration
    @property
    def tier(self):
        return self._tier
    @tier.setter
    def tier(self, tier):
        self._tier = tier
    @property
    def gross_fee(self):
        return self._gross_fee
    @gross_fee.setter
    def gross_fee(self, fee):
        self._gross_fee = fee

    # find what tier should be used to get gross fee
    # tier are index of the rates
    def determine_tier(self):
        if self.duration < 3:
            return 0
        elif self.duration < 5:
            return 1
        elif self.duration < 7:
            return 2
        elif self.duration > 6:
            return 3
        else:
            return 0

    # get gross charging fee
    # change rates depending on charger type, AC or DC Charger
    # calculate duration x tiered hourly
    def this_gross_fee(self):
        rates = []
        maxi = 0
        tier = self.determine_tier()
        if self.charger_type == "AC":
            rates = self._ac_rates
            maxi = self._ac_max
        elif self.charger_type == "DC":
            rates = self._dc_rates
            maxi = self._dc_max

        self.gross_fee = rates[tier] * self.duration
        if self.gross_fee > maxi:
            self.gross_fee = maxi


# one ChargingSession per user
# one Charger per Charging Session
class ChargingSession:
    def __init__(self, userid, vehicle, user_type, duration, charger_type,
                 is_new_user, is_certified_ev, is_peak_hour, is_idle_park, lost_card):
        # instantiante new User based on the user type
        # automatically waive if applicable
        if user_type == "Student":
            self._user = StudentUser(userid, vehicle, charger_type)
            self._user_type = "Student"
        elif user_type == "Staff":
            self._user = StaffUser(userid, vehicle, charger_type)
            self._user_type = "Staff"
        elif user_type == "Guest":
            self._user = GuestUser(userid, vehicle, charger_type)
            self._user_type = "Guest"

        # BOOLEAN FLAGS for discounts and surcharges
        self.__is_new_user = is_new_user
        self.__is_certified_ev = is_certified_ev
        self.__is_peak_hour = is_peak_hour
        self.__is_idle_park = is_idle_park
        self.__lost_card = lost_card

        # storage for applied discounts and surcharges
        # useful for itemized bill breakdown
        self.discount_dict = {}
        self.surcharge_dict = {}

        # ROUND UP duration (eg 2.3 --> 3, 2.6 --> 3)
        self.__duration = math.ceil(float(duration))
        self.__charger_type = charger_type

        # to be updated by later methods
        self._charger = None
        self._gross_charging_fee = 0
        self._net_payable = 0

    # @PROPERTY - safe getter/setter methods
    @property
    def user_type(self):
        return self._user_type
    @property
    def user(self):
        return self._user
    @property
    def duration(self):
        return self.__duration
    @property
    def charger(self):
        return self._charger
    @charger.setter
    def charger(self, charger):
        self._charger = charger
    @property
    def charger_type(self):
        return self.__charger_type
    @property
    def is_new_user(self):
        return self.__is_new_user
    @property
    def is_certified_ev(self):
        return self.__is_certified_ev
    @property
    def is_peak_hour(self):
        return self.__is_peak_hour
    @property
    def is_idle_park(self):
        return self.__is_idle_park
    @property
    def lost_card(self):
        return self.__lost_card
    @property
    def gross_charging_fee(self):
        return self._gross_charging_fee
    @gross_charging_fee.setter
    def gross_charging_fee(self, fee):
        self._gross_charging_fee = fee
    @property
    def net_payable(self):
        return self._net_payable
    @net_payable.setter
    def net_payable(self, net_payable):
        self._net_payable = net_payable

    # call Charger Class to get Gross Fee
    def get_gross_charging_fee(self):
        self.charger = Charger(self.charger_type, self.duration)
        self.gross_charging_fee = self.charger.gross_fee
        self.net_payable = self.gross_charging_fee

    # apply 100 % waiver
    def apply_new_user_waiver(self):
        self.discount_dict.update({"First-Time User (Complimentary Charge)": self.gross_charging_fee})
        self.net_payable = self.net_payable - self.gross_charging_fee

    # apply user waiver by calling User class
    def apply_user_waiver(self):
        amount, applied_discount = self.user.get_waiver(self.gross_charging_fee)
        self.net_payable = self.net_payable - amount

        if applied_discount:
            self.discount_dict.update({applied_discount: amount})

    # Main discount method - call other discount methods if conditions meet
    # apply other waiver that are not user-specific and flat discount
    def apply_discounts(self):
        if self.__is_new_user == "True":
            self.apply_new_user_waiver()
            pass
        else:
            self.apply_user_waiver()
            if self.__is_certified_ev == "True":
                self.net_payable -= 2.00
                self.discount_dict.update({"Green Eco-Pass Holder (Certified EV)": 2.00})

    # apply flat rate surcharges based on flags
    def apply_surcharges(self):
        if self.__is_peak_hour == "True":
            self.net_payable = self.net_payable + 5.00
            self.surcharge_dict.update({"Peak Hour Charging Surcharge (12 PM – 4 PM)": 5.00})
        if self.__is_idle_park == "True":
            self.net_payable = self.net_payable + 15.00
            self.surcharge_dict.update({"Idle Parking Surcharge": 15.00})
        if self.__lost_card == "True":
            self.net_payable = self.net_payable + 30.00
            self.surcharge_dict.update({"Lost RFID Access Card Replacement Fee": 30.00})

    # return None
    # Display total bill for the single charging session
    def bill_output(self):
        # get all necessary value in this order
        # calculate gross fee from charging only, then apply discounts and surcharges
        # to update net payable
        self.get_gross_charging_fee()
        self.apply_discounts()
        self.apply_surcharges()
        # Cosmetics for the receipt
        line_separator = "=" * 60
        section_separator = "*" * 60
        print(line_separator)
        # f:>20 will right-align the string/number within 20 characters
        # f:<20 will left-align the string/number within 20 characters
        # f^68 will center-align the string within 68 characters
        print(f"{'Member Type: ':>20} \t{self.user_type}")
        print(f"{'UserID: ':>20} \t{self.user.user_id}")
        print(f"{'Vehicle Number: ':>20} \t{self.user.vehicle_number}")
        print(f"{'Charger Used: ':>20} \t{self.charger_type}")
        print(f"{'Session Duration: ':>20} \t{self.duration} hour(s)")
        print(f"{'GROSS FEE: ':>50} \tRM {self.gross_charging_fee:<20.2f}")
        print(section_separator)
        print(f"{'DISCOUNTS/WAIVER':^68}")
        for d_name, d_price in self.discount_dict.items():
            print(f"{d_name:>50} \t-RM {d_price:<20.2f}")

        print(f"{'SURCHARGES':^68}")
        for s_name, s_price in self.surcharge_dict.items():
            print(f"{s_name:>50} \t+RM {s_price:<20.2f}")

        print(section_separator)
        print(f"{'NET PAYABLE':>50}")
        print(f"{'TOTAL':>50} \tRM {self.net_payable:<20.2f}")
        print(line_separator)



if __name__ == '__main__':
    # Instantiate multiple users here

    # user 1 is a student using AC
    user1 = ChargingSession("student01", "100AAA000", "Student", 2.6, "AC",
                                  "False", "True",
                                  "True", "True", "False")
    # user 2 is a staff member
    user2 = ChargingSession("staff01", "100BBB000", "Staff", 10, "DC",
                                  "False", "False",
                                  "False", "True", "False")
    # user 3 is new guest user
    user3 = ChargingSession("guest01", "153CCC000", "Guest", 5.7, "AC",
                                  "True", "True",
                                  "False", "False", "False")
    # user 4 is student
    user4 = ChargingSession("student02", "908SDD", "Student", 0.8, "DC",
                                  "True", "False",
                                  "False", "False", "False")
    # user 5 is staff
    user5 = ChargingSession("staff02", "EV890", "Staff", 4.2, "AC",
                                  "False", "False",
                                  "True", "False", "True")

    active_users = [user1, user2, user3, user4, user5]

    # Loop for each session and output bill
    for i, session in enumerate(active_users):
        print(f'SESSION {i + 1}:')
        session.bill_output()
