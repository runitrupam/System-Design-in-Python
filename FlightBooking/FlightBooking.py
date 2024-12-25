'''
FR:-
search for flights based on date, arrival time and departure time.
Users login, signup
select a flight
enter personal details
choose seats and meals
payment
confirmation notification

Non FR:-
Scalability
Maintainability
Modularity(easy to add more functions)

Actors :-
Admin
Operators
Customers

'''

from enum import Enum
from typing import List, Optional
from datetime import datetime
import uuid

class UserType:
    ADMIN = 3
    CUSTOMER = 1
    OPERATOR = 2

class SeatType:
    ECONOMY = 1
    BUSINESS = 2

class FlightStatus:
    ONTIME = 1
    INACTIVE = 2
    CANCELLED = 3
    ARRIVED = 4
    DELAY = 5



class MealType:
    VEG = 1
    NON_VEG = 2
    NO_MEAL = 3



class Meal:
    def __init__(self, id: int, name: str, type: MealType, price: float):
        self.__id = id  # Private
        self.name = name
        self.type = type
        self.price = price

class Airline:
    def __init__(self, id: int, name: str, logo_url: str):
        self.__id = id  # Private
        self.name = name
        self.logo_url = logo_url

class Airport:
    def __init__(self, id: int, name: str, code: str, city: str, country: str, timezone: str):
        self.__id = id  # Private
        self.name = name
        self.code = code
        self.city = city
        self.country = country
        self.timezone = timezone

class FlightSchedule:
    def __init__(self, id : int, start_time : datetime, end_time : datetime ,\
                 start_airport : Airport, end_airport : Airport ):
        self.__id = id  # Private
        self.start_time = start_time
        self.end_time = end_time
        self.start_airport = start_airport
        self.end_airport = end_airport

    def get_duration(self) -> int:
        return (self.end_time - self.start_time).total_seconds() // 3600


class Flight:
    def __init__(self, flight_no: str, airline: Airline, status: FlightStatus, meals: List[Meal]):
        self.__flight_no = flight_no  # Private
        self.airline = airline
        self.status = status
        self.meals = meals
        self.schedules = []

    def update_status(self, status: FlightStatus):
        self.status = status

    def add_schedule(self, schedule: FlightSchedule):
        self.schedules.append(schedule)

    def get_flight_schedule(self, date: datetime, arrival_time: datetime,\
                     departure_time: datetime, start_airport : Airport, end_airport: Airport) -> Optional[FlightSchedule]:
        temp_schedule : List[FlightSchedule] = []
        for schedule in self.schedules:
            if (schedule.start_time.date() == date and schedule.start_airport == start_airport and schedule.end_airport == end_airport
                    and schedule.start_time.time() <= arrival_time and schedule.end_time.time() >= departure_time):
                temp_schedule.append(schedule)
        return temp_schedule




class User:
    def __init__(self, id: int, username: str, password: str, user_type: UserType, personal_details : dict):
        self.__id = id  # Private
        self.username = username
        self.password = password
        self.user_type = user_type
        self.personal_details = None
        self.status = None

    def login(self, username, password):
        if self.username == username and self.password == password:
            self.status = "logged_in"
            return True
        return False

class Payment:
    def __init__(self, user: User, flight: Flight,schedule:FlightSchedule, amount: float, transaction_id: str):
        self.user = user
        self.flight = flight
        self.schedule = schedule
        self.amount = amount
        self.__transaction_id = transaction_id

class Notification:
    def __init__(self, user: User, message: str, notification_id:str):
        self.user = user
        self.__notification_id = notification_id  # Private
        self.message = message


class BookingDetails:
    def __init__(self, flight: Flight, schedule : FlightSchedule,
                 user: User, start: str, no_of_passengers : int, destination: str, date: datetime, pnr: str, meal: Optional[Meal] = None):
        self.flight = flight
        self.schedule = schedule # all details of trip here
        self.user = user
        self.no_of_passengers = no_of_passengers
        self.pnr = None
        self.meal = meal
        self.status = None

    def confirm(self):
        self.pnr = str(uuid.uuid4())
        self.status = "booked"
        self.notifications.append(Notification(self.user, f"Your booking for flight {self.flight.flight_no} has been confirmed.", str(self.pnr )))
        self.payments.append(Payment(self.user, self.flight, self.schedule, self.schedule.get_duration() * self.no_of_passengers, self.pnr))
        return True


class FlightBookingSystem:

    def __init__(self):
        self.airlines = []
        self.airports = []
        self.flights = []
        self.users = []
        self.payments = []
        self.notifications = []
        self.booking_details = []

    def add_airline(self, airline: Airline):
        self.airlines.append(airline)

    def add_airport(self, airport: Airport):
        self.airports.append(airport)

    def add_flights(self,flight:Flight):
        self.flights.append(flight)

    def add_user(self, user: User):
        self.users.append(user)

    def get_schedules(self, date : datetime.date(), start_airport : Airport, end_airport:Airport,
                      arrival_time : datetime , departure_time : datetime, airline : Optional[Airline] ):
        schedules : List[Flight] = []
        for flight in self.flights:
            curr_flight_schedules =  flight.get_flight_schedule(date, arrival_time,departure_time, start_airport, end_airport)
            if curr_flight_schedules and (airline is None or flight.airline == airline):
                schedules.extend(curr_flight_schedules)
        # print statement
        return schedules


    def confirm_booking(self, booking_details: BookingDetails):
        if booking_details.confirm():
            self.booking_details.append(booking_details)
            return True
        else:
            return False

