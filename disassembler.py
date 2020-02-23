import sys
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

        for filename in self.infilenames:
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

    def simulate(self,lines,dataMap,textMap,fullMap):
        for sline in lines:
            opcode = sline[0:6]

            print(opcode)
            if opcode == '011111':
                operand = []
                register = []
                x = 6
                for i in range(3):
                    operand.append(sline[x:x + 5])
                    x += 5

                for i in range(3):
                    register.append(int(operand[i], 2))

                if sline[22:31] == '100001010':  # add
                    REG[register[0]] = REG[register[1]] + REG[register[2]]
                    print('add')
                elif sline[22:31] == '000101000':  # subf
                    REG[register[0]] = REG[register[2]] - REG[register[1]]
                    print('sub')
                elif sline[21:30] == '0000011100':  # and
                    REG[register[1]] = REG[register[0]] & REG[register[2]]
                    print('and')
                elif sline[21:30] == '0110111100':  # or
                    REG[register[1]] = REG[register[0]] | REG[register[2]]
                    print('or')
            elif opcode == '001110':  # addi
                operand = []
                register = []
                x = 6
                for i in range(2):
                    operand.append(sline[x:x + 5])
                    x += 5
                # print(operand)
                for i in range(2):
                    register.append(int(operand[i], 2))
                # print(register)
                # print(sline[16:])
                d = int(sline[16:], 2)
                REG[register[0]] = REG[register[1]] + d
            #elif opcode == '111010':

        print(REG)
        for i in range(32):
            REG[i] = 0

    def main(self):
        inlines = self.mergeInputFiles()  # get all the lines from input in list
        outlines = []
        lines = list(map(lambda line: self.stripComments(line.rstrip()),inlines))  # get rid of \n whitespace at end of line #return either proper lines or empty item
        lines = list(filter(None, lines))
        dataMap, textMap, fullMap=self.map(lines)
        self.simulate(lines,dataMap,textMap,fullMap)






if __name__ == '__main__':
    print('Number of arguments:', len(sys.argv), 'arguments.')
    print('Argument List:', str(sys.argv))


    if len(sys.argv) < 4 or '-i' not in sys.argv or '-o' \
            not in sys.argv:
        print(
            'Usage: python Assembler.py -i <inputfile.asm>[ <inputfile2.asm> <inputfile3.asm> ...] -o <outputfile.hex>')
        sys.exit(2)

    inputfiles = sys.argv[sys.argv.index('-i') + 1:sys.argv.index('-o')]
    outputfile = sys.argv[sys.argv.index('-o') + 1]

    assembler = disassembler(inputfiles)
    assembler.main()