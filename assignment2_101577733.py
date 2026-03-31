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

    # Q3: 
    """
    The benefit of using the @property tag and the @target.setter are that they allow the getter and setter
    functions to have the same names as the actual field. In this case "target". 
    This creates simplification. It simplifies the code needed to access these getters and setters. It also allows
    one to obscure the real name of the field.
    """
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
# - scan_range(self, start_port, end_port):
#     - Create threads list
#     - Create Thread for each port targeting scan_port
#     - Start all threads (one loop)
#     - Join all threads (separate loop)


# Q1:
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

    # Q4: 
    """
    If you removed all try-except blocks from the scan_port method 
    and tried to scan a port on a machine that is not reachable that would cause the program to crash. An exception 
    would be raised and there would be nothing to catch it.

    """
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
    
    # Q2:
    """
    Using multiple threads for the purpose of scanning ports allows many ports to be scanned simultaneously,
    which greatly reduces the amount of time it takes.
    scanning 1024 ports without the use of threads would take much longer
    """
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

# I was not able to complete the SQL portions of this assignment.
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

def load_past_scans():
    pass



# ============================================================
# MAIN PROGRAM
# ============================================================
if __name__ == "__main__":
    pass
    try:  
        target = input("enter a target IP address: (default is 127.0.0.1)") or "127.0.0.1"
        start_port = input("enter a start port between 1 and 1024:")
        end_port = input("enter a start port between 1 and 1024:")
    except ValueError as ex: 
        "Invalid input. Please enter a valid integer."

    ps1 = PortScanner(target)

    print(f"Scanning {target} from port {start_port} to {end_port}...")
    ps1.scan_range(start_port, end_port)
    open_ports = ps1.get_open_ports()

    print(f"--- Scan Results for {target} ---")
    for port in open_ports:
        print(f"Port: {port.port}: {port.status} ({port.service_name})")
    # save_results(target, open_ports)
    # I unfortunately needed to comment our this line because I was not able to complete everything in time.

    try:  
        history = input("Would you like to see past scan history? (yes/no): ")
    except ValueError as ex: 
        "Invalid input. Please enter a valid input."

    # if history == "yes":
    #     load_past_scans()


# Q5: 
"""
One feature I would add is a feature that would allow the user to only save specific ports such as https or http.
This is a feature that could have value to users who are specifically looking for certain ports. 


I was not able to complete a diagram in time.
"""
