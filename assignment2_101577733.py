"""
Author: John Kenny
Assignment: #2
Description: Port Scanner — A tool that scans a target machine for open network ports
"""

import socket
import threading
import sqlite3
import os
import platform
import datetime


print("Python Version: ", platform.python_version())
print("Operating System: ", os.name)



# this dictionary stores commonly used port numbers with their corresponding service
common_ports = {
    21: "FTP",
    22: "SSH",
    23: "Telnet",
    25: "SMTP",
    53: "DNS",
    80: "HTTP",
    110: "POP3",
    143: "IMAP",
    443: "HTTPS",
    3306: "MySQL",
    3389: "RDP",
    8080: "HTTP-Alt"
}

class NetworkTool:
    def __init__(self, target: str):
        self.__target = target

    @property
    def target(self):
        return self.__target
    
    @target.setter
    def target(self):
        if self.target != "":
            return self.__target
        else:
            print("Error: Target cannot be empty")

    def __del__(self):
        print("NetworkTool instance destroyed")




# Q3: What is the benefit of using @property and @target.setter?
# TODO: Your 2-4 sentence answer here... (Part 2, Q3)



# TODO: Create the PortScanner child class that inherits from NetworkTool (Step vi)
# - Constructor: call super().__init__(target), initialize self.scan_results = [], self.lock = threading.Lock()
# - Destructor: print "PortScanner instance destroyed", call super().__del__()
#
# - scan_port(self, port):
#     Q4: What would happen without try-except here?
#     TODO: Your 2-4 sentence answer here... (Part 2, Q4)
#
#     - try-except with socket operations
#     - Create socket, set timeout, connect_ex
#     - Determine Open/Closed status
#     - Look up service name from common_ports (use "Unknown" if not found)
#     - Acquire lock, append (port, status, service_name) tuple, release lock
#     - Close socket in finally block
#     - Catch socket.error, print error message
#
# - get_open_ports(self):
#     - Use list comprehension to return only "Open" results
#
#     Q2: Why do we use threading instead of scanning one port at a time?
#     TODO: Your 2-4 sentence answer here... (Part 2, Q2)
#
# - scan_range(self, start_port, end_port):
#     - Create threads list
#     - Create Thread for each port targeting scan_port
#     - Start all threads (one loop)
#     - Join all threads (separate loop)



"""
Portscanner reuses code from NetworkTool through inheritance. 
One example of how it does this is through its setter function for the target field.
The setter function for the target field is: target(). 
"""
class PortScanner(NetworkTool):
    def __init__(self, target = ''):
        super().__init__(target)
        self.scan_results = []
        self.lock = threading.Lock()
    
    def __del__(self):
        super().__del__()
        print("PortScanner instance destroyed")

    def scan_port(self, port):
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(1)
            result = sock.connect_ex((self.target, port))
            if result == 0:
                status = "Open"
            else:
                status = "Closed"
                   
            if port not in common_ports.keys():
                service_name = "Unknown"
            else:
                service_name = common_ports[port]
            self.lock.acquire()
            self.scan_results.append((port, status, service_name))
            self.lock.release()
        except socket.error as ex:
            print(f"Error scanning port {port}: {ex}")
        finally:
            sock.close()

    def get_open_ports(self):
        return [x for x in self.scan_results if x[1] == "Open"]
    
    def scan_range(self, start_port, end_port):
        threads = []
        ports = self.get_open_ports()
        for port in ports:
            thread = threading.Thread(target=self.scan_port, args=(port,))
            threads.append(thread)
        for thread in threads:
            thread.start()
        for thread in threads:
            thread.join()



# TODO: Create save_results(target, results) function (Step vii)
# - Connect to scan_history.db
# - CREATE TABLE IF NOT EXISTS scans (id, target, port, status, service, scan_date)
# - INSERT each result with datetime.datetime.now()
# - Commit, close
# - Wrap in try-except for sqlite3.Error

def save_results(target, results):
    conn = sqlite3.connect("scan_history.db")
    cur = conn.cursor()

    if not os.path.isfile("scan_history.db"):
        cur.execute('''
            CREATE TABLE scans (
            id INTEGER PRIMARY KEY AUTOINCREMENT ,
            target TEXT,
            port INTEGER,
            status TEXT,
            service TEXT,
            scan_date TEXT
            )
        ''')



# TODO: Create load_past_scans() function (Step viii)
# - Connect to scan_history.db
# - SELECT all from scans
# - Print each row in readable format
# - Handle missing table/db: print "No past scans found."
# - Close connection


# ============================================================
# MAIN PROGRAM
# ============================================================
if __name__ == "__main__":
    pass
    # TODO: Get user input with try-except (Step ix)
    # - Target IP (default "127.0.0.1" if empty)
    # - Start port (1-1024)
    # - End port (1-1024, >= start port)
    # - Catch ValueError: "Invalid input. Please enter a valid integer."
    # - Range check: "Port must be between 1 and 1024."
    try:  
        target = input("enter a target IP address: (default is 127.0.0.1)") or "127.0.0.1"
        start_port = input("enter a start port between 1 and 1024:")
        end_port = input("enter a start port between 1 and 1024:")
    except ValueError as ex: 
        "Invalid input. Please enter a valid integer."

    # TODO: After valid input (Step x)
    # - Create PortScanner object
    # - Print "Scanning {target} from port {start} to {end}..."
    # - Call scan_range()
    # - Call get_open_ports() and print results
    # - Print total open ports found
    # - Call save_results()
    # - Ask "Would you like to see past scan history? (yes/no): "
    # - If "yes", call load_past_scans()

    ps1 = PortScanner(target)

    print(f"Scanning {target} from port {start_port} to {end_port}...")
    ps1.scan_range(start_port, end_port)
    open_ports = ps1.get_open_ports()

    print(f"--- Scan Results for {target} ---")
    for port in open_ports:
        print(f"Port: {port.port}: {port.status} ({port.service_name})")
    save_results(target, open_ports)


# Q5: New Feature Proposal
# TODO: Your 2-3 sentence description here... (Part 2, Q5)
# Diagram: See diagram_studentID.png in the repository root
