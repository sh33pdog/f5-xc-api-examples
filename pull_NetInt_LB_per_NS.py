import requests
import json

# Function to make API requests
def request(tenant, token, api):
    url = f'https://{tenant}.console.ves.volterra.io/api{api}'
    headers = {'Authorization': 'APIToken ' + token}
    response = requests.get(url, headers=headers)
    response.raise_for_status()  # Raise an error for bad response status
    return response.json()

# Main function
def main():
    # Collect input from the user
    tenant = input("\nEnter F5 XC Tenant: ").strip() or "my-tenant"
    token = input("\nEnter F5 XC Token: ").strip() or "my-token"

    try:
        # Fetch all namespaces for the given tenant
        namespaces_response = request(tenant, token, "/web/namespaces")
        namespaces = namespaces_response.get('items', [])
    except requests.exceptions.RequestException as e:
        print("Error fetching namespaces:", e)
        return

    # Iterate over each namespace
    for namespace in namespaces:
        namespace_name = namespace["name"]
        print("\nNamespace:", namespace_name)

        try:
            # Fetch network interfaces for the current namespace
            network_interfaces_response = request(tenant, token, f"/config/namespaces/{namespace_name}/network_interfaces")
            network_interfaces = network_interfaces_response.get('items', [])

            # Fetch load balancers for the current namespace
            loadbalancers_response = request(tenant, token, f"/config/namespaces/{namespace_name}/http_loadbalancers")
            loadbalancers = loadbalancers_response.get('items', [])
        except requests.exceptions.RequestException as e:
            print(f"Error fetching data for namespace {namespace_name}:", e)
            continue

        # Print network interfaces
        print("\nNetwork Interfaces:")
        if network_interfaces:
            for interface in network_interfaces:
                print("  -", interface["name"])
                # Print other information about the network interface here
        else:
            print("  No network interfaces found for this namespace.")

        # Print load balancers
        print("\nLoad Balancers:")
        if loadbalancers:
            for lb in loadbalancers:
                print("  -", lb["name"])
                # Print other information about the load balancer here
        else:
            print("  No load balancers found for this namespace.")

if __name__ == "__main__":
    main()
