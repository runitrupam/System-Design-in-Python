'''

Chain of Responsibility Pattern
Use Cases of Chain of Responsibility Pattern
	1.	Event Handling in GUI Frameworks
	2.	Logging Frameworks
	3.	Authentication and Authorization
	4.	Technical Support Escalation
	5.	Validation Frameworks
	6.	Data Processing Pipelines

'''

from abc import ABC, abstractmethod

class BaseATMHandler(ABC):
    def __init__(self, denomination, next_handler=None):
        self.denomination = denomination
        self.next_handler = next_handler

    def handle_request(self, amount):
        """
        Handles the withdrawal amount by providing notes of the current denomination
        and delegating the remaining amount to the next handler.
        """
        if amount >= self.denomination:
            num_notes = amount // self.denomination
            remainder = amount % self.denomination
            print(f"{num_notes} x {self.denomination} notes")
        else:
            num_notes = 0
            remainder = amount

        # Pass the remainder to the next handler if it exists
        if remainder > 0 and self.next_handler:
            self.next_handler.handle_request(remainder)
        elif remainder > 0:
            print(f"Cannot dispense {remainder} as no smaller denominations are available.")

# Concrete Handlers
class Handler2000(BaseATMHandler):
    def __init__(self, next_handler=None):
        super().__init__(2000, next_handler)

class Handler500(BaseATMHandler):
    def __init__(self, next_handler=None):
        super().__init__(500, next_handler)

class Handler100(BaseATMHandler):
    def __init__(self, next_handler=None):
        super().__init__(100, next_handler)

# Configure the Chain
handler_100 = Handler100()
handler_500 = Handler500(next_handler=handler_100)
handler_2000 = Handler2000(next_handler=handler_500)

# Usage
withdraw_amount = 2500
print(f"Withdraw Request: {withdraw_amount}")
handler_2000.handle_request(withdraw_amount)

withdraw_amount = 3700
print(f"\nWithdraw Request: {withdraw_amount}")
handler_2000.handle_request(withdraw_amount)

withdraw_amount = 75
print(f"\nWithdraw Request: {withdraw_amount}")
handler_2000.handle_request(withdraw_amount)


'''
Output:-
Withdraw Request: 2500
1 x 2000 notes
1 x 500 notes

Withdraw Request: 3700
1 x 2000 notes
3 x 500 notes
2 x 100 notes

Withdraw Request: 75
Cannot dispense 75 as no smaller denominations are available.


'''