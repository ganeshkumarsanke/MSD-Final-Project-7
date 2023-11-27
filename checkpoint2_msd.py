trace_file_dictionary = {}
global cpu_cycles
DEBUG_MODE = input("enter the debug mode on/off")
if DEBUG_MODE == "on":
    file_name = input("enter the path of the file")
else:
    file_name = ("trace.txt")
with open(file_name, 'r') as file:
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
        if(Time in trace_file_dictionary.keys()):
          trace_file_dictionary[Time].append([int(core), operation, str(row), str(high_column_bits), str(bank), str(bank_group)])
        else:
          trace_file_dictionary[Time] = [[int(core), operation, str(row), str(high_column_bits), str(bank), str(bank_group)]]

def pop_add_retire_list(add_retire_list):
    if(len(add_retire_list)>0):
            retire_object = add_retire_list[0]
            if(retire_object[2]=='0'):
                write_file.writelines((str(cpu_cycles))+" 0 "+"ACT0 "+retire_object[6]+" "+retire_object[5]+" "+retire_object[3][2:]+"\n")
                write_file.writelines((str(cpu_cycles))+" 0 "+"ACT1 "+retire_object[6]+" "+retire_object[5]+" "+retire_object[3][2:]+"\n")
                write_file.writelines((str(cpu_cycles))+" 0 "+"RD0 "+retire_object[6]+" "+retire_object[5]+" "+retire_object[4][2:]+"\n")
                write_file.writelines((str(cpu_cycles))+" 0 "+"RD1 "+retire_object[6]+" "+retire_object[5]+" "+retire_object[4][2:]+"\n")
                write_file.writelines((str(cpu_cycles))+" 0 "+"PRE "+retire_object[6]+" "+retire_object[5]+" "+retire_object[3][2:]+"\n\n")
                """print((str(retire_object[0]).zfill(16))+" 0 "+"ACT0 "+retire_object[6]+" "+retire_object[5]+" "+retire_object[3][2:]+"\n")
                print((str(retire_object[0]).zfill(16))+" 0 "+"ACT1 "+retire_object[6]+" "+retire_object[5]+" "+retire_object[3][2:]+"\n")
                print((str(retire_object[0]).zfill(16))+" 0 "+"RD0 "+retire_object[6]+" "+retire_object[5]+" "+retire_object[4][2:]+"\n")
                print((str(retire_object[0]).zfill(16))+" 0 "+"RD1 "+retire_object[6]+" "+retire_object[5]+" "+retire_object[4][2:]+"\n")
                print((str(retire_object[0]).zfill(16))+" 0 "+"PRE "+retire_object[6]+" "+retire_object[5]+" "+retire_object[3][2:]+"\n")"""
            elif(retire_object[2]=='1'):
                write_file.writelines((str(cpu_cycles))+" 0 "+"ACT0 "+retire_object[6]+" "+retire_object[5]+" "+retire_object[3][2:]+"\n")
                write_file.writelines((str(cpu_cycles))+" 0 "+"ACT1 "+retire_object[6]+" "+retire_object[5]+" "+retire_object[3][2:]+"\n")
                write_file.writelines((str(cpu_cycles))+" 0 "+"WR0 "+retire_object[6]+" "+retire_object[5]+" "+retire_object[4][2:]+"\n")
                write_file.writelines((str(cpu_cycles))+" 0 "+"WR1 "+retire_object[6]+" "+retire_object[5]+" "+retire_object[4][2:]+"\n")
                write_file.writelines((str(cpu_cycles))+" 0 "+"PRE "+retire_object[6]+" "+retire_object[5]+" "+retire_object[3][2:]+"\n\n")
                """print(str(retire_object[0])+" 0 "+"ACT0 "+retire_object[6]+" "+retire_object[5]+" "+retire_object[3][2:]+"\n")
                print(str(retire_object[0])+" 0 "+"ACT1 "+retire_object[6]+" "+retire_object[5]+" "+retire_object[3][2:]+"\n")
                print(str(retire_object[0])+" 0 "+"WR0 "+retire_object[6]+" "+retire_object[5]+" "+retire_object[4][2:]+"\n")
                print(str(retire_object[0])+" 0 "+"WR1 "+retire_object[6]+" "+retire_object[5]+" "+retire_object[4][2:]+"\n")
                print(str(retire_object[0])+" 0 "+"PRE "+retire_object[6]+" "+retire_object[5]+" "+retire_object[3][2:]+"\n")"""
            elif(retire_object[2]=='2'):
                write_file.writelines((str(cpu_cycles))+" 0 "+"ACT0 "+retire_object[6]+" "+retire_object[5]+" "+retire_object[3][2:]+"\n")
                write_file.writelines((str(cpu_cycles))+" 0 "+"ACT1 "+retire_object[6]+" "+retire_object[5]+" "+retire_object[3][2:]+"\n")
                write_file.writelines((str(cpu_cycles))+" 0 "+"IF0 "+retire_object[6]+" "+retire_object[5]+" "+retire_object[4][2:]+"\n")
                write_file.writelines((str(cpu_cycles))+" 0 "+"IF1 "+retire_object[6]+" "+retire_object[5]+" "+retire_object[4][2:]+"\n")
                write_file.writelines((str(cpu_cycles))+" 0 "+"PRE "+retire_object[6]+" "+retire_object[5]+" "+retire_object[3][2:]+"\n\n")
                """print(str(retire_object[0])+" 0 "+"ACT0 "+retire_object[6]+" "+retire_object[5]+" "+retire_object[3][2:]+"\n")
                print(str(retire_object[0])+" 0 "+"ACT1 "+retire_object[6]+" "+retire_object[5]+" "+retire_object[3][2:]+"\n")
                print(str(retire_object[0])+" 0 "+"IF0 "+retire_object[6]+" "+retire_object[5]+" "+retire_object[4][2:]+"\n")
                print(str(retire_object[0])+" 0 "+"IF1 "+retire_object[6]+" "+retire_object[5]+" "+retire_object[4][2:]+"\n")
                print(str(retire_object[0])+" 0 "+"PRE "+retire_object[6]+" "+retire_object[5]+" "+retire_object[3][2:]+"\n")"""

            add_retire_list.remove(retire_object)

sorted_times = sorted(trace_file_dictionary.keys())
sorted_list=[]
for i in sorted_times:
    sorted_list+= [[i]+j for j in sorted(trace_file_dictionary[i], key=lambda x: x[1])]
#print(sorted_list)
cpu_cycles,dimm_cycles = sorted_list[0][0],int(sorted_list[0][0])//2
add_retire_list=[]

write_file = open("final23.txt",'w+')

while(len(sorted_list)!=0):
    count=0
    # cpu_cycles+=2
    # dimm_cycles+=1
    if(len(add_retire_list) >=16):
        print("queue is full,  cannot add more items into the queue\n")
        pop_add_retire_list(add_retire_list)
    else:
        pop_add_retire_list(add_retire_list)
    for i in sorted_list:
        if(i[0]<=cpu_cycles and len(add_retire_list)<16):
            print("\nInsertion happened in queue at "+ str(i[0]))
            add_retire_list+=[i]
            count+=1
    sorted_list=sorted_list[count:]
    if(len(add_retire_list)!=0):
        print("Present status of queue\n")
    for i in add_retire_list:
        print(i)
    print("\nCPU cycles are "+str(cpu_cycles))

    cpu_cycles += 2
    dimm_cycles += 1

while(len(add_retire_list)!=0):
    pop_add_retire_list(add_retire_list)


