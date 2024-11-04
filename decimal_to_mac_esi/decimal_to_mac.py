import sys

def decimal_to_mac(decimal):
    # Convert decimal to a 48-bit hexadecimal (12 hex digits)
    hex_value = f"{decimal:012x}"
    
    # Format the hex string as a MAC address (XX:XX:XX:XX:XX:XX)
    mac_address = ":".join(hex_value[i:i+2] for i in range(0, 12, 2))
    return mac_address

if __name__ == "__main__":
    # Get decimal input from the command line
    if len(sys.argv) != 2:
        print("Usage: python script.py <decimal_number>")
        sys.exit(1)

    try:
        decimal_input = int(sys.argv[1])
        if decimal_input < 0 or decimal_input > 281474976710655:
            raise ValueError("The decimal number must be between 0 and 281474976710655 (48-bit range).")
        
        mac_address = decimal_to_mac(decimal_input)
        print("MAC Address:", mac_address)
        
    except ValueError as e:
        print(f"Invalid input: {e}")
