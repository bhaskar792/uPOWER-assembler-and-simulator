import sys
from Utils import Utils
import getopt

from InstructionParser import InstructionParser

REG = [0]*32
class disassembler(object):

    def __init__(self, infilenames):
        self.infilenames = infilenames


    def stripComments(self, line):
        if not line:
            return ''

        cleaned = line
        if line.find('#') != -1:
            cleaned = line[0:line.find('#')]  # Get rid of anything after a comment(#).
        return cleaned

    def mergeInputFiles(self):  # given list of all input lines
        outlines = []

        filename = self.infilenames
        with open(filename) as f:
            outlines += f.readlines()

        f.close()

        return outlines  # return all the lines of assembly file
    def buildTextMap(self,lines):
        labelsMap = {}
        count = 10000000
        for lineNo, line in enumerate(lines):
            split = line.split(':', 1)
            if len(split) == 1:
                label = split[0].strip()
                labelsMap[count] = label
                count = count + 4

        return labelsMap

    def buildDataMap(self, lines):
        labelsMap = {}
        count = 400000
        for lineNo, line in enumerate(lines):
            split = line.split(':', 1)
            if len(split) > 1:
                label = split[1].strip()
                labelsMap[count] = label
                count = count + 4

        return labelsMap


    def maps(self,lines):


        dataMap = self.buildDataMap(lines)
        textMap = self.buildTextMap(lines)
        fullMap = {**dataMap, **textMap}
        return dataMap,textMap,fullMap

    def simulate(self, lines, dataMap, textMap, fullMap):
        pc = 10000000
        u = Utils()
        nPc = -1
        breakPointSet = False
        while (pc <= (len(textMap) - 1) * 4 + 10000000):
            if (nPc == pc):
                breakPointSet = False
            if (not breakPointSet):
                while (True):
                    inpt = input()
                    if (inpt == 'text'):
                        print(textMap)
                    elif (inpt == 'data'):
                        print(dataMap)
                    elif (inpt == 'reg'):
                        print(REG)
                    elif (inpt == 'pc'):
                        print(pc)
                    elif (inpt == 'stepi'):
                        break
                    elif (inpt == 'jump'):
                        print('please enter new pc with considering start of the section as 0 ex 4 or 8 or 12 or 40')
                        pc = int(input())
                        pc = pc + 10000000
                        continue
                    elif (inpt == 'break'):
                        print('please enter pc with considering start of the section as 0 ex 4 or 8 or 12 or 40')
                        breakPointSet = True
                        nPc = int(input())
                        nPc = nPc + 10000000
                        break
                    else:
                        print('Usage')
                        print('text: print text section')
                        print('data: print data section')
                        print('reg: print value of all the registers')
                        print('pc: current value of program counter')
                        print('stepi: execute next instruction')
                        print(
                            'jump: Jump to a specific instruction. Type jump for usage then enter nPc according to given usage')
                        print(
                            'break: continue to a specfic instruction. Type break for usage then enter nPc according to given usage')
                        print('designed by: ')
                        print('Bhaskar Kataria (181CO213)')
                        print('Ketan Bhujange (181CO227)')
                        print('Manas Trivedi (181CO231)')
                        print('Omanshu Mahawar (181CO237)')

            sline = textMap[pc]

            opcode = sline[0:6]

            if opcode == '011111':

                operand = []
                register = []
                for x in range(6, 21, 5):
                    operand.append(sline[x:x + 5])
                # print(operand)
                for i in range(3):
                    register.append(int(operand[i], 2))
                # print(register)
                # print(sline[22:31])
                if sline[22:31] == '100001010':  # add
                    REG[register[0]] = REG[register[1]] + REG[register[2]]
                    print('add')
                elif sline[22:31] == '000101000':  # subf
                    REG[register[0]] = REG[register[2]] - REG[register[1]]
                    print('sub')
                elif sline[21:30] == '000001110':  # and
                    REG[register[1]] = REG[register[0]] & REG[register[2]]
                    print('and')
                elif sline[21:30] == '011011110':  # or
                    REG[register[1]] = REG[register[0]] | REG[register[2]]
                    print('or')
            elif opcode == '001110':  # addi
                print('addi')
                operand = []
                register = []
                for x in range(6, 16, 5):
                    operand.append(sline[x:x + 5])
                # print(operand)
                for i in range(2):
                    register.append(int(operand[i], 2))
                # print(register)
                # print(sline[16:])
                d = int(sline[16:], 2)
                REG[register[0]] = REG[register[1]] + d
            # elif opcode == '111010' :
            elif opcode == '010011':  # bca
                print('bca')
                operand = []
                register = []
                for x in range(6, 16, 5):
                    operand.append(sline[x:x + 5])
                for i in range(2):
                    register.append(int(operand[i], 2))
                if (REG[register[0]] > REG[register[1]]):
                    lineNo = int(sline[16:30], 2)
                    pc = lineNo * 4 + 10000000
                    print(lineNo)
                    continue
            elif opcode == '111010':  # ld opcode
                print('ld')
                operand = []
                register = []
                for x in range(6, 16, 5):
                    operand.append(sline[x:x + 5])
                register.append(int(operand[0], 2))
                register.append(int(operand[1], 2))
                offsetLineNo = int(sline[16:30], 2)
                regLineNo = REG[register[1]]
                lineNo = offsetLineNo + regLineNo
                REG[register[0]] = int(dataMap[lineNo * 4 + 400000], 2)
            elif opcode == '111110':  # store opcode (std)
                print('std')
                operand = []
                register = []
                for x in range(6, 16, 5):
                    operand.append(sline[x:x + 5])
                register.append(int(operand[0], 2))
                register.append(int(operand[1], 2))
                offsetLineNo = int(sline[16:30], 2)
                regLineNo = REG[register[1]]
                lineNo = offsetLineNo + regLineNo
                binary = u.int2bs(REG[register[0]], 32)
                dataMap[lineNo * 4 + 400000] = binary

            print('pc is ' + str(pc))
            pc += 4
            print('REG')
            print(REG)
    def main(self):
        inlines = self.mergeInputFiles()
        lines = list(map(lambda line: self.stripComments(line.rstrip()),inlines))  # get rid of \n whitespace at end of line #return either proper lines or empty item
        lines = list(filter(None, lines))
        dataMap, textMap, fullMap=self.maps(lines)
        print('dataMap')
        print (dataMap)
        self.simulate(lines,dataMap,textMap,fullMap)






if __name__ == '__main__':
    print('Number of arguments:', len(sys.argv), 'arguments.')
    print('Argument List:', str(sys.argv))


    if len(sys.argv) < 2 or '-i' not in sys.argv :
        print(
            'Usage: python disassembler.py -i <inputfile.txt>')
        sys.exit(2)

    inputfiles = sys.argv[sys.argv.index('-i') + 1]

    assembler = disassembler(inputfiles)
    assembler.main()