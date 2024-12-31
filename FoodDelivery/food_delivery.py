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
from typing import List, Optional, Tuple
from collections import defaultdict
from abc import ABC, abstractmethod
from DeliveryAssignmentStrategy import DeliveryAssignmentStrategy, NearestDeliveryBoyStrategy, \
    RoundRobinDeliveryBoyStrategy, LastOrderDateTimeDeliveryBoyStrategy
from DeliveryBoy import DeliveryBoy
import math


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


class FoodOrder:
    def __init__(self, booking_id: int, restaurant: Restaurant, user: User, food_items: List[Food]):
        self.booking_id = booking_id
        self.restaurant = restaurant
        self.user = user
        self.food_items = food_items
        self.observers: List[Observer] = []
        self.order_status = 'in_cart'  # Order status can be 'in_cart', 'confirmed', 'dispatched', 'completed'

    def update_order_status(self, order_status):
        self.order_status = order_status

    def add_observer(self, observer: Observer):
        self.observers.append(observer)

    def remove_observer(self, observer: Observer):
        self.observers.remove(observer)

    def notify_observers(self, message: str):
        for observer in self.observers:
            observer.update(self.booking_id, message)

    def confirm_booking(self):
        self.order_status = 'confirmed'
        print(f"Booking Confirmed: {self.booking_id} for user {self.user.name} at {self.restaurant.name}")
        self.notify_observers("Your order has been confirmed!")

    def complete_food_delivery(self):
        self.order_status = 'completed'
        print(f"Food Delivery Completed: {self.booking_id} for user {self.user.name} at {self.restaurant.name}")
        self.notify_observers("Your food has been delivered!")


class FoodOrderingSystem:
    def __init__(self, strategy: DeliveryAssignmentStrategy):
        self.restaurants: List[Restaurant] = []
        self.users: List[User] = []
        self.location_food_map: defaultdict[Tuple[str, Optional[FoodType]], List[Restaurant]] = defaultdict(list)
        self.delivery_boys: List[DeliveryBoy] = []
        self.assignment_strategy = strategy  # Inject the strategy

    def add_delivery_boy(self, delivery_boy: DeliveryBoy):
        self.delivery_boys.append(delivery_boy)



    def add_user(self, user: User):
        self.users.append(user)

    def add_restaurant(self, restaurant: Restaurant):
        self.restaurants.append(restaurant)
        for food_item in restaurant.menu.food_items:
            if food_item.status == "active":
                self.location_food_map[(restaurant.location.city, food_item.food_type)].append(restaurant)
                self.location_food_map[(restaurant.location.pincode, food_item.food_type)].append(restaurant)



    def get_food_items(self, restaurant: Restaurant, food_type: Optional[FoodType] = None):
        if food_type:
            return [food for food in restaurant.menu.food_items if
                    food.food_type == food_type and food.status == "active"]
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
    def confirm_booking(self, booking: FoodOrder):
        booking.confirm_booking()
    def assign_delivery_boy_to_order(self, order: "FoodOrder"):
        """Use the selected strategy to assign a delivery boy."""
        return self.assignment_strategy.assign_delivery_boy(order, self.delivery_boys)


# Example Usage
if __name__ == "__main__":
    # Create Location
    loc1 = Location(1, "Mumbai", "India", "400001", "Maharashtra", 19.0760, 72.8777)
    loc2 = Location(2, "Pune", "India", "411001", "Maharashtra", 18.5204, 73.8567)

    # Delivery Boys
    boy1 = DeliveryBoy(1, "Delivery Boy 1", (19.0760, 72.8777))  # Mumbai
    boy2 = DeliveryBoy(2, "Delivery Boy 2", (18.5204, 73.8567))  # Pune
    boy3 = DeliveryBoy(3, "Delivery Boy 3", (19.0761, 72.8778))  # Mumbai

    # Create Food Items
    pizza = Food(1, "Pizza", 500, FoodType.VEG, "active")
    burger = Food(2, "Burger", 200, FoodType.NON_VEG, "active")

    # Create Menu and Add Food
    menu = Menu(1, "Main Menu")
    menu.add_food(pizza)
    menu.add_food(burger)

    # Create Restaurant
    restaurant = Restaurant(1, "Food Paradise", loc1, menu)

    # Create User
    user = User(1, "John Doe", UserType.CUSTOMER)
    user.set_location(loc1)

    # Initialize Food Ordering System
    # system = FoodOrderingSystem()
    system = FoodOrderingSystem(NearestDeliveryBoyStrategy())
    system.add_restaurant(restaurant)
    system.add_user(user)
    system.add_delivery_boy(boy1)
    system.add_delivery_boy(boy2)
    system.add_delivery_boy(boy3)

    # Search Restaurants
    available_restaurants = system.get_all_restaurants(loc1, FoodType.VEG)
    for r in available_restaurants:
        print(f"Available Restaurant: {r.name} in {r.location.city}")

    # Create Notification Observers
    whatsapp = WhatsAppNotification()
    email = EmailNotification()
    sms = SMSNotification()

    # Create a FoodOrder instance
    food_order1 = FoodOrder(101, restaurant, user, [pizza, burger])

    # Add Observers
    food_order1.add_observer(whatsapp)
    food_order1.add_observer(email)
    food_order1.add_observer(sms)

    # Confirm food_order1
    food_order1.confirm_booking()
    # Assign Delivery Boy
    order1_delivery_boy = system.assign_delivery_boy_to_order(food_order1)
    order1_delivery_boy.complete_order()
    print()

    # Change strategy to RoundRobinDeliveryBoyStrategy
    system.assignment_strategy = RoundRobinDeliveryBoyStrategy()
    order2 = FoodOrder(102, restaurant, user, [burger])
    order2_delivery_boy = system.assign_delivery_boy_to_order(order2)
    order2_delivery_boy.complete_order()
    print()

    # change strategy to LastOrderDateTimeDeliveryBoyStrategy
    system.assignment_strategy = LastOrderDateTimeDeliveryBoyStrategy()
    order3 = FoodOrder(103, restaurant, user, [pizza])
    order3.confirm_booking()
    system.assign_delivery_boy_to_order(order3)

'''
# Output:

Available Restaurant: Food Paradise in Mumbai
Booking Confirmed: 101 for user John Doe at Food Paradise
WhatsApp Notification - Booking ID: 101, Message: Your order has been confirmed!
Email Notification - Booking ID: 101, Message: Your order has been confirmed!
SMS Notification - Booking ID: 101, Message: Your order has been confirmed!
Assigned Order 101 to DeliveryBoy Delivery Boy 1
DeliveryBoy Delivery Boy 1 completed Order 101

Assigned Order 102 to DeliveryBoy Delivery Boy 1
DeliveryBoy Delivery Boy 1 completed Order 102

Booking Confirmed: 103 for user John Doe at Food Paradise
DeliveryBoy: Delivery Boy 1, Status: available, Last Order Datetime: 2024-12-31 19:59:49.723140
DeliveryBoy: Delivery Boy 2, Status: available, Last Order Datetime: 2024-12-10 00:00:00
DeliveryBoy: Delivery Boy 3, Status: available, Last Order Datetime: 2024-12-10 00:00:00
Assigned Order 103 to DeliveryBoy Delivery Boy 2
'''
