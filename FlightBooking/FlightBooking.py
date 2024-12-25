from enum import Enum
from typing import List, Optional, Dict, Set
from datetime import datetime
import uuid


class UserType:
    ADMIN = 3
    CUSTOMER = 1
    OPERATOR = 2


class SeatType(Enum):
    ECONOMY = 1
    BUSINESS = 2


class FlightStatus(Enum):
    ONTIME = 1
    INACTIVE = 2
    CANCELLED = 3
    ARRIVED = 4
    DELAY = 5


class MealType(Enum):
    VEG = 1
    NON_VEG = 2
    NO_MEAL = 3


class Meal:
    def __init__(self, id: int, name: str, type: MealType, price: float):
        self.id = id
        self.name = name
        self.type = type
        self.price = price


class Airline:
    def __init__(self, id: int, name: str, logo_url: str):
        self.id = id
        self.name = name
        self.logo_url = logo_url


class Airport:
    def __init__(self, id: int, name: str, code: str, city: str, country: str, timezone: str):
        self.id = id
        self.name = name
        self.code = code
        self.city = city
        self.country = country
        self.timezone = timezone


class FlightSchedule:
    def __init__(self, id: int, start_time: datetime, end_time: datetime,
                 start_airport: Airport, end_airport: Airport, seats: Dict[int, SeatType]):
        self.id = id
        self.start_time = start_time
        self.end_time = end_time
        self.start_airport = start_airport
        self.end_airport = end_airport
        self.seats = seats
        self.booked_seats: Set[int] = set()

    def get_duration(self) -> int:
        return (self.end_time - self.start_time).total_seconds() // 3600

    def book_seats(self, seat_numbers: List[int]) -> bool:
        unavailable_seats = [seat for seat in seat_numbers if seat in self.booked_seats or seat not in self.seats]
        if unavailable_seats:
            print(f"Error: Seats {unavailable_seats} are not available.")
            return False
        self.booked_seats.update(seat_numbers)
        print(f"Seats {seat_numbers} successfully booked.")
        return True

    def available_seats(self) -> List[int]:
        return [seat for seat in self.seats if seat not in self.booked_seats]


class Flight:
    def __init__(self, flight_no: str, airline: Airline, status: FlightStatus, meals: List[Meal]):
        self.flight_no = flight_no
        self.airline = airline
        self.status = status
        self.meals = meals
        self.schedules: List[FlightSchedule] = []

    def update_status(self, status: FlightStatus):
        self.status = status

    def add_schedule(self, schedule: FlightSchedule):
        self.schedules.append(schedule)

    def get_flight_schedule(self, date: datetime, arrival_time: datetime, departure_time: datetime,
                            start_airport: Airport, end_airport: Airport) -> List[FlightSchedule]:
        return [
            schedule for schedule in self.schedules
            if schedule.start_time.date() == date.date() and
               schedule.start_airport == start_airport and
               schedule.end_airport == end_airport and
               schedule.start_time.time() <= arrival_time.time() <= schedule.end_time.time() and
               schedule.start_time.time() <= departure_time.time() <= schedule.end_time.time()
        ]


class User:
    def __init__(self, id: int, username: str, password: str, user_type: UserType, personal_details: dict):
        self.id = id
        self.username = username
        self.password = password
        self.user_type = user_type
        self.personal_details = personal_details
        self.status = None

    def login(self, username: str, password: str) -> bool:
        if self.username == username and self.password == password:
            self.status = "logged_in"
            print(f"User {self.username} logged in successfully.")
            return True
        print(f"Login failed for user {self.username}.")
        return False


class Payment:
    def __init__(self, user: User, flight: Flight, schedule: FlightSchedule, amount: float, transaction_id: str):
        self.user = user
        self.flight = flight
        self.schedule = schedule
        self.amount = amount
        self.__transaction_id = transaction_id


class Notification:
    def __init__(self, user: User, message: str, notification_id: str):
        self.user = user
        self.__notification_id = notification_id  # Private
        self.message = message


class BookingDetails:
    def __init__(self, flight: Flight, schedule: FlightSchedule,
                 user: User, start: str, no_of_passengers: int, seats: List[int], destination: str, date: datetime,
                 pnr: str, meal: Optional[Meal] = None):
        self.flight = flight
        self.schedule = schedule
        self.user = user
        self.no_of_passengers = no_of_passengers
        self.pnr = pnr
        self.meal = meal
        self.status = None
        self.notifications: List[Notification] = []
        self.payments: List[Payment] = []

    def confirm(self) -> bool:
        if self.schedule.book_seats([1, 3]):  # Book seats 1 and 3

            self.pnr = str(uuid.uuid4())
            self.status = "booked"
            self.notifications.append(
                Notification(self.user, f"Your booking for flight {self.flight.flight_no} has been confirmed.",
                             str(self.pnr)))
            self.payments.append(Payment(self.user, self.flight, self.schedule,
                                         self.schedule.get_duration() * self.no_of_passengers, self.pnr))
            return True
        return False


class FlightBookingSystem:
    def __init__(self):
        self.airlines: List[Airline] = []
        self.airports: List[Airport] = []
        self.flights: List[Flight] = []
        self.users: List[User] = []
        self.bookings: List[BookingDetails] = []

    def add_airline(self, airline: Airline):
        self.airlines.append(airline)

    def add_airport(self, airport: Airport):
        self.airports.append(airport)

    def add_flight(self, flight: Flight):
        self.flights.append(flight)

    def add_user(self, user: User):
        self.users.append(user)

    def get_schedules(self, date: datetime, start_airport: Airport, end_airport: Airport,
                      arrival_time: datetime, departure_time: datetime, airline: Optional[Airline] = None) -> List[
        FlightSchedule]:
        schedules: List[FlightSchedule] = []
        for flight in self.flights:
            curr_flight_schedules = flight.get_flight_schedule(date, arrival_time, departure_time, start_airport,
                                                               end_airport)
            if curr_flight_schedules and (airline is None or flight.airline == airline):
                schedules.extend([(schedule, flight) for schedule in curr_flight_schedules])
        return schedules

    def confirm_booking(self, booking_details: BookingDetails) -> bool:
        if booking_details.confirm():
            self.bookings.append(booking_details)
            return True
        return False


# Example Usage
if __name__ == "__main__":
    from datetime import datetime, timedelta

    # Create a flight booking system
    system = FlightBookingSystem()

    # Add some airports
    airport1 = Airport(1, "Mumbai Airport", "JFK", "New York", "USA", "EST")
    airport2 = Airport(2, "Delhi Airport", "LAX", "Los Angeles", "USA", "PST")
    system.add_airport(airport1)
    system.add_airport(airport2)

    # Add an airline
    airline1 = Airline(1, "Indigo Airlines", "https://logo.com/american-airlines.png")
    system.add_airline(airline1)

    # Create a flight
    flight1 = Flight("AA100", airline1, FlightStatus.ONTIME, [])
    flight2 = Flight("BB100", airline1, FlightStatus.ONTIME, [])

    system.add_flight(flight1)
    system.add_flight(flight2)

    # Add flight schedules
    schedule1 = FlightSchedule(
        1,
        start_time=datetime(2024, 12, 25, 10, 0),  # 10:00 AM
        end_time=datetime(2024, 12, 25, 14, 0),  # 2:00 PM
        start_airport=airport1,
        end_airport=airport2,
        seats={1: SeatType.ECONOMY, 2: SeatType.BUSINESS, 3: SeatType.ECONOMY}
    )
    schedule2 = FlightSchedule(
        1,
        start_time=datetime(2024, 12, 25, 15, 0),
        end_time=datetime(2024, 12, 25, 20, 0),
        start_airport=airport2,
        end_airport=airport1,
        seats={1: SeatType.ECONOMY, 2: SeatType.BUSINESS, 3: SeatType.ECONOMY}
    )
    flight1.add_schedule(schedule1)
    flight1.add_schedule(schedule2)
    flight2.add_schedule(schedule1)

    # Add a user
    user1 = User(1, "rk568", "password123", UserType.CUSTOMER, {"email": "rk@example.com"})
    system.add_user(user1)

    # Login the user
    user1.login("rk568", "password123")

    # Search for schedules
    print("Available schedules:")
    schedules = system.get_schedules(
        date=datetime(2024, 12, 25),
        start_airport=airport1,
        end_airport=airport2,
        arrival_time=datetime(2024, 12, 25, 11, 0),
        departure_time=datetime(2024, 12, 25, 13, 0),
        airline=airline1
    )  # returns the flight departure after the given time and arrival time before the given arrival time.

    for schedule, flight in schedules:
        print(
            f"Flight : {flight.flight_no}, Airline : {flight.airline.name}, Schedule ID: {schedule.id}, Start: {schedule.start_time}, End: {schedule.end_time}")

    # Book a flight
    if schedules:
        selected_schedule = schedules[0][0]

        # Create booking details
        booking_details = BookingDetails(
            flight=flight1,
            schedule=selected_schedule,
            user=user1,
            start=airport1.name,
            destination=airport2.name,
            no_of_passengers=2,
            seats=[1, 3],
            date=datetime(2024, 12, 25),
            pnr=None,
            meal=None
        )

        # Confirm the booking
        if system.confirm_booking(booking_details):
            print(f"Booking confirmed! PNR: {booking_details.pnr}")
            print(f"Notifications: {[notification.message for notification in booking_details.notifications]}")
            print(
                f"Payment details: Amount - {booking_details.payments[0].amount}, Transaction ID - {booking_details.payments[0]._Payment__transaction_id}")
        else:
            print("Booking failed.")

'''
Output:-
User rk568 logged in successfully.
Available schedules:
Flight : AA100, Airline : Indigo Airlines, Schedule ID: 1, Start: 2024-12-25 10:00:00, End: 2024-12-25 14:00:00
Flight : BB100, Airline : Indigo Airlines, Schedule ID: 1, Start: 2024-12-25 10:00:00, End: 2024-12-25 14:00:00
Seats [1, 3] successfully booked.
Booking confirmed! PNR: 897652ba-02f7-4132-bcf9-df6c1d82c5d7
Notifications: ['Your booking for flight AA100 has been confirmed.']
Payment details: Amount - 8.0, Transaction ID - 897652ba-02f7-4132-bcf9-df6c1d82c5d7
'''
