import requests

def get_ip_info():
    # API URL to get public IP info
    api_url = "https://ipapi.co/json/"
    
    try:
        # Send a request to the API
        response = requests.get(api_url)
        data = response.json()

        # Extracting relevant information
        ipv4 = data.get('ip', 'N/A')
        country = data.get('country_name', 'N/A')
        region = data.get('region', 'N/A')
        city = data.get('city', 'N/A')
        isp = data.get('org', 'N/A')
        asn = data.get('asn', 'N/A')

        # Display the extracted information
        print(f"Public IPv4/IPv6: {ipv4}")
        print(f"Country: {country}")
        print(f"Region: {region}")
        print(f"City: {city}")
        print(f"ISP: {isp}")
        print(f"ASN: {asn}")

    except requests.exceptions.RequestException as e:
        print(f"Error fetching IP information: {e}")

if __name__ == "__main__":
    get_ip_info()
