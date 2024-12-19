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

def get_shared_virtual_k8s():
    """Fetch virtual K8s associated with the 'shared' namespace."""
    namespace_name = "shared"  # Name of the shared namespace
    headers = get_headers()  # Call the function to get headers
    
    # Endpoint for fetching virtual K8s for the 'shared' namespace
    url = f"{API_URL}/config/namespaces/{namespace_name}/virtual_k8ss"
    
    response = requests.get(url, headers=headers)

    # Log response details for debugging
    if response.status_code == 200:
        shared_virtual_k8s = response.json()  # Get all virtual K8s in shared
        # Extract and return just the names of the virtual K8s
        return {vk8s["name"] for vk8s in shared_virtual_k8s.get("items", [])}  # Use set for easy comparison
    else:
        raise Exception(f"Failed to fetch virtual K8s for namespace '{namespace_name}': {response.text}")

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

def get_virtual_k8s(namespace):
    """Fetch virtual K8s associated with a given namespace."""
    headers = get_headers()  # Call the function to get headers
    
    # Endpoint for fetching virtual K8s for a specific namespace
    url = f"{API_URL}/config/namespaces/{namespace}/virtual_k8ss"
    
    response = requests.get(url, headers=headers)

    # Log response details for debugging
    if response.status_code == 200:
        return response.json()  # Returns the JSON response containing virtual K8s
    else:
        raise Exception(f"Failed to fetch virtual K8s for namespace '{namespace}': {response.text}")

def main():
    try:
        # Step 1: Get all virtual K8s from the shared namespace
        shared_virtual_k8s = get_shared_virtual_k8s()  # Get names of virtual K8s in shared

        # Step 2: Get filtered namespaces (excluding 'shared')
        namespaces = get_namespaces()  # Fetch filtered namespaces

        # Check if namespaces are found
        if namespaces:  # Check if the list is not empty
            for ns in namespaces:
                namespace_name = ns["name"]  # Get the name of the namespace
                
                # Fetch virtual K8s for the current namespace
                virtual_k8s = get_virtual_k8s(namespace_name)
                
                # Check if virtual K8s are found and print them
                if "items" in virtual_k8s:
                    for vk8s in virtual_k8s["items"]:
                        # Only print virtual K8s that are NOT in the shared namespace
                        if vk8s["name"] not in shared_virtual_k8s:
                            print(f"{namespace_name}: {vk8s['name']}")
                else:
                    print(f"{namespace_name}: No virtual K8s found.")
        else:
            print("No namespaces found in tenant '{}'.".format(TENANT_NAME))
    
    except Exception as e:
        print("Error:", e)

if __name__ == "__main__":
    main()
