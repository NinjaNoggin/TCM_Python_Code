import subprocess
import ipaddress

def scan_network(gateway, subnet_mask):
    """
    Scans the home network for online hosts using ping.

    Args:
        gateway: The IP address of your network gateway.
        subnet_mask: The subnet mask for your network.

    Returns:
        A list of IP addresses of online hosts.
    """

    online_hosts = []
    network = ipaddress.ip_network(f"{gateway}/{subnet_mask}", strict=False)

    for host in network:
        if host != ipaddress.ip_network(f"{gateway}/{subnet_mask}", strict=False):  # Exclude the network address itself
            try:
                # Use subprocess to execute the ping command.  -c 1 is for one ping.  -w 1 is for a 1-second timeout.
                process = subprocess.run(["ping", "-c", "1", "-w", "1", str(host)],
                                        stdout=subprocess.DEVNULL,  # Suppress output
                                        stderr=subprocess.DEVNULL, # Suppress errors
                                        timeout=2) # Add a timeout to prevent hangs

                if process.returncode == 0:  # Ping was successful
                    online_hosts.append(str(host))
            except subprocess.TimeoutExpired:
                # Host timed out, consider it offline
                pass
            except Exception as e:
                print(f"Error pinging {host}: {e}")

    return online_hosts


if __name__ == "__main__":
    gateway_ip = "10.0.0.1"
    subnet_mask = "255.255.255.0"

    online_hosts = scan_network(gateway_ip, subnet_mask)

    if online_hosts:
        print("Online hosts:")
        for host in online_hosts:
            print(host)
    else:
        print("No online hosts found.")