from typing import List, Optional
from abc import ABC, abstractmethod
import math
from DeliveryBoy import DeliveryBoy



# Abstract Strategy for DeliveryBoy Assignment
class DeliveryAssignmentStrategy(ABC):
    @abstractmethod
    def assign_delivery_boy(self, order: "FoodOrder", delivery_boys: List[DeliveryBoy]):
        pass


# Concrete Strategy: Nearest Delivery Boy
class NearestDeliveryBoyStrategy(DeliveryAssignmentStrategy):
    def assign_delivery_boy(self, order: "FoodOrder", delivery_boys: List[DeliveryBoy]):
        """Assign the nearest available delivery boy to the order."""
        restaurant_location = (order.restaurant.location.latitude, order.restaurant.location.longitude)
        available_boys = [boy for boy in delivery_boys if boy.status == "available"]

        if not available_boys:
            print("No available delivery boys!")
            return None

        # Find the nearest delivery boy
        nearest_boy = min(available_boys, key=lambda boy: boy.distance_from(restaurant_location))
        nearest_boy.assign_order(order)
        return nearest_boy


# Concrete Strategy: Round-Robin Assignment
class RoundRobinDeliveryBoyStrategy(DeliveryAssignmentStrategy):
    def __init__(self):
        self.last_assigned_index = -1

    def assign_delivery_boy(self, order: "FoodOrder", delivery_boys: List[DeliveryBoy]):
        """Assign delivery boys in a round-robin fashion."""
        available_boys = [boy for boy in delivery_boys if boy.status == "available"]

        if not available_boys:
            print("No available delivery boys!")
            return None

        # Round-robin assignment
        self.last_assigned_index = (self.last_assigned_index + 1) % len(available_boys)
        selected_boy = available_boys[self.last_assigned_index]
        selected_boy.assign_order(order)
        return selected_boy


class LastOrderDateTimeDeliveryBoyStrategy(DeliveryAssignmentStrategy):

    def assign_delivery_boy(self, order: "FoodOrder", delivery_boys: List[DeliveryBoy]):
        """Assign delivery boys based on last order time"""
        available_boys = [boy for boy in delivery_boys if boy.status == "available"]
        for boy in delivery_boys:
            print(boy)
        available_boys = sorted(available_boys, key = lambda boy: boy.last_order_datetime)

        # print([boy ])
        if not available_boys:
            print("No available delivery boys!")
            return None

        selected_boy = available_boys[0]
        selected_boy.assign_order(order)
        return selected_boy
