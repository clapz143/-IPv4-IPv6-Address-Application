import requests
import argparse
import socket
import platform
import time

def get_ip_info(output_json=False):
    api_url = "https://ipapi.co/json/"  # No API key

    try:
        response = requests.get(api_url, timeout=10)

        # Handle HTTP 429 (Too Many Requests)
        if response.status_code == 429:
            print("Too many requests (HTTP 429). Retrying after 60 seconds...")
            time.sleep(60)  # Wait for 60 seconds before retrying
            response = requests.get(api_url, timeout=10)

        # Handle HTTP 403 (Forbidden)
        if response.status_code == 403:
            print("Access forbidden (HTTP 403). The free plan may have been blocked for your IP.")
            print("Consider using a VPN or switching to an API key for reliable access.")
            return

        if response.status_code != 200:
            print(f"Error: Received HTTP {response.status_code} from API.")
            return

        data = response.json()

        # Extracting information
        ipv4 = data.get('ip', 'N/A')
        country = data.get('country_name', 'N/A')
        region = data.get('region', 'N/A')
        city = data.get('city', 'N/A')
        isp = data.get('org', 'N/A')
        asn = data.get('asn', 'N/A')

        if output_json:
            print(data)
        else:
            console = Console()
            table = Table(title="IP Information")
            table.add_column("Attribute", style="cyan", no_wrap=True)
            table.add_column("Value", style="magenta")

            table.add_row("Public IPv4/IPv6", ipv4)
            table.add_row("Country", country)
            table.add_row("Region", region)
            table.add_row("City", city)
            table.add_row("ISP", isp)
            table.add_row("ASN", asn)

            console.print(table)

    except requests.exceptions.Timeout:
        print("Error: The request timed out. Please try again later.")
    except requests.exceptions.RequestException as e:
        print(f"Error fetching IP information: {e}")

def dns_lookup(domain):
    try:
        print(f"Performing DNS lookup for domain: {domain}")
        ip_address = socket.gethostbyname(domain)
        print(f"IP Address: {ip_address}")
    except socket.gaierror as e:
        print(f"DNS lookup failed for {domain}: {e}")
    except Exception as e:
        print(f"Unexpected error during DNS lookup: {e}")

def network_info():
    try:
        print("\nNetwork Interfaces and Addresses:")
        if platform.system() == "Windows":
            import psutil
            for interface, addrs in psutil.net_if_addrs().items():
                for addr in addrs:
                    if addr.family == psutil.AF_LINK:  # MAC Address
                        print(f"Interface: {interface}, MAC Address: {addr.address}")
        else:
            import os
            for interface in os.listdir('/sys/class/net/'):
                if interface != "lo":  # Skip loopback
                    ip_path = f"/sys/class/net/{interface}/address"
                    if os.path.exists(ip_path):
                        with open(ip_path, 'r') as file:
                            mac = file.read().strip()
                            print(f"Interface: {interface}, MAC Address: {mac}")

    except Exception as e:
        print(f"Error retrieving network information: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Fetch public IP, perform DNS lookups, and display network information.")
    parser.add_argument('--json', action='store_true', help="Output results in JSON format")
    parser.add_argument('--dns', type=str, help="Perform a DNS lookup for a domain")
    parser.add_argument('--network', action='store_true', help="Display detailed network information")
    args = parser.parse_args()

    if args.dns:
        dns_lookup(args.dns)
    elif args.network:
        network_info()
    else:
        get_ip_info(output_json=args.json)
