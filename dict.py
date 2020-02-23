




def stripComments(line):
    if not line:
        return ''

    cleaned = line
    if line.find('#') != -1:
        cleaned = line[0:line.find('#')]  # Get rid of anything after a comment(#).
    return cleaned

def mergeInputFiles(filename):  # given list of all input lines
    outlines = []
    with open(filename) as f:
        outlines += f.readlines()

        f.close()

    return outlines

def buildTextMap(lines):
    labelsMap = {}
    count = 10000000
    for lineNo, line in enumerate(lines):
        split = line.split(':', 1)
        if len(split) == 1:
            label = split[0].strip()
            labelsMap[count] = label
            count = count + 4

    return labelsMap

def buildDataMap(lines):
    labelsMap = {}
    count = 400000
    for lineNo, line in enumerate(lines):
        split = line.split(':', 1)
        if len(split) > 1:
            label = split[1].strip()
            labelsMap[count] = label
            count = count + 4

    return labelsMap

def maps(lines):

    dataMap = buildDataMap(lines)
    textMap = buildTextMap(lines)
    fullMap = {**dataMap, **textMap}
    return dataMap, textMap, fullMap



REG = [0]*32
REG[0]=1
REG[1]=1
REG[2]=1
REG[3]=1
REG[4]=1
REG[5]=5
REG[6]=1




inline=mergeInputFiles('testsim1.txt')
lines = list(map(lambda line:stripComments(line.rstrip()), inline))

print(lines)
dataMap,textMap,fullMap=maps(lines)
print(dataMap)
print(textMap)
print(fullMap)
pc=10000000
for pc in range(10000000,len(textMap)*4+10000000,4):
    print(textMap[pc])
'''for sline in lines:
    print(sline[6:21])
'''
print("######################################################")
print((len(textMap)-1)*4+10000000)
while (pc<=(len(textMap)-1)*4+10000000):

   # if (pc > (len(textMap)-1) * 4 + 10000000):
   #     break
    sline=textMap[pc]
    opcode = sline[0:6]

    print(opcode)
    if opcode == '011111':

        operand = []
        register = []
        for x in range(6,21,5):
            operand.append(sline[x:x+5])
        #print(operand)
        for i in range(3):
            register.append(int(operand[i],2))
        print(register)
        # print(sline[22:31])
        if sline[22:31] == '100001010':            #add
            REG[register[0]] = REG[register[1]] + REG[register[2]]
            print('add')
        elif sline[22:31] == '000101000' :          #subf
            REG[register[0]] = REG[register[2]] - REG[register[1]]
            print('sub')
        elif sline[21:30] == '0000011100' :         #and
            REG[register[1]] = REG[register[0]] & REG[register[2]]
            print('and')
        elif  sline[21:30] == '0110111100' :        #or
            REG[register[1]] = REG[register[0]] | REG[register[2]]
            print('or')
    elif opcode == '001110' :   #addi
        operand = []
        register = []
        for x in range(6,16,5):
            operand.append(sline[x:x + 5])
        #print(operand)
        for i in range(2):
            register.append(int(operand[i], 2))
        #print(register)
        #print(sline[16:])
        d = int(sline[16:],2)
        REG[register[0]] = REG[register[1]] + d
   # elif opcode == '111010' :
    elif opcode =='010011':      #bca

        operand=[]
        register=[]
        for x in range(6,16,5):
            operand.append(sline[x:x+5])
        for i in range(2):
            register.append(int(operand[i],2))
        if(REG[register[0]]>REG[register[1]]):
            lineNo=int(sline[16:30],2)
            pc=lineNo*4+10000000
            continue
    elif opcode=='000111':   #ldata opcode
        operand=[]
        register=[]
        for x in range(6,11,5):
            operand.append(sline[x:x+5])
        lineNo=int(sline[11:],2)
        register.append(int(operand[0],2))
        REG[register[0]]=int(dataMap[lineNo*4+400000],2)
    elif opcode=='111010':   #ld opcode
        operand=[]
        register=[]
        for x in range(6,16,5):
            operand.append(sline[x:x+5])
        register.append(int(operand[0],2))
        register.append(int(operand[1],2))
        offsetLineNo = int(sline[16:30], 2)
        regLineNo = REG[register[1]]
        lineNo=offsetLineNo+regLineNo
        REG[register[0]]=int(dataMap[lineNo*4+400000])
    elif opcode=='111110':   #store opcode
        operand=[]
        register=[]
        for x in range(6,16,5):
            operand.append(sline[x:x+5])
        register.append(int(operand[0],2))
        register.append(int(operand[1],2))
        offsetLineNo = int(sline[16:30], 2)
        regLineNo = REG[register[1]]
        lineNo=offsetLineNo+regLineNo
        dataMap[lineNo*4+400000]=bin(REG[register[0]])

    print('pc is '+ str(pc))
    pc += 4


         

print(REG)
for i in range(32):
        REG[i] = 0
