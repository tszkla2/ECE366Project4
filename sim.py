def simulate(Instruction,Hex):
    mem_space = 4096
    Register = [0,0,0,0,0,0,0,0]
    Memory = [0 for i in range(mem_space)]
    PC = 0
    DIC = 0
    finished = False
    
    while(not(finished)):
    
        DIC += 1
        fetch = Instruction[PC]
    
        if (fetch[0:32] == '00010000000000001111111111111111'):
            print("PC =" + str(PC*4) + " Instruction: 0x" +  Hex[PC] + " : Deadloop.")
            finished = True

        elif (fetch[0:6] == '000000' and fetch[26:32] == '100000'): #add
            PC += 1
            Register[int(fetch[16:21],2)] = Register[int(fetch[6:11],2)] + Register[int(fetch[11:16],2)]

        elif (fetch[0:6] == '000000' and fetch[26:32] == '100010'): #sub
            PC += 1
            Register[int(fetch[16:21],2)] = Register[int(fetch[6:11],2)] - Register[int(fetch[11:16],2)]

        elif (fetch[0:6] == '000000' and fetch[26:32] == '100110'): #xor
            PC += 1
            Register[int(fetch[16:21],2)] = Register[int(fetch[6:11],2)] ^ Register[int(fetch[11:16],2)] 
           
        elif(fetch[0:6] == '001000'): #addi
            imm = int(fetch[16:32],2)
            PC += 1
            Register[int(fetch[11:16],2)] = Register[int(fetch[6:11],2)] + imm

        elif(fetch[0:6] == '000100'): #beq
            imm = int(fetch[16:32],2)
            PC += 1
            if (Register[int(fetch[6:11],2)] == Register[int(fetch[11:16],2)]):
                PC = PC + imm
            else:
                PC

        elif(fetch[0:6] == '000101'): #bne
            imm = int(fetch[16:32],2)
            PC += 1
            if (Register[int(fetch[6:11],2)] == Register[int(fetch[11:16],2)]):
                PC
            else:
                PC = PC + imm

        elif(fetch[0:6] == '000000' and fetch[26:32] == '101010'): #slt
            PC += 1
            if Register[int(fetch[6:11],2)] < Register[int(fetch[11:16],2)]:
                Register[int(fetch[16:21],2)] = 1
            else:
                0

        elif(fetch[0:6] == '100011'): #lw
            imm = int(fetch[16:32],2)
            PC += 1
            Register[int(fetch[11:16],2)] = Memory[imm + Register[int(fetch[6:11],2)] - 8192]

        elif(fetch[0:6] == '101011'): #sw
            imm = int(fetch[16:32],2)
            PC += 1
            Memory[imm + Register[int(fetch[6:11],2)] - 8192]= Register[int(fetch[11:16],2)]

 

    print("DIC: " +str(DIC))
    print("Registers: " + str(Register))
     
   


def main():
    I_file = open("i_mem.txt","r")
    Instruction = []             
    Hex = []
    for line in I_file:
        if (line == "\n" or line[0] =='#'):     
            continue
        line = line.replace('\n','')
        Hex.append(line)
        line = format(int(line,16),"032b")
        Instruction.append(line)
        
    
    simulate(Instruction,Hex)



if __name__ == "__main__":
    main()
