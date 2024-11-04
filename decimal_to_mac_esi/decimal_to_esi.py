import sys

def decimal_to_esi(decimal):
    # Convert decimal to a 72-bit hexadecimal
    hex_value = f"{decimal:018x}"
    
    # Format the hex string as a ESI IDs (XX:XX:XX:XX:XX:XX:XX:XX:XX)
    # Manaully generated ESI's should always start with 00:
    esi = '00:' + ":".join(hex_value[i:i+2] for i in range(0, 18, 2))
    return esi

if __name__ == "__main__":
    # Get decimal input from the command line
    if len(sys.argv) != 2:
        print("Usage: python script.py <decimal_number>")
        sys.exit(1)

    try:
        decimal_input = int(sys.argv[1])
        if decimal_input < 0 or decimal_input > 4722366482869645213695:
            raise ValueError("The decimal number must be between 0 and 4722366482869645213695 (72-bit range).")
        
        esi = decimal_to_esi(decimal_input)
        print("ESI:", esi)
        
    except ValueError as e:
        print(f"Invalid input: {e}")
