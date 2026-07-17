# Custom Multi-Threaded HTTP Server in Python

A lightweight, low-level HTTP server built entirely from scratch using Python's native `socket` and `threading` libraries. This project bypasses modern web frameworks (like Flask or FastAPI) to handle raw TCP networking, HTTP request parsing, and multi-threaded client handling manually.

As a practical demonstration, the server serves a simple HTML form (similar in spirit to a Google Form), accepts submitted user details via `POST`, and logs each submission into an Excel spreadsheet.

---

## Features

- **No Frameworks** — built purely on top of standard Python TCP sockets (`socket.SOCK_STREAM`), with no Flask/FastAPI/Django involved.
- **Multi-threaded Architecture** — every incoming client connection is handed off to its own thread via `threading.Thread`, so multiple submissions can be handled concurrently.
- **Manual HTTP Parsing** — decodes the raw byte stream, detects the request method, and manually splits and parses the `POST` body (`key=value&key=value` format) without any external parsing library.
- **URL-Decoding by Hand** — converts basic URL-encoded characters back to their original form (e.g. `%40` → `@`, `+` → space) directly in code.
- **Thread-Safe Persistence** — uses a `threading.Lock` to safely append each submission (`username`, `email`) into `users.xlsx` via `openpyxl`, even under concurrent requests.
- **Self-Contained Response** — the HTML form (with inline CSS) is generated in Python and served directly as the HTTP response body, with a manually constructed response header (status line, `Content-Type`, `Content-Length`, `Connection: close`).

---

## Tech Stack

| Component      | Details                          |
|-----------------|----------------------------------|
| Language        | Python 3.x                       |
| Core Modules    | `socket`, `threading`            |
| Third-Party Lib | `openpyxl` (Excel read/write)     |
| Frontend        | Inline HTML5 & CSS3              |
| Storage         | `users.xlsx`                     |

---

## How It Works

1. The server opens a TCP socket and listens on port `65432`.
2. When a client connects, a new thread is spawned to handle that connection independently.
3. The raw request bytes are decoded and inspected:
   - If it's a `POST` request, the body is extracted and split on `&`/`=` to pull out form fields.
   - `username` and `email` values are cleaned up (URL-decoded) and appended to `users.xlsx` under a lock, so concurrent writes don't corrupt the file.
4. Regardless of the request type, the server responds with a manually built HTTP header followed by the HTML form, so the page can be reloaded and resubmitted.
5. The connection is then closed (`Connection: close`), and the thread exits.

---

## Getting Started

### Prerequisites
- Python 3.x
- `openpyxl` installed:
  ```
  pip install openpyxl
  ```
- An existing `users.xlsx` file in the project directory (the script expects one to already exist and loads it with `load_workbook`).

### Clone the Repository

```
git clone https://github.com/shauryasri14/webserver-using-python.git
cd webserver-using-python
```

### Run the Server

```
python web_server.py
```

The server will start listening on port `65432`. Visit:

```
http://localhost:65432
```

Fill in the form and submit — your name and email will be appended as a new row in `users.xlsx`.

---
## Demo Video




https://github.com/user-attachments/assets/cd962863-7162-4fcd-b775-97698df2e2d5







## Known Limitations

This project is intentionally minimal and was built to understand HTTP and sockets at a low level rather than to be production-ready. A few honest caveats:

- Only handles a single request per connection (`Connection: close`), and reads at most 1024 bytes per request — larger payloads aren't handled.
- Form parsing assumes exactly the fields the form sends (`username`, `email`) and isn't a general-purpose URL-decoder.
- No input validation, sanitization, or error responses (e.g. 404, 400) are implemented — it's a happy-path demo.
- `users.xlsx` must already exist before starting the server.

---

## Why This Project

Frameworks like Flask/FastAPI hide almost all of the networking and protocol-handling work. This project was built to peel that back — manually parsing HTTP requests, managing raw sockets, and handling concurrency with threads — to build a genuine, ground-up understanding of what a web server actually does.
