import requests

# Constants
TENANT_NAME = "f5-emea-ent"  # The tenant from which we want to fetch namespaces
API_URL = f"https://{TENANT_NAME}.console.ves.volterra.io/api"  # Base API URL
API_TOKEN = "ADD_YOUR_API_TOKEN_HERE"  # Replace with your F5 API token

def get_headers():
    """Function to generate headers using API Token."""
    return {
        "Authorization": f"APIToken {API_TOKEN}",  # Correct format for the API token
        "Content-Type": "application/json",
    }

def get_shared_app_firewalls():
    """Fetch application firewalls associated with the 'shared' namespace."""
    namespace_name = "shared"  # Name of the shared namespace
    headers = get_headers()  # Call the function to get headers
    
    # Endpoint for fetching app firewalls for the 'shared' namespace
    url = f"{API_URL}/config/namespaces/{namespace_name}/app_firewalls"
    
    response = requests.get(url, headers=headers)

    # Log response details for debugging
    if response.status_code == 200:
        shared_firewalls = response.json()  # Get all app firewalls in shared
        # Extract and return just the names of the app firewalls
        return {af["name"] for af in shared_firewalls.get("items", [])}  # Use set for easy comparison
    else:
        raise Exception(f"Failed to fetch app firewalls for namespace '{namespace_name}': {response.text}")

def get_namespaces():
    """Fetch all namespaces in the specified tenant, excluding 'shared'."""
    headers = get_headers()  # Call the function to get headers
    
    # Endpoint for fetching namespaces
    url = f"{API_URL}/web/namespaces"  
    
    response = requests.get(url, headers=headers)

    # Log response details for debugging
    if response.status_code == 200:
        all_namespaces = response.json()  # Get all namespaces
        # Filter out the 'shared' namespace
        filtered_namespaces = [ns for ns in all_namespaces.get("items", []) if ns["name"].lower() != "shared"]
        return filtered_namespaces  # Return only the filtered namespaces
    else:
        raise Exception(f"Failed to fetch namespaces: {response.text}")

def get_app_firewalls(namespace):
    """Fetch application firewalls associated with a given namespace."""
    headers = get_headers()  # Call the function to get headers
    
    # Endpoint for fetching app firewalls for a specific namespace
    url = f"{API_URL}/config/namespaces/{namespace}/app_firewalls"
    
    response = requests.get(url, headers=headers)

    # Log response details for debugging
    if response.status_code == 200:
        return response.json()  # Returns the JSON response containing app firewalls
    else:
        raise Exception(f"Failed to fetch app firewalls for namespace '{namespace}': {response.text}")

def main():
    try:
        # Step 1: Get all app firewalls from the shared namespace
        shared_app_firewalls = get_shared_app_firewalls()  # Get names of app firewalls in shared

        # Step 2: Get filtered namespaces (excluding 'shared')
        namespaces = get_namespaces()  # Fetch filtered namespaces

        # Check if namespaces are found
        if namespaces:  # Check if the list is not empty
            for ns in namespaces:
                namespace_name = ns["name"]  # Get the name of the namespace
                
                # Fetch app firewalls for the current namespace
                app_firewalls = get_app_firewalls(namespace_name)
                
                # Check if app firewalls are found and print them
                if "items" in app_firewalls:
                    for af in app_firewalls["items"]:
                        # Only print app firewalls that are NOT in the shared namespace
                        if af["name"] not in shared_app_firewalls:
                            print(f"{namespace_name}: {af['name']}")
                else:
                    print(f"{namespace_name}: No app firewalls found.")
        else:
            print("No namespaces found in tenant '{}'.".format(TENANT_NAME))
    
    except Exception as e:
        print("Error:", e)

if __name__ == "__main__":
    main()
