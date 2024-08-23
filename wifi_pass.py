import subprocess

def get_wifi_networks():
    try:
        output = subprocess.check_output(['netsh', 'wlan', 'show', 'profiles']).decode('utf-8', errors="backslashreplace").split('\n')
        profiles = [line.split(':')[1].strip() for line in output if "All User Profile" in line]
        return profiles
    
    except subprocess.CalledProcessError:
        return None

def get_wifi_password(profile):
    try:
        password_output = subprocess.check_output(['netsh', 'wlan', 'show', 'profile', profile, 'key=clear']).decode('utf-8', errors="backslashreplace").split('\n')
        password_lines = [line.split(':')[1].strip() for line in password_output if "Key Content" in line]
        password = password_lines[0] if len(password_lines) > 0 else None
        return password
    
    except subprocess.CalledProcessError:
        return None

# Step 1: Display available network names
networks = get_wifi_networks()

if networks:
    print("Available Wi-Fi networks:")
    for index, network in enumerate(networks):
        print(f"{index + 1}. {network}")
    print()
    
    # Step 2: Prompt user to choose a network or search for a network
    while True:
        choice = input("Enter the number of the network you want to view the password for, or enter a keyword to search (or 'q' to quit): ")
        if choice.lower() == 'q':
            print("Exiting the script.")
            break
        elif choice.isdigit() and 1 <= int(choice) <= len(networks):
            chosen_network = networks[int(choice) - 1]
            
            # Step 3: Retrieve and display password for the chosen network
            password = get_wifi_password(chosen_network)
            
            if password:
                print(f"Network: {chosen_network}")
                print(f"Password: {password}")
            else:
                print("Password not found for the chosen network.")
            breaks
        else:
            keyword = choice.lower()
            filtered_networks = [(index + 1, network) for index, network in enumerate(networks) if keyword in network.lower()]
            
            if filtered_networks:
                print(f"Matching networks for keyword '{keyword}':")
                for index, network in filtered_networks:
                    print(f"{index}. {network}")
                print()
            else:
                print(f"No networks found matching the keyword '{keyword}'. Please try again.")
else:
    print("Unable to retrieve available Wi-Fi networks.")
