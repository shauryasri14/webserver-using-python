# Custom Multi-Threaded HTTP Server in Python

A lightweight, low-level HTTP server built entirely from scratch using Python's native `socket` and `threading` libraries. This project bypasses modern web frameworks (like Flask or FastAPI) to handle raw TCP networking, HTTP request parsing, and multi-threaded client handling manually. 

As a practical application, the server serves an HTML form, processes incoming `POST` requests, and logs user data into an Excel spreadsheet.

---

## Features

* **No Frameworks:** Built purely on top of standard Python TCP sockets (`socket.SOCK_STREAM`).
* **Multi-threaded Architecture:** Utilizes the `threading` module to handle concurrent incoming client connections without blocking.
* **Manual HTTP Parsing:** Decodes byte streams, isolates HTTP method types, and parses URL-encoded form data (e.g., converting `%40` back to `@`).
* **Persistent Data Storage:** Integrates with `openpyxl` to automatically append submitted form data into an Excel sheet (`users.xlsx`) in real-time.

---

## Tech Stack

* **Language:** Python 3.x
* **Core Modules:** `socket`, `threading`
* **Third-Party Libraries:** `openpyxl` (for Excel manipulation)
* **Frontend:** Inline HTML5 & CSS3

---

## Clone the Repository
```bash
git clone [https://github.com/shauryasri14/webserver-using-python.git](https://github.com/shauryasri14/webserver-using-python.git)
cd webserver-using-python
