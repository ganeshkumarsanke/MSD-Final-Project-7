# --------------------------------------- Team 7 ------------------------------------------
# ------Authors: Ganeshkumar Sanke, Rakshita Joshi, Srikar Varma Datla, Vinay Sreedhara --------

trace_file_dictionary = {}
global cpu_cycles
global first_instruction
# ----------------------- Declaring Constants ---------------------------
tRC = 115
tRAS = 76
tRRD_L = 12
tRRD_S = 8
tRP = 39
tCWD = 38
tCL = 40
tRCD = 39
tWR = 30
tRTP = 18
tCCD_L = 12
tCCD_S = 8
tCCD_L_WR = 48
tCCD_S_WR = 8
tBURST = 8
tCCD_L_RTW = 16
tCCD_S_RTW = 16
tCCD_L_WTR = 70
tCCD_S_WTR = 52

# ------------------------ Conditional debugging -------------------------
DEBUG_MODE = input("enter the debug mode on/off")

if DEBUG_MODE == "on":
    file_name = input("enter the path of the file")
else:
    file_name = ("trace.txt")
with open(file_name, 'r') as file:
    for line in file:
        # ----------- Split the line into individual components ---------
        Time, core, operation, address = line.strip().split()
        Time = int(Time)

        # ------------- Decoding the hexadecimal address --------------
        address = int(address, 16)
        address = bin(address)[2:].zfill(34)

        # -- extracting row, high column, bank, and bank group bits --
        row = hex(int(address[0:16], 2))
        high_column_bits = hex(int(address[16:22], 2))
        bank = int(address[22:24], 2)
        bank_group = int(address[24:27], 2)

        # ---------- storing the values in a dictionary --------------
        if(Time in trace_file_dictionary.keys()):
          trace_file_dictionary[Time].append([int(core), operation, str(row), str(high_column_bits), str(bank), str(bank_group)])
        else:
          trace_file_dictionary[Time] = [[int(core), operation, str(row), str(high_column_bits), str(bank), str(bank_group)]]

p_bg = 100
p_b = 100
p_row = 00000000000
first_instruction = 1
last_cpu_cycles = 0

# --------------- Function to read the trace file instructions to use DRAM Commands --------------
def pop_add_retire_list(add_retire_list):
    global cpu_cycles
    # -------- Variables to maintain the previous status of bank groups, banks, and rows -------
    global p_bg
    global p_b
    global p_row
    global first_instruction
    global last_cpu_cycles
    if(len(add_retire_list)>0):
            retire_object = add_retire_list[0]
            # -------- retire_object[0] = time -----------
            # -------- retire_object[1] = core -----------
            # ------ retire_object[2] = operation --------
            # --------- retire_object[3] = row -----------
            # --- retire_object[4] = high_column_bits --
            # -- ------retire_object[5] = bank ---------
            # ------ retire_object[6] = bank group -------

            # ------------------------------- If Operation is Read ----------------------------------
            if(retire_object[2]=='0'):
                CurrentTime = int(cpu_cycles)

            # --------- check for same bank and bank group ------------
                if (int(p_bg) == int(retire_object[6]) and int(p_b) == int(retire_object[5])):

                    if int(cpu_cycles) - last_cpu_cycles >= (tRP * 2):
                        CurrentTime = int(cpu_cycles)
                    else:
                        CurrentTime = int(cpu_cycles) + tRP * 2

                    write_file.writelines((str(CurrentTime).zfill(16)).ljust(15) +" 0 ".ljust(10) +"ACT0 ".ljust(10) +retire_object[6].ljust(10)+retire_object[5].ljust(10)+retire_object[3][2:].ljust(10) +"\n")
                    CurrentTime = CurrentTime + 2

                    write_file.writelines((str(CurrentTime).zfill(16)).ljust(15)+" 0 ".ljust(10)+"ACT1 ".ljust(10)+retire_object[6].ljust(10)+retire_object[5].ljust(10)+retire_object[3][2:].ljust(10)+"\n")
                    CurrentTime = CurrentTime + (tRCD) * 2

                    write_file.writelines((str(CurrentTime).zfill(16)).ljust(15)+" 0 ".ljust(10)+"RD0 ".ljust(10)+retire_object[6].ljust(10)+retire_object[5].ljust(10)+retire_object[4][2:].ljust(10)+"\n")
                    CurrentTime = CurrentTime + 2

                    write_file.writelines((str(CurrentTime).zfill(16)).ljust(15)+" 0 ".ljust(10)+"RD1 ".ljust(10)+retire_object[6].ljust(10)+retire_object[5].ljust(10)+retire_object[4][2:].ljust(10)+"\n")
                    CurrentTime = CurrentTime + (tCL + tBURST) * 2

                    write_file.writelines((str(CurrentTime).zfill(16)).ljust(15)+" 0 ".ljust(10)+"PRE ".ljust(10)+retire_object[6].ljust(10)+retire_object[5].ljust(10)+"\n\n")

                    cpu_cycles = int(CurrentTime)
                    last_cpu_cycles = cpu_cycles

                    p_bg = retire_object[6]
                    p_b = retire_object[5]

                else:
                    if int(first_instruction) == 1:
                        CurrentTime = int(cpu_cycles)
                        first_instruction = 0

                    elif int(cpu_cycles) - last_cpu_cycles >= (tRP * 2):
                        CurrentTime = int(cpu_cycles)

                    else:
                        CurrentTime = int(cpu_cycles) + 2

                        write_file.writelines((str(CurrentTime).zfill(16)).ljust(15)+" 0 ".ljust(10) +"ACT0 ".ljust(10) +retire_object[6].ljust(10)+retire_object[5].ljust(10)+retire_object[3][2:].ljust(10)+"\n")
                        CurrentTime = CurrentTime + 2

                        write_file.writelines((str(CurrentTime).zfill(16)).ljust(15) +" 0 ".ljust(10) +"ACT1 ".ljust(10) +retire_object[6].ljust(10)+retire_object[5].ljust(10)+retire_object[3][2:].ljust(10)+"\n")

                        CurrentTime = CurrentTime + (tRCD) * 2

                        write_file.writelines((str(CurrentTime).zfill(16)).ljust(15)+" 0 ".ljust(10)+"RD0 ".ljust(10)+retire_object[6].ljust(10)+retire_object[5].ljust(10)+retire_object[4][2:].ljust(10)+"\n")
                        CurrentTime = CurrentTime + 2

                        write_file.writelines((str(CurrentTime).zfill(16)).ljust(15) +" 0 ".ljust(10) +"RD1 ".ljust(10) +retire_object[6].ljust(10)+retire_object[5].ljust(10)+retire_object[4][2:].ljust(10)+"\n")
                        CurrentTime = CurrentTime + (tCL + tBURST) * 2

                        write_file.writelines((str(CurrentTime).zfill(16)).ljust(15) +" 0 ".ljust(10) +"PRE ".ljust(10) +retire_object[6].ljust(10)+retire_object[5].ljust(10)+"\n\n")

                        cpu_cycles = int(CurrentTime)
                        last_cpu_cycles = cpu_cycles

                        p_bg = retire_object[6]
                        p_b = retire_object[5]

            # ------------------------------- If Operation is Write ----------------------------------
            elif(retire_object[2]=='1'):
            # --------- check for same bank and bank group ------------
                if int(p_bg) == int(retire_object[6]) and int(p_b) == int(retire_object[5]):

                    if int(cpu_cycles) - last_cpu_cycles >= (tRP * 2):
                        CurrentTime = int(cpu_cycles)
                    else:
                        CurrentTime = int(cpu_cycles) + tRP * 2

                    write_file.writelines((str(CurrentTime).zfill(16)).ljust(15)+ " 0 " .ljust(10) + "ACT0 ".ljust(10) + retire_object[6].ljust(10)+retire_object[5].ljust(10)+retire_object[3][2:].ljust(10)+"\n")
                    CurrentTime = CurrentTime + 2

                    write_file.writelines((str(CurrentTime).zfill(16)).ljust(15)+" 0 ".ljust(10)+ "ACT1 ".ljust(10)  + retire_object[6].ljust(10)+retire_object[5].ljust(10)+retire_object[3][2:].ljust(10)+"\n")

                    CurrentTime = CurrentTime + (tRCD) * 2

                    write_file.writelines((str(CurrentTime).zfill(16)).ljust(15)+" 0 ".ljust(10)+ "WR0 ".ljust(10)+retire_object[6].ljust(10) + retire_object[5].ljust(10)+retire_object[4][2:].ljust(10)+"\n")
                    CurrentTime = CurrentTime + 2

                    write_file.writelines((str(CurrentTime).zfill(16)).ljust(15)+" 0 ".ljust(10)+ "WR1 ".ljust(10)+retire_object[6].ljust(10)+retire_object[5].ljust(10)+retire_object[4][2:].ljust(10)+"\n")
                    CurrentTime = CurrentTime + (tCWD + tBURST) * 2

                    write_file.writelines((str(CurrentTime).zfill(16)).ljust(15)+" 0 ".ljust(10)+"PRE ".ljust(10)+ retire_object[6].ljust(10)+retire_object[5].ljust(10)+"\n\n")

                    cpu_cycles = int(CurrentTime)
                    last_cpu_cycles = cpu_cycles

                    p_bg = retire_object[6]
                    p_b = retire_object[5]

                else:
                    if int(first_instruction) == 1:
                        CurrentTime = int(cpu_cycles)
                        first_instruction = 0

                    elif int(cpu_cycles) - last_cpu_cycles >= (tRP * 2):
                        CurrentTime = int(cpu_cycles)

                    else:
                        CurrentTime = int(cpu_cycles) + 2

                    write_file.writelines((str(CurrentTime).zfill(16)).ljust(15)+" 0 ".ljust(10)+"ACT0 ".ljust(10)+retire_object[6].ljust(10)+retire_object[5].ljust(10)+retire_object[3][2:].ljust(10)+"\n")
                    CurrentTime = CurrentTime + 2

                    write_file.writelines((str(CurrentTime).zfill(16)).ljust(15)+" 0 ".ljust(10)+"ACT1 ".ljust(10)+retire_object[6].ljust(10)+retire_object[5].ljust(10)+retire_object[3][2:].ljust(10)+"\n")

                    CurrentTime = CurrentTime + (tRCD) * 2

                    write_file.writelines((str(CurrentTime).zfill(16)).ljust(15)+" 0 ".ljust(10)+"WR0 ".ljust(10)+retire_object[6].ljust(10)+retire_object[5].ljust(10)+retire_object[4][2:].ljust(10)+"\n")
                    CurrentTime = CurrentTime + 2

                    write_file.writelines((str(CurrentTime).zfill(16)).ljust(15)+" 0 ".ljust(10)+"WR1 ".ljust(10)+retire_object[6].ljust(10)+retire_object[5].ljust(10)+retire_object[4][2:].ljust(10)+"\n")
                    CurrentTime = CurrentTime + (tCWD + tBURST) * 2

                    write_file.writelines((str(CurrentTime).zfill(16)).ljust(15)+" 0 ".ljust(10)+"PRE ".ljust(10)+retire_object[6].ljust(10)+retire_object[5].ljust(10)+"\n\n")

                    cpu_cycles = int(CurrentTime)
                    last_cpu_cycles = cpu_cycles

                    p_bg = retire_object[6]
                    p_b = retire_object[5]

            # ------------------------------- If Operation is Instruction Fetch ----------------------------------
            elif(retire_object[2]=='2'):
            # --------- check for same bank and bank group ------------
                if (int(p_bg) == int(retire_object[6]) and int(p_b) == int(retire_object[5])):

                    if int(cpu_cycles) - last_cpu_cycles >= (tRP * 2):
                        CurrentTime = int(cpu_cycles)
                    else:
                        CurrentTime = int(cpu_cycles) + tRP * 2

                    write_file.writelines((str(CurrentTime).zfill(16)).ljust(15)+ " 0 ".ljust(10) + "ACT0 ".ljust(10) + retire_object[6].ljust(10)+retire_object[5].ljust(10)+retire_object[3][2:].ljust(10)+ "\n")
                    CurrentTime = CurrentTime + 2

                    write_file.writelines((str(CurrentTime).zfill(16)).ljust(15) + " 0 ".ljust(10) + "ACT1 ".ljust(10) + retire_object[6].ljust(10)+retire_object[5].ljust(10)+retire_object[3][2:].ljust(10)+"\n")

                    CurrentTime = CurrentTime + (tRCD) * 2

                    write_file.writelines((str(CurrentTime).zfill(16)).ljust(15) +" 0 ".ljust(10)+ "RD0 ".ljust(10)+ retire_object[6].ljust(10)+retire_object[5].ljust(10)+retire_object[4][2:].ljust(10)+"\n")
                    CurrentTime = CurrentTime + 2

                    write_file.writelines((str(CurrentTime).zfill(16)).ljust(15) + " 0 ".ljust(10)+"RD1 ".ljust(10) + retire_object[6].ljust(10)+retire_object[5].ljust(10)+retire_object[4][2:].ljust(10)+"\n")
                    CurrentTime = CurrentTime + (tCL + tBURST) * 2

                    write_file.writelines((str(CurrentTime).zfill(16)).ljust(15) + " 0 ".ljust(10) + "PRE ".ljust(10) + retire_object[6].ljust(10)+ retire_object[5].ljust(10)+"\n\n")

                    cpu_cycles = int(CurrentTime)
                    last_cpu_cycles = cpu_cycles

                    p_bg = retire_object[6]
                    p_b = retire_object[5]

                else :
                    if int(first_instruction) == 1:
                        CurrentTime = int(cpu_cycles)
                        first_instruction = 0

                    elif int(cpu_cycles) - last_cpu_cycles >= (tRP * 2):
                        CurrentTime = int(cpu_cycles)

                    else:
                        CurrentTime = int(cpu_cycles) + 2

                    write_file.writelines((str(CurrentTime).zfill(16)).ljust(15)+ " 0 ".ljust(10)+"ACT0 ".ljust(10)+retire_object[6].ljust(10)+retire_object[5].ljust(10)+retire_object[3][2:].ljust(10)+"\n")
                    CurrentTime = CurrentTime + 2

                    write_file.writelines((str(CurrentTime).zfill(16)).ljust(15)+ " 0 ".ljust(10)+"ACT1 ".ljust(10)+retire_object[6].ljust(10)+retire_object[5].ljust(10)+retire_object[3][2:].ljust(10)+"\n")

                    CurrentTime = CurrentTime + (tRCD) * 2

                    write_file.writelines((str(CurrentTime).zfill(16)).ljust(15)+ " 0 ".ljust(10)+"RD0 ".ljust(10)+retire_object[6].ljust(10)+retire_object[5].ljust(10)+retire_object[4][2:].ljust(10)+"\n")
                    CurrentTime = CurrentTime + 2

                    write_file.writelines((str(CurrentTime).zfill(16)).ljust(15)+ " 0 ".ljust(10)+"RD1 ".ljust(10)+retire_object[6].ljust(10)+retire_object[5].ljust(10)+retire_object[4][2:].ljust(10)+"\n")
                    CurrentTime = CurrentTime + (tCL + tBURST) * 2

                    write_file.writelines((str(CurrentTime).zfill(16)).ljust(15)+ " 0 ".ljust(10)+"PRE ".ljust(10)+retire_object[6].ljust(10)+retire_object[5].ljust(10)+"\n\n")

                    cpu_cycles = int(CurrentTime)
                    last_cpu_cycles = cpu_cycles

                    p_bg = retire_object[6]
                    p_b = retire_object[5]

            else:
                cpu_cycles += 2

            # ------ Retiring the entry from the main queue ------
            add_retire_list.remove(retire_object)

    # ------- if main queue has no entry, increment in the cpu cycles will be as follows: --------
    elif (len(add_retire_list) == 0):
        if (int(cpu_cycles) % 2 == 0):
            cpu_cycles += 2
        else:
            if (int(cpu_cycles) % 2 != 0):
                cpu_cycles += 1
            else:
                cpu_cycles += 2

sorted_times = sorted(trace_file_dictionary.keys())

sorted_list=[]

for i in sorted_times:
    sorted_list+= [[i]+j for j in sorted(trace_file_dictionary[i], key=lambda x: x[1])]

cpu_cycles = sorted_list[0][0]

add_retire_list=[]

# ----  Opening text file to output the DRAM Commands in ------
write_file = open("output_try.txt",'w+')

while(len(sorted_list)!=0):
    count=0

# ------ Moving entries from queue to the DIMM ------
    if(len(add_retire_list) >= 16):
        print("Queue is full, cannot add more items into the queue\n")
        pop_add_retire_list(add_retire_list)
    else:
        pop_add_retire_list(add_retire_list)

    for i in sorted_list:
    # ----- Insertion happens in main queue if instruction's time is lesser than cpu cycle or when len(queue) < 16 -----
        if(i[0] <= cpu_cycles and len(add_retire_list)<16):
            print("\nInsertion happened in queue at \n"+ str(cpu_cycles))
            add_retire_list+=[i]
            count+=1

    # ------ Sorted List truncated from the entry which has last been inserted into the queue ------
    sorted_list = sorted_list[count:]

    if(len(add_retire_list)!=0):
        print("Present status of queue")
    for i in add_retire_list:
        print(i)

# ----- Checking if the main queue is empty or not ------
while(len(add_retire_list)!=0):
    pop_add_retire_list(add_retire_list)

