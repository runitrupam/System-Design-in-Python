from typing import List, Optional, Tuple
import math
import pandas as pd


class DeliveryBoy:
    def __init__(self, id: int, name: str, location: Tuple[float, float], status: str = "available"):
        self.id = id
        self.name = name
        self.location = location  # (latitude, longitude)
        self.status = status  # "available" or "busy"
        self.current_order = None
        self.last_order_datetime = pd.to_datetime('2024-12-10')

    def __str__(self):
        return f"DeliveryBoy: {self.name}, Status: {self.status}, Last Order Datetime: {self.last_order_datetime}"

    def update_last_order_datetime(self):
        self.last_order_datetime = pd.to_datetime('now')

    def distance_from(self, restaurant_location: Tuple[float, float]) -> float:
        """Calculate distance between delivery boy and restaurant using the Haversine formula."""
        lat1, lon1 = self.location
        lat2, lon2 = restaurant_location
        R = 6371  # Earth's radius in kilometers
        dlat = math.radians(lat2 - lat1)
        dlon = math.radians(lon2 - lon1)
        a = math.sin(dlat / 2) ** 2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon / 2) ** 2
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
        return R * c

    def assign_order(self, order: "FoodOrder"):
        """Assign an order to the delivery boy if available."""
        if self.status == "available":
            self.status = "busy"
            self.current_order = order
            print(f"Assigned Order {order.booking_id} to DeliveryBoy {self.name}")
            order.update_order_status("dispatched")
        else:
            print(f"DeliveryBoy {self.name} is currently busy.")

    def complete_order(self):
        """Complete the current order and make the delivery boy available again."""
        if self.current_order:
            print(f"DeliveryBoy {self.name} completed Order {self.current_order.booking_id}")
            self.current_order.update_order_status("completed")
            self.status = "available"
            self.current_order = None
            self.update_last_order_datetime()

