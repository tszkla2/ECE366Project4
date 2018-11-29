import math
mem_size = 4096
total_blocks = 8
block_size = 32
offset = int(math.log(total_blocks,2))


def simulate(Instruction,Hex):
    Register = [0,0,0,0,0,0,0,0]
    Memory = [0 for i in range(mem_size)]
    Cycle = 0
    Cycle_count = 1
    Cycle_3 = 0
    Cycle_4 = 0
    Cycle_5 = 0
    PC = 0
    DIC = 0
    Pipeline = 0
    lw_use = 0
    compute_branch = 0
    branch_flush = 0

    Cache =  [0 for i in range(total_blocks)]
    Valid =  [0 for i in range(total_blocks)]
    Tag   =  ['0' for i in range(total_blocks)]
    Hit = 0
    Miss = 0
    
    finished = False

    while(not(finished)):
    
        DIC += 1

        fetch = Instruction[PC]
    
        if (fetch[0:32] == '00010000000000001111111111111111'): #endless beq loop
            print("PC: " + str(PC*4) + " Instruction: 0x" + Hex[PC] + " :Deadloop \n")
            Cycle += 3
            Cycle_count += 3
            Cycle_3 += 1
            Pipeline += 1   
            Pipeline += 4   #Last Instruction
            finished = True
            
        elif (fetch[0:6] == '000000' and fetch[26:32] == '100000'): #add
            print("Cycles: " + str(Cycle_count))
            print("PC: " + str(PC*4) + " Instruction: 0x" + Hex[PC] + " :" + "add $" + str(int(fetch[16:21],2)) + ",$" +str(int(fetch[6:11],2)) + ",$" + str(int(fetch[11:16],2)) )
            print("Taking 4 cycles \n")
            PC += 1
            Cycle += 4
            Cycle_count += 4
            Cycle_4 += 1
            Pipeline += 1
            Register[int(fetch[16:21],2)] = Register[int(fetch[6:11],2)] + Register[int(fetch[11:16],2)]

        elif (fetch[0:6] == '000000' and fetch[26:32] == '100010'): #sub
            print("Cycles: " + str(Cycle_count))
            print("PC: " + str(PC*4) + " Instruction: 0x" + Hex[PC] + " :" + "sub $" + str(int(fetch[16:21],2)) + ",$" +str(int(fetch[6:11],2)) + ",$" + str(int(fetch[11:16],2)) )
            print("Taking 4 cycles \n")
            PC += 1
            Cycle += 4
            Cycle_count += 4
            Cycle_4 += 1
            Pipeline += 1
            Register[int(fetch[16:21],2)] = Register[int(fetch[6:11],2)] - Register[int(fetch[11:16],2)]

        elif (fetch[0:6] == '000000' and fetch[26:32] == '100110'): #xor
            print("Cycles: " + str(Cycle_count))
            print("PC: " + str(PC*4) + " Instruction: 0x" + Hex[PC] + " :" + "xor $" + str(int(fetch[16:21],2)) + ",$" +str(int(fetch[6:11],2)) + ",$" + str(int(fetch[11:16],2)) )
            print("Taking 4 cycles \n")
            PC += 1
            Cycle += 4
            Cycle_count += 4
            Cycle_4 += 1
            Pipeline += 1
            Register[int(fetch[16:21],2)] = Register[int(fetch[6:11],2)] ^ Register[int(fetch[11:16],2)] 
           
        elif(fetch[0:6] == '001000'): #addi
            if (fetch[16]=='0'):
                imm = int(fetch[16:32],2)
            else:
                imm = -1*(65535 -int(fetch[16:32],2)+1)
            print("Cycles: " + str(Cycle_count))
            print("PC: " + str(PC*4) + " Instruction: 0x" + Hex[PC] + " :" + "addi $" + str(int(fetch[11:16],2)) + ",$" +str(int(fetch[6:11],2)) + "," + str(imm) )
            print("Taking 4 cycles \n")
            PC += 1
            Cycle += 4
            Cycle_count += 4
            Cycle_4 += 1
            Pipeline += 1
            Register[int(fetch[11:16],2)] = Register[int(fetch[6:11],2)] + imm

        elif(fetch[0:6] == '000100'): #beq
            if (fetch[16]=='0'):
                imm = int(fetch[16:32],2)
            else:
                imm = -1*(65535-int(fetch[16:32],2)+1)
            print("Cycles: " + str(Cycle_count))
            print("PC: " + str(PC*4) + " Instruction: 0x" + Hex[PC] + " :" + "beq $" + str(int(fetch[6:11],2)) + ",$" +str(int(fetch[11:16],2)) + "," + str(imm) )
            print("Taking 3 cycles \n")
            PC += 1
            Cycle += 3
            Cycle_count += 3
            Cycle_3 += 1
            Pipeline += 1
            if (Register[int(fetch[6:11],2)] == Register[int(fetch[11:16],2)]):
                PC = PC + imm
            else:
                PC = PC

        elif(fetch[0:6] == '000101'): #bne
            if (fetch[16]=='0'):
                imm = int(fetch[16:32],2)
            else:
                imm = -1*(65535-int(fetch[16:32],2)+1)
            print("Cycles: " + str(Cycle_count))
            print("PC: " + str(PC*4) + " Instruction: 0x" + Hex[PC] + " :" + "bne $" + str(int(fetch[6:11],2)) + ",$" +str(int(fetch[11:16],2)) + "," + str(imm) )
            print("Taking 3 cycles \n")
            PC += 1
            Cycle += 3
            Cycle_count += 3
            Cycle_3 += 1
            Pipeline += 1
            if (Register[int(fetch[6:11],2)] != Register[int(fetch[11:16],2)]):
                PC = PC + imm
            else:
                PC = PC

        elif(fetch[0:6] == '000000' and fetch[26:32] == '101010'): #slt
            print("Cycles: " + str(Cycle_count))
            print("PC: " + str(PC*4) + " Instruction: 0x" + Hex[PC] + " :" + "slt $" + str(int(fetch[16:21],2)) + ",$" +str(int(fetch[6:11],2)) + ",$" + str(int(fetch[11:16],2)) )
            print("Taking 4 cycles \n")
            PC += 1
            Cycle += 4
            Cycle_count += 4
            Cycle_4 += 1
            Pipeline += 1
            if Register[int(fetch[6:11],2)] < Register[int(fetch[11:16],2)]:
                Register[int(fetch[16:21],2)] = 1
            else:
                Register[int(fetch[16:21],2)] = 0

        elif(fetch[0:6] == '100011'): #lw
            imm = int(fetch[16:32],2)
            print("Cycles: " + str(Cycle_count))
            print("PC: " + str(PC*4) + " Instruction: 0x" + Hex[PC] + " :" + "lw $" + str(int(fetch[11:16],2)) + "," + hex(imm) + "($" + str(int(fetch[6:11],2)) + ")" )
            print("Taking 5 cycles \n")
            PC += 1
            Cycle += 5
            Cycle_count += 5
            Cycle_5 += 1
            Pipeline += 1
            
            temp = int(fetch[32-offset-2:32-2],2)
            
            if (Valid[temp] == 0):  #Miss
                Miss += 1
                Cache[temp] = Memory[imm + Register[int(fetch[6:11],2)] - 8192]
                Register[int(fetch[11:16],2)] = Cache[temp]
                Valid[temp] = 1    #Valid = 1
                Tag[temp] = fetch[16:32-offset-2]
            else: #Valid = 1
                if(Tag[temp] == fetch[16:32-offset-2]): #Hit
                    Hit += 1
                    Register[int(fetch[11:16],2)] = Cache[temp]
                else:   #Miss
                    Miss += 1
                    Cache[temp] = Memory[imm + Register[int(fetch[6:11],2)] - 8192]
                    Register[int(fetch[11:16],2)] = Cache[temp]
                    Tag[temp] = fetch[16:32-offset-2]
          

        elif(fetch[0:6] == '101011'): #sw
            imm = int(fetch[16:32],2)
            print("Cycles: " + str(Cycle_count))
            print("PC: " + str(PC*4) + " Instruction: 0x" + Hex[PC] + " :" + "sw $" + str(int(fetch[11:16],2)) + "," + hex(imm) + "($" + str(int(fetch[6:11],2)) + ")" )
            print("Taking 4 cycles \n")
            PC += 1
            Cycle += 4
            Cycle_count += 4
            Cycle_4 += 1
            Pipeline += 1

            #temp = int(fetch[32-offset-2:32-2],2)
            
            #if (Valid[temp] == 0):  #Miss
            #    Miss += 1
            #    Memory[imm + Register[int(fetch[6:11],2)] - 8192] = Register[int(fetch[11:16],2)]
            #    Cache[temp] = Register[int(fetch[11:16],2)]
            #    Valid[temp] = 1
            #    Tag[temp] = fetch[16:32-offset-2]
            #else:   #Valid = 1
            #   if(Tag[temp] == fetch[16:32-offset-2]):     #Hit
            #        Hit += 1
            #        Cache[temp] = Register[int(fetch[11:16],2)] 
            #    else:   #Miss
            #        Miss += 1
            #        Memory[imm + Register[int(fetch[6:11],2)] - 8192] = Register[int(fetch[11:16],2)]
            #        Cache[temp] = Register[int(fetch[11:16],2)]
            #        Tag[temp] = fetch[16:32-offset-2]

    print("---------------------------------")
    print("DIC: "+str(DIC))
    print("Single Cycle: " + str(DIC))
    print("Multi Cycle: " + str(Cycle))
    print("Pipeline Cycle: " + str(Pipeline))
    print("3 Step Cycles: " + str(Cycle_3))
    print("4 Step Cycles: " + str(Cycle_4))
    print("5 Step Cycles: " + str(Cycle_5))
    print("\n")
    print("Hit: " + str(Hit))
    print("Miss: " + str(Miss))
    if(Hit == 0):
        print("Hitrate: 0") 
    else:
        print("Hitrate: " + str(100*(float(Hit)/float(Hit + Miss))) + "%")
        
    print("\n")
    print("Registers: ")
    print("$0: " + str(Register[0]))
    print("$1: " + str(Register[1]))
    print("$2: " + str(Register[2]))
    print("$3: " + str(Register[3]))
    print("$4: " + str(Register[4]))
    print("$5: " + str(Register[5]))
    print("$6: " + str(Register[6]))
    print("$7: " + str(Register[7]))
    print("PC: " + str(PC*4))
    print("\n")
    print("Cache: " + str(Cache))
    print("Valid: " + str(Valid))
    print("Tag: " + str(Tag))
    #print("Memory: " + str(Memory))
     
def main():
    I_file = open("i_mem_A1.txt","r")     #Change file name to change input file
    Instruction = []             
    Hex = []
    for line in I_file:
        if (line == "\n" or line[0] =='#'):     
            continue
        line = line.replace('0x', '')
        line = line.replace('\n','')
        Hex.append(line)
        line = format(int(line,16),"032b")
        Instruction.append(line)
        
    simulate(Instruction,Hex)

if __name__ == "__main__":
    main()
