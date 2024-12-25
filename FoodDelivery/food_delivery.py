'''
Food Delivery Service:-


Functional Requirements (FR)
	•	User Management: Register, login, manage user types
	•	Restaurant & Menu Management: Add/update restaurant and menu items
	•	Food Ordering: Book food items, confirm bookings
	•	Search & Filtering: Search by location, food type, and status
	•	Location Management: Update and search locations
	•	Booking Notification: Notify users through WhatsApp, Email, SMS
	•	Payment: Payment integration (suggested)
	•	Food Booking: Track bookings, selected food items
	•	Data Persistence: Store user, restaurant, and booking data

Non-Functional Requirements (NFR)
	•	Performance: Efficient user and restaurant handling
	•	Scalability: Support growth without degradation
	•	Usability: Intuitive UI, easy navigation
	•	Security: Secure user data and login
	•	Availability: 24/7 system uptime
	•	Maintainability: Easy to update and maintain
	•	Extensibility: Add new features easily (e.g., notifications)
	•	Logging & Monitoring: Log important actions, monitor health
	•	Compliance: Data protection and privacy laws
	•	Cross-Platform Support: Accessible on web and mobile

 pyreverse -o png FoodDelivery/food_delivery.py

'''


from enum import Enum
from typing import List, Optional
from collections import defaultdict
from abc import ABC, abstractmethod

# Enums
class FoodType(Enum):
    VEG = "veg"
    NON_VEG = "non_veg"

class UserType(Enum):
    ADMIN = "admin"
    RESTAURANT_OWNER = "restaurant_owner"
    CUSTOMER = "customer"
    OPERATOR = "operator"
    SUPPORT = "support"

# Notification Type Enum
class NotificationType(Enum):
    WHATSAPP = "WhatsApp"
    EMAIL = "Email"
    SMS = "SMS"

# Observer Interface
class Observer(ABC):
    @abstractmethod
    def update(self, booking_id: int, message: str):
        pass

# Concrete Observers
class WhatsAppNotification(Observer):
    def update(self, booking_id: int, message: str):
        print(f"WhatsApp Notification - Booking ID: {booking_id}, Message: {message}")

class EmailNotification(Observer):
    def update(self, booking_id: int, message: str):
        print(f"Email Notification - Booking ID: {booking_id}, Message: {message}")

class SMSNotification(Observer):
    def update(self, booking_id: int, message: str):
        print(f"SMS Notification - Booking ID: {booking_id}, Message: {message}")

# Classes
class Food:
    def __init__(self, id: int, name: str, price: float, food_type: FoodType, status: str):
        self.id = id
        self.name = name
        self.price = price
        self.food_type = food_type
        self.status = status  # "active" or "inactive"

    def update_food(self, price: Optional[float] = None, status: Optional[str] = None):
        if price:
            self.price = price
        if status:
            self.status = status

class Menu:
    def __init__(self, id: int, name: str):
        self.id = id
        self.name = name
        self.food_items: List[Food] = []

    def add_food(self, food: Food):
        self.food_items.append(food)

    def delete_food(self, food_id: int):
        self.food_items = [food for food in self.food_items if food.id != food_id]

class Location:
    def __init__(self, id: int, city: str, country: str, pincode: str, state: str, latitude: float, longitude: float):
        self.id = id
        self.city = city
        self.country = country
        self.pincode = pincode
        self.state = state
        self.latitude = latitude
        self.longitude = longitude

    def update_location(self, city: Optional[str] = None, state: Optional[str] = None):
        if city:
            self.city = city
        if state:
            self.state = state

class Restaurant:
    def __init__(self, id: int, name: str, location: Location, menu: Menu):
        self.id = id
        self.name = name
        self.location = location
        self.menu = menu

class User:
    def __init__(self, id: int, name: str, user_type: UserType, location: Optional[Location] = None):
        self.id = id
        self.name = name
        self.user_type = user_type
        self.location = location

    def login(self):
        print(f"{self.name} logged in.")

    def signup(self):
        print(f"{self.name} signed up.")

    def set_location(self, location: Location):
        self.location = location

    def get_location(self):
        return self.location

class FoodBooking:
    def __init__(self, booking_id: int, restaurant: Restaurant, user: User, food_items: List[Food]):
        self.booking_id = booking_id
        self.restaurant = restaurant
        self.user = user
        self.food_items = food_items
        self.observers: List[Observer] = []

    def add_observer(self, observer: Observer):
        self.observers.append(observer)

    def remove_observer(self, observer: Observer):
        self.observers.remove(observer)

    def notify_observers(self, message: str):
        for observer in self.observers:
            observer.update(self.booking_id, message)

    def confirm_booking(self):
        print(f"Booking Confirmed: {self.booking_id} for user {self.user.name} at {self.restaurant.name}")
        self.notify_observers("Your order has been confirmed!")

class FoodOrderingSystem:
    def __init__(self):
        self.restaurants: List[Restaurant] = []
        self.users: List[User] = []
        self.location_food_map: defaultdict[Tuple[str, Optional[FoodType]], List[Restaurant]] = defaultdict(list)

    def add_users(self, user: User):
        self.users.append(user)

    def add_restaurant(self, restaurant: Restaurant):
        self.restaurants.append(restaurant)
        for food_item in restaurant.menu.food_items:
            if food_item.status == "active":
                self.location_food_map[(restaurant.location.city, food_item.food_type)].append(restaurant)
                self.location_food_map[(restaurant.location.pincode, food_item.food_type)].append(restaurant)

    def confirm_booking(self, booking: FoodBooking):
        booking.confirm_booking()

    def get_food_items(self, restaurant: Restaurant, food_type: Optional[FoodType] = None):
        if food_type:
            return [food for food in restaurant.menu.food_items if food.food_type == food_type and food.status == "active"]
        return [food for food in restaurant.menu.food_items if food.status == "active"]

    def get_all_restaurants(self, location: Location, food_type: Optional[FoodType] = None):
        if food_type:
            city_key = (location.city, food_type)
            pincode_key = (location.pincode, food_type)
            restaurants = self.location_food_map.get(city_key, []) + self.location_food_map.get(pincode_key, [])
            return list(set(restaurants))  # Remove duplicates
        else:
            results = set()
            for key, restaurants in self.location_food_map.items():
                if key[0] in (location.city, location.pincode):
                    results.update(restaurants)
            return list(results)

# Example Usage
if __name__ == "__main__":
    # Create Location
    loc = Location(1, "Mumbai", "India", "400001", "Maharashtra", 19.0760, 72.8777)

    # Create Food Items
    pizza = Food(1, "Pizza", 500, FoodType.VEG, "active")
    burger = Food(2, "Burger", 200, FoodType.NON_VEG, "active")

    # Create Menu and Add Food
    menu = Menu(1, "Main Menu")
    menu.add_food(pizza)
    menu.add_food(burger)

    # Create Restaurant
    restaurant = Restaurant(1, "Food Paradise", loc, menu)

    # Create User
    user = User(1, "John Doe", UserType.CUSTOMER)
    user.set_location(loc)

    # Initialize Food Ordering System
    system = FoodOrderingSystem()
    system.add_restaurant(restaurant)
    system.add_users(user)

    # Search Restaurants
    available_restaurants = system.get_all_restaurants(loc, FoodType.VEG)
    for r in available_restaurants:
        print(f"Available Restaurant: {r.name} in {r.location.city}")

    # Create Notification Observers
    whatsapp = WhatsAppNotification()
    email = EmailNotification()
    sms = SMSNotification()

    # Create a FoodBooking instance
    booking = FoodBooking(101, restaurant, user, [pizza, burger])

    # Add Observers
    booking.add_observer(whatsapp)
    booking.add_observer(email)
    booking.add_observer(sms)

    # Confirm Booking
    booking.confirm_booking()

    # Output:
    # Available Restaurant: Food Paradise in Mumbai
    # Booking Confirmed: 101 for user John Doe at Food Paradise
    # WhatsApp Notification - Booking ID: 101, Message: Your order has been confirmed!
    # Email Notification - Booking ID: 101, Message: Your order has been confirmed!
    # SMS Notification - Booking ID: 101, Message: Your order has been confirmed!