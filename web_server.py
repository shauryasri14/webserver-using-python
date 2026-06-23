import socket
import threading
from openpyxl import load_workbook
dict1={}
wb= load_workbook("users.xlsx")
ws=wb.active
SERVER_PORT=65432
server=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
server.bind(("0.0.0.0",SERVER_PORT))
server.listen()
print(f"Listening at port {SERVER_PORT}")
def form():
    return """
    <html>
    <head>
        <style>
            body {
                margin: 0;
                height: 100vh;
                display: flex;
                justify-content: center;
                align-items: center;
                background-color: #f0f2f5;
                font-family: Arial, sans-serif;
            }

            .container {
                background: white;
                padding: 30px;
                border-radius: 10px;
                box-shadow: 0px 0px 10px rgba(0,0,0,0.2);
                text-align: center;
            }

            input {
                width: 250px;
                padding: 10px;
                margin: 8px;
            }

            button {
                padding: 10px 20px;
                cursor: pointer;
            }
        </style>
    </head>

    <body>
        <div class="container">
            <h2>Enter Details</h2>

            <form method="POST" action="/submit">
                <input type="text" name="username" placeholder="Your name"><br>
                <input type="email" name="email" placeholder="Your email"><br>
                <button type="submit">Submit</button>
            </form>
        </div>
    </body>
    </html>
    """

imga=form().encode('utf-8')
header = (
            "HTTP/1.1 200 OK\r\n"
            "Content-Type: text/html;char-set=utf-8\r\n"  
            f"Content-Length: {len(imga)}\r\n"
            "Connection: close\r\n"
            "\r\n"
        )

def handle_client(csocket, caddress):
    try:

        print(f"Connected: {caddress}")
        request = csocket.recv(1024)
        rtext=request.decode('utf-8')
        if rtext.startswith("POST"):

            body = rtext.split("\r\n\r\n")[1]
            r=body.split("&")

            for m in r:
                if "=" in m:
                    key,value=m.split("=",1)
                    dict1[key]=value

            s=dict1["email"].replace("%40","@")
            dict1["email"]=s
            k=dict1["username"].replace("+"," ")
            dict1["username"]=k
            print(dict1)
            lock=threading.Lock()
            with lock:
                ws.append([dict1["username"], dict1["email"]])
                wb.save("users.xlsx")

        csocket.sendall(header.encode('utf-8') + imga)
    except Exception as e:
        print("Error: ", e)
    finally:
        csocket.close()

while True:
    try:
        vsocket=server.accept()
        csocket=vsocket[0]
        caddress=vsocket[1]
        thread = threading.Thread(target=handle_client, args=(csocket, caddress))
        thread.start()
    except Exception as e:
        print("Error",e)

server.close()