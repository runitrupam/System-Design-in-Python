

'''

Non-FR :-
Scalability
Maintainability
Performance

Actors :-
Customers
Operators

Entities:-
User
Car
Location
ReservationService
PaymentGateway
NotificationGateway

FR :-
Login/Signup
Enter Location of the User
Search for the cars in a given Location
Choose Cars
Add details to book
Do Payment/Payment Gateway
get the confirmation notification



'''



from enum import Enum
from typing import List


# Enums
class UserType(Enum):
    CUSTOMER = 1
    OPERATOR = 2


class CarType(Enum):
    SEDAN = 1
    XUV = 2


class StatusType(Enum):
    VACANT = 1
    RUNNING = 2
    BOOKED = 3
    INACTIVE = 4


# Location Class
class Location:
    def __init__(self, id: int, pincode: str, latitude: int, longitude: int, city: str, address: str):
        self._id = id  # Private
        self.pincode = pincode
        self.latitude = latitude
        self.longitude = longitude
        self.city = city
        self.address = address

    def update_location(self, pincode: str, latitude: int, longitude: int, city: str, address: str):
        self.pincode = pincode
        self.latitude = latitude
        self.longitude = longitude
        self.city = city
        self.address = address

    def get_location(self):
        return {
            "pincode": self.pincode,
            "latitude": self.latitude,
            "longitude": self.longitude,
            "city": self.city,
            "address": self.address,
        }

    def delete_location(self):
        self.pincode = None
        self.latitude = None
        self.longitude = None
        self.city = None
        self.address = None


# User Class
class User:
    def __init__(self, id: int, name: str, user_type: UserType, loc: Location, license_id: str):
        self._id = id  # Private
        self.name = name
        self.user_type = user_type
        self.location = loc
        self.license_id = license_id

    def signup(self):
        print(f"User {self.name} has signed up.")

    def signin(self):
        print(f"User {self.name} has signed in.")

    def get_location(self):
        return self.location.get_location()


# Car Class
class Car:
    def __init__(self, id: int, name: str, car_type: CarType, status: StatusType, car_license: str, loc: Location, chassis_number: str):
        self._id = id  # Private
        self.name = name
        self.car_type = car_type
        self.status = status
        self.car_license = car_license
        self.location = loc
        self._chassis_number = chassis_number  # Private

    def reserve_vehicle(self):
        if self.status == StatusType.VACANT:
            self.status = StatusType.BOOKED
            print(f"Car {self.name} has been reserved.")
        else:
            print(f"Car {self.name} is not available.")

    def update_car_details(self, name: str, car_type: CarType, status: StatusType, car_license: str, loc: Location):
        self.name = name
        self.car_type = car_type
        self.status = status
        self.car_license = car_license
        self.location = loc


# Reserve Class
class Reserve:
    def __init__(self, id: int, user: User, car: Car, pickup: Location, drop: Location, rental_price: float, duration_in_hr: int):
        self._id = id  # Private
        self.user = user
        self.car = car
        self.pickup = pickup
        self.drop = drop
        self.rental_price = rental_price
        self.duration_in_hr = duration_in_hr

    def get_price(self):
        return self.rental_price

    def get_duration(self):
        return self.duration_in_hr


# CarReservationSystem Class
class CarReservationSystem:
    def __init__(self):
        self.cars = []  # List of Car
        self.users = []  # List of User
        self.locations = []  # List of Location
        self.reservations = []  # List of Reserve
        self.location_car_map = {}  # Mapping of Location to List of Cars

    def get_car_by_location(self, location: Location) -> List[Car]:
        return self.location_car_map.get(location, [])

    def get_car_by_type(self, car_type: CarType) -> List[Car]:
        return [car for car in self.cars if car.car_type == car_type]

    def book_car(self, reservation: Reserve):
        reservation.car.reserve_vehicle()
        self.reservations.append(reservation)

    def confirmation(self, reservation: Reserve):
        print(f"Reservation confirmed for User {reservation.user.name} with Car {reservation.car.name}.")


# Step 1: Setup Locations
loc1 = Location(id=1,pincode="560001", latitude=12, longitude=77, city="Bangalore", address="MG Road")
loc2 = Location(id=12,pincode="110001", latitude=28, longitude=77, city="Delhi", address="Connaught Place")

# Step 2: Create Users
user1 = User(id=1, name="Alice", user_type=UserType.CUSTOMER, loc=loc1, license_id="DL12345")
user2 = User(id=2, name="Bob", user_type=UserType.OPERATOR, loc=loc2, license_id="KA98765")

# Step 3: Add Cars
car1 = Car(id=1, name="Hyundai i10", car_type=CarType.SEDAN, status=StatusType.VACANT,
           car_license="KA01AB1234", loc=loc1, chassis_number="CH123456789")
car2 = Car(id=2, name="Toyota Fortuner", car_type=CarType.XUV, status=StatusType.VACANT,
           car_license="DL02XY5678", loc=loc2, chassis_number="CH987654321")

# Step 4: Initialize CarReservationSystem
car_reservation_system = CarReservationSystem()

# Add data to system
car_reservation_system.cars.extend([car1, car2])
car_reservation_system.users.extend([user1, user2])
car_reservation_system.locations.extend([loc1, loc2])

# Map cars to locations
car_reservation_system.location_car_map[loc1] = [car1]
car_reservation_system.location_car_map[loc2] = [car2]

# Step 5: Make a Reservation
reserve = Reserve(id=1, user=user1, car=car1, pickup=loc1, drop=loc2, rental_price=1500.0, duration_in_hr=5)

# Book the car
car_reservation_system.book_car(reserve)

# Confirm reservation
car_reservation_system.confirmation(reserve)


'''
Output:-
Car Hyundai i10 has been reserved.
Reservation confirmed for User Alice with Car Hyundai i10.


'''