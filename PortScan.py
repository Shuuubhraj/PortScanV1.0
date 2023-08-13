import socket
import sys

# Colors for formatting
GREEN = "\033[32m"
RED = "\033[31m"
WHITE = "\033[37m"
RESET = "\033[0m"

# Banner
banner = RED + """
██████╗  ██████╗ ██████╗ ████████╗███████╗ ██████╗ █████╗ ███╗   ██╗
██╔══██╗██╔═══██╗██╔══██╗╚══██╔══╝██╔════╝██╔════╝██╔══██╗████╗  ██║
██████╔╝██║   ██║██████╔╝   ██║   ███████╗██║     ███████║██╔██╗ ██║
██╔═══╝ ██║   ██║██╔══██╗   ██║   ╚════██║██║     ██╔══██║██║╚██╗██║
██║     ╚██████╔╝██║  ██║   ██║   ███████║╚██████╗██║  ██║██║ ╚████║
╚═╝      ╚═════╝ ╚═╝  ╚═╝   ╚═╝   ╚══════╝ ╚═════╝╚═╝  ╚═╝╚═╝  ╚═══╝  v1.0
""" + RESET + """
"""

# Your information
your_name = RED + "Rajput Shubhraj Singh" + RESET
your_github = RED + "@Shuuubhraj" + RESET

common_ports = {
    20: "FTP Data",
    21: "FTP Control",
    22: "SSH",
    23: "Telnet",
    25: "SMTP",
    53: "DNS",
    67: "DHCP Server",
    68: "DHCP Client",
    69: "TFTP",
    80: "HTTP",
    110: "POP3",
    115: "SFTP",
    123: "NTP",
    137: "NetBIOS Name Service",
    138: "NetBIOS Datagram Service",
    139: "NetBIOS Session Service",
    143: "IMAP",
    161: "SNMP",
    162: "SNMP Trap",
    389: "LDAP",
    443: "HTTPS",
    445: "Microsoft-DS (SMB)",
    465: "SMTP (SSL)",
    500: "ISAKMP",
    514: "Syslog",
    587: "SMTP (TLS/STARTTLS)",
    636: "LDAP (SSL/TLS)",
    873: "rsync",
    990: "FTPS (SSL/TLS)",
    993: "IMAPS",
    995: "POP3S",
    1433: "Microsoft SQL Server",
    3306: "MySQL",
    3389: "RDP",
    5900: "VNC",
    6667: "IRC",
    8000: "HTTP Alternate",
    8080: "HTTP Proxy",
    9090: "WebSM",
    9100: "JetDirect",
    10000: "Webmin/Web-based Admin",
    17185: "VNC",
    20000: "Usermin/Web-based User"
}

service_descriptions = {
    20: "FTP Data - File Transfer Protocol (Data Channel).\nAn unencrypted protocol used for transferring files.",
    21: "FTP Control - File Transfer Protocol (Control Channel).\nUsed to control FTP sessions and send commands.",
    22: "SSH - Secure Shell for secure remote access.\nProvides encrypted communication and secure command execution.",
    23: "Telnet - Unencrypted remote terminal access.\nNot recommended due to lack of security.",
    25: "SMTP - Simple Mail Transfer Protocol for email transmission.\nUsed to send emails between servers.",
    53: "DNS - Domain Name System for translating domain names to IP addresses.\nResolves human-readable domain names to IP addresses.",
    67: "DHCP Server - Dynamic Host Configuration Protocol (Server).\nAssigns IP addresses and network configuration to clients.",
    68: "DHCP Client - Dynamic Host Configuration Protocol (Client).\nRequests IP addresses and network configuration from servers.",
    69: "TFTP - Trivial File Transfer Protocol for basic file transfers.\nUsed for simple read and write operations.",
    80: "HTTP - Hypertext Transfer Protocol for web browsing.\nTransfers web pages and resources between clients and servers.",
    110: "POP3 - Post Office Protocol version 3 for receiving emails.\nDownloads emails from a server to a client.",
    115: "SFTP - Secure File Transfer Protocol for secure file transfers.\nUsed with SSH for encrypted data transmission.",
    123: "NTP - Network Time Protocol for clock synchronization.\nSynchronizes timekeeping among a set of distributed time servers.",
    137: "NetBIOS Name Service - Network Basic Input/Output System.\nResolves NetBIOS names to IP addresses.",
    138: "NetBIOS Datagram Service - Network Basic Input/Output System.\nSends and receives datagram packets for NetBIOS communication.",
    139: "NetBIOS Session Service - Network Basic Input/Output System.\nEstablishes and maintains connections between NetBIOS devices.",
    143: "IMAP - Internet Message Access Protocol for email retrieval.\nAllows multiple devices to access and manage the same mailbox.",
    161: "SNMP - Simple Network Management Protocol for network management.\nUsed to monitor and manage network devices.",
    162: "SNMP Trap - Simple Network Management Protocol for sending notifications.\nUsed to send alerts from devices to a central monitoring system.",
    389: "LDAP - Lightweight Directory Access Protocol for directory services.\nUsed to access and manage directory information.",
    443: "HTTPS - Hypertext Transfer Protocol Secure for secure web browsing.\nEncrypts web page data for secure communication.",
    445: "Microsoft-DS (SMB) - Microsoft Directory Services (Server Message Block).\nUsed for file, printer, and communication sharing in Windows networks.",
    465: "SMTP (SSL) - Simple Mail Transfer Protocol over SSL.\nEncrypted version of SMTP for secure email transmission.",
    500: "ISAKMP - Internet Security Association and Key Management Protocol.\nUsed to establish security associations and exchange keys.",
    514: "Syslog - System Logging Protocol for collecting and sending log messages.\nUsed for monitoring and troubleshooting.",
    587: "SMTP (TLS/STARTTLS) - Simple Mail Transfer Protocol with TLS/STARTTLS.\nEncrypted version of SMTP for secure email transmission.",
    636: "LDAP (SSL/TLS) - Lightweight Directory Access Protocol over SSL/TLS.\nSecure version of LDAP for encrypted directory access.",
    873: "rsync - Remote Sync for file synchronization.\nEfficiently transfers and synchronizes files between systems.",
    990: "FTPS (SSL/TLS) - FTP Secure with SSL/TLS.\nEncrypted version of FTP for secure file transfers.",
    993: "IMAPS - Internet Message Access Protocol over SSL.\nSecure version of IMAP for encrypted email retrieval.",
    995: "POP3S - Post Office Protocol version 3 over SSL.\nSecure version of POP3 for encrypted email retrieval.",
    1433: "Microsoft SQL Server - Database management system.\nUsed for managing and querying relational databases.",
    3306: "MySQL - Open-source relational database management system.\nUsed for storing and retrieving structured data.",
    3389: "RDP - Remote Desktop Protocol for remote access.\nAllows users to connect to a remote computer's desktop.",
    5900: "VNC - Virtual Network Computing for remote desktop access.\nAllows remote control of another computer's desktop.",
    6667: "IRC - Internet Relay Chat for online chat and communication.\nUsed for real-time text messaging and group discussions.",
    8000: "HTTP Alternate - Alternate port for HTTP communication.\nUsed when the standard HTTP port (80) is unavailable.",
    8080: "HTTP Proxy - HTTP proxy server for web requests.\nActs as an intermediary between clients and servers.",
    9090: "WebSM - Web-based System Manager for server administration.\nProvides a web interface for managing system settings.",
    9100: "JetDirect - HP JetDirect printing protocol.\nUsed for sending print jobs to network printers.",
    10000: "Webmin/Web-based Admin - Web-based system administration tool.\nAllows administrators to manage system settings via a web interface.",
    17185: "VNC - Virtual Network Computing for remote desktop access.\nAlternate port for VNC remote control.",
    20000: "Usermin/Web-based User - Web-based user interface for system administration.\nAllows users to manage their accounts and settings."
}



def check_port(ip, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(1)
    result = sock.connect_ex((ip, port))
    sock.close()
    return result == 0

def display_service_info(port):
    if port in service_descriptions:
        description = service_descriptions[port]
        lines = description.split("\n")
        for line in lines:
            print(GREEN + line.strip() + RESET)
    else:
        print(RED + "No information available for this service." + RESET)

def main():
    print(banner)
    print(f"By: {your_name}")
    print(f"GitHub: {your_github}\n")
    
    while True:
        target_ip = input(WHITE + "Enter the target IP address: " + RESET)

        print("\nScanning ports...\n")
        print(f"{'Port':<10} {'Service':<50} {'Status'}")
        print("-" * 70)

        for port, service in common_ports.items():
            status = GREEN + "Open" + RESET if check_port(target_ip, port) else RED + "Closed" + RESET
            print(f"{port:<10} {service:<50} {status}")

        print("\nResults for common ports displayed.\n")
        
        while True:
            print(RED + "Select an option:" + RESET)
            print("1. Exit")
            print("2. Manually check specific ports")
            print("3. Get Service Info")
            print("4. Check another IP")
            
            try:
                choice = int(input())
                if choice == 1:
                    sys.exit("\nExiting...")
                elif choice == 2:
                    port_to_check = int(input("Enter the port to check: "))
                    if check_port(target_ip, port_to_check):
                        print(f"Port {port_to_check} is {GREEN}open{RESET}.")
                    else:
                        print(f"Port {port_to_check} is {RED}closed{RESET}.")
                elif choice == 3:
                    port_to_info = int(input("Enter the port for service info: "))
                    display_service_info(port_to_info)
                elif choice == 4:
                    break
                else:
                    print(RED + "Invalid option. Please enter a valid option." + RESET)
            except KeyboardInterrupt:
                sys.exit("\nExiting...")
            except ValueError:
                print(RED + "Invalid input. Please enter a valid option." + RESET)

if __name__ == "__main__":
    main()
