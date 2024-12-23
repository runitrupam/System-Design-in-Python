'''

 Chain of Responsibility Pattern
Use Cases of Chain of Responsibility Pattern
	1.	Event Handling in GUI Frameworks
	2.	Logging Frameworks
	3.	Authentication and Authorization
	4.	Technical Support Escalation
	5.	Validation Frameworks
	6.	Data Processing Pipelines


ATM
There is a chain , e.g. If you like to withdraw 2500 rs note from the bank
Hanldler_2000  --> 0
Hanldler_500  --> 4
Hanldler_100  --> 10

so 4*500 + 5*100 = 2500
Code goes to Hanldler_2000(amt = 2500) --> Hanldler_500(amt = 2500) --> Hanldler_100(amt = 500)
And the reurn is checked with the original amount

'''
from abc import ABC, abstractmethod
from enum import Enum

class LogLevel(Enum):
    INFO = 1
    DEBUG = 2
    ERROR = 3
    WARNING = 4

# Abstract BaseLogger
class BaseLogger(ABC):
    def __init__(self, log_level, next_logger=None):
        self.log_level = log_level
        self.next_logger = next_logger

    def log(self, level, message):
        """
        Handles the log message if it matches or delegates it to the next handler.
        """
        if level == self.log_level:
            self.write_message(message)
        elif self.next_logger:
            self.next_logger.log(level, message)
        else:
            print(f"Log level {level.name} not handled: {message}")

    @abstractmethod
    def write_message(self, msg):
        """Abstract method to define the logger's output behavior."""
        pass

# Concrete Loggers
class InfoLogger(BaseLogger):
    def write_message(self, msg):
        print(f"[INFO]: {msg}")

class DebugLogger(BaseLogger):
    def write_message(self, msg):
        print(f"[DEBUG]: {msg}")

class ErrorLogger(BaseLogger):
    def write_message(self, msg):
        print(f"[ERROR]: {msg}")

# Configure the Chain
info_logger = InfoLogger(LogLevel.INFO)
debug_logger = DebugLogger(LogLevel.DEBUG, next_logger=info_logger)
error_logger = ErrorLogger(LogLevel.ERROR, next_logger=debug_logger)


# Usage
error_logger.log(LogLevel.INFO, "This is an info message.")
error_logger.log(LogLevel.DEBUG, "Debugging application.")
error_logger.log(LogLevel.ERROR, "An error occurred!")
error_logger.log(LogLevel.WARNING, "This is a warning.")  # Unhandled level / Exception (Warning no declared)
# Note:- Code follows SOLID

'''
Output:-
[INFO]: This is an info message.
[DEBUG]: Debugging application.
[ERROR]: An error occurred!
Log level WARNING not handled: This is a warning.

'''