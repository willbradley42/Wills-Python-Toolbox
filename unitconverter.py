def dec_bin_hex(num, base):
    if base == 2:
        return bin(num)[2:]  # Convert to binary and remove '0b' prefix
    elif base == 16:
        return hex(num)[2:].upper()  # Convert to hexadecimal and remove '0x' prefix
    else:
        raise ValueError("Base must be either 2 (binary) or 16 (hexadecimal)")
    
