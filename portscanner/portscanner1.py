import argparse
import socket
from datetime import datetime
from termcolor import colored

def scan_port(target, port, timeout=1):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(timeout)
        result = s.connect_ex((target, port))
        if result == 0:
            return True
        else:
            return False
    except:
        return False

def scan_target(target, start_port, end_port, timeout):
    open_ports = []
    for port in range(start_port, end_port + 1):
        print(colored(f"Scanning port {port}...", "yellow"))
        if scan_port(target, port, timeout):
            open_ports.append(port)
    return open_ports

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Python port scanner')
    parser.add_argument('target', metavar='TARGET', type=str, help='The target to scan')
    parser.add_argument('--timeout', metavar='TIMEOUT', type=int, default=1, help='The connection timeout in seconds (default: 1)')
    args = parser.parse_args()

    target = socket.gethostbyname(args.target)
    timeout = args.timeout

    print(colored(r"""
                                  .                                                                                
                                .o8                                                                                
oo.ooooo.   .ooooo.  oooo d8b .o888oo       .oooo.o  .ooooo.   .oooo.   ooo. .oo.   ooo. .oo.    .ooooo.  oooo d8b 
 888' `88b d88' `88b `888""8P   888        d88(  "8 d88' `"Y8 `P  )88b  `888P"Y88b  `888P"Y88b  d88' `88b `888""8P 
 888   888 888   888  888       888        `"Y88b.  888        .oP"888   888   888   888   888  888ooo888  888     
 888   888 888   888  888       888 .      o.  )88b 888   .o8 d8(  888   888   888   888   888  888    .o  888     
 888bod8P' `Y8bod8P' d888b      "888"      8""888P' `Y8bod8P' `Y888""8o o888o o888o o888o o888o `Y8bod8P' d888b    
 888                                                                                                               
o888o  
    """, "cyan"))

    print(colored(f"Scanning target: {target}", "green"))
    print(colored(f"Time started: {datetime.now()}", "green"))
    print(colored("-" * 50, "yellow"))

    menu = """
    Please select an option:
    1. Scan all ports (1-65535)
    2. Scan well-known ports (1-10000)
    3. Scan a custom range of ports
    4. Scan a single custom port
    """

    print(colored(menu, "cyan"))
    option = input(colored("Option: ", "cyan"))

    if option == "1":
        start_port = 1
        end_port = 65535
    elif option == "2":
        start_port = 1
        end_port = 10000
    elif option == "3":
        custom_ports = input(colored("Enter the custom range of ports (start-end): ", "cyan"))
        start_port, end_port = map(int, custom_ports.split('-'))
    elif option == "4":
        custom_port = input(colored("Enter the custom port to scan: ", "cyan"))
        start_port = end_port = int(custom_port)

    open_ports = scan_target(target, start_port, end_port, timeout)

    if len(open_ports) == 0:
        print(colored("No open ports found.", "red"))
    else:
        for port in open_ports:
            print(colored(f"Port {port} is open", "green"))
