# Chain of Responsibility Pattern: Logging Example

## Overview

The **Chain of Responsibility** is a behavioral design pattern that allows a request to pass through a chain of handlers. Each handler can either process the request or pass it to the next handler in the chain. This approach decouples the sender of the request from its receiver, making the system more flexible and easier to maintain.

This project demonstrates the Chain of Responsibility pattern through a logging system. Log messages are processed by different loggers (`ErrorLogger`, `DebugLogger`, and `InfoLogger`) based on their severity.

---

## Features

- **Flexible Request Handling**: Requests are handled by the first capable handler in the chain.
- **Decoupled Components**: The sender of a request does not need to know which handler will process it.
- **Single Responsibility**: Each handler focuses on handling a specific type of request.
- **Scalability**: Easily add or remove handlers from the chain.

---

## Usage

### Logging System Example

This example implements a logging system with log levels: `INFO`, `DEBUG`, `ERROR`, and `WARNING`. 

Each logger in the chain processes a specific level:
- `InfoLogger` handles `INFO` logs.
- `DebugLogger` handles `DEBUG` logs.
- `ErrorLogger` handles `ERROR` logs.

If a log level is not handled by any logger in the chain, a message indicating the unhandled log is displayed.

---
