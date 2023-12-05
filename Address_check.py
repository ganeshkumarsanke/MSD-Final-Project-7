
with open("trace_file_closed_mi.txt", 'r') as file:
    for line in file:
        # Split the line into individual components
        Time, core, operation, address = line.strip().split()

        Time = int(Time)

        # Decoding the hexadecimal address
        address = int(address, 16)
        address = bin(address)[2:].zfill(34)  # converting it to binary and making sure it's 34 bits

        row = hex(int(address[0:16], 2))  # hex only takes int as argument, [0:16]= 0-15 (16th bit is excluded)
        high_column_bits = hex(int(address[16:22], 2))
        bank = int(address[22:24], 2)
        bank_group = int(address[24:27], 2)

        print("For line at time: "+str(Time)+" Bank Group: "+str(bank_group)+" Bank: "+str(bank)+" Row : "+row+" High column bits: "+high_column_bits)
