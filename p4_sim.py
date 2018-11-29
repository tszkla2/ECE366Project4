mem_space = 4096

def simulate(Instruction,Hex):
    Register = [0,0,0,0,0,0,0,0]
    Memory = [0 for i in range(mem_space)]
    Cycle = 0
    Cycle_count = 1
    Cycle_3 = 0
    Cycle_4 = 0
    Cycle_5 = 0
    PC = 0
    DIC = 0
    Pipeline = 0

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
            Register[int(fetch[11:16],2)] = Memory[imm + Register[int(fetch[6:11],2)] - 8192]

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
            Memory[imm + Register[int(fetch[6:11],2)] - 8192]= Register[int(fetch[11:16],2)]

    print("DIC: "+str(DIC))
    print("Single Cycle: " + str(DIC))
    print("Multi Cycle: " + str(Cycle))
    print("Pipeline Cycle: " + str(Pipeline))
    print("3 Step Cycles: " + str(Cycle_3))
    print("4 Step Cycles: " + str(Cycle_4))
    print("5 Step Cycles: " + str(Cycle_5))
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
     
def main():
    I_file = open("i_mem_test.txt","r")     #Change file name to change input file
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
