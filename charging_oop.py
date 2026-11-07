from abc import ABC, abstractmethod
import math

class User:
    def __init__(self, user_id, vehicle_number):
        self.user_id = user_id
        self.vehicle_number = vehicle_number




if __name__ == '__main__':

    # Instantiate multiple users here
    # id, vehicle, user type, duration,
    #new_user= "True", peak_hour, certified_ev, idle_parking
    userSession = User("stu001", "veh011", "Student", 2.6, "AC")
    print("user: ", userSession.user.user_id)