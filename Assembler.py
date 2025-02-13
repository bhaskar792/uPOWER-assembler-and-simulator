
import sys
import getopt

from InstructionParser import InstructionParser


class Assembler(object):

    def __init__(self, infilenames, outfilename):
        self.infilenames = infilenames
        self.outfilename = outfilename

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

    def buildLabelsMap(self,lines):
        labelsMap = {}
        textmap = {}
        for i in lines:
            if (len(list(filter(None, i.split(':')))) > 1):
                textmap[list(filter(None, i.split(':')))[0]] = bin(
                    int(list(filter(None, i.split(':')))[1].strip(), 16))[2:]
        textMapLen = len(textmap)
        count = 0
        for (lineNo, line) in enumerate(lines):
            split = line.split(':', 1)
            if len(split) > 1:
                label = split[0]
                labelsMap[
                    label] = lineNo - count - textMapLen  # because everytime at place of label line is removed to everytime decrease by 1
                if (len(list(filter(None, split))) == 1):
                    count = count + 1
        for key in list(labelsMap):
            if labelsMap[key] < 0:
                del labelsMap[key]
        # labelsMap = labelsMap - textmap
        return labelsMap

    def buildtextmap(self,lines):
        textmap = {}
        for i in lines:
            if (len(list(filter(None, i.split(':')))) > 1):
                textmap[list(filter(None, i.split(':')))[0]] = bin(int(list(filter(None, i.split(':')))[1].strip(),16))[2:]

        return textmap



    def AssemblyToHex(self):
        '''given an ascii assembly file , read it in line by line and convert each line of assembly to machine code
........then save that machinecode to an outputfile'''

        inlines = self.mergeInputFiles()  # get all the lines from input in list
        outlines = []

        lines = list(map(lambda line: \
                     self.stripComments(line.rstrip()), inlines))  # get rid of \n whitespace at end of line #return either proper lines or empty item

        lines = list(filter(None, lines))
        textmap = self.buildtextmap(lines)  # for text section
        labelsMap = self.buildLabelsMap(lines)  # build labelsmap like {'bro': 0, 'there': 2, 'hey': 3} and line numbers are correct

        parser = InstructionParser(labelsMap=labelsMap)
        
        instrlines = []
        for i in lines:
            stripped = i.split(':', 1)
            if len(stripped) > 1:
                i = ''
            instrlines.append(i)

        
        instrlines = filter(None, instrlines)
        
        outlines = map(lambda line: parser.convert(line), instrlines)
        with open(self.outfilename, 'w') as of:
            for k, v in textmap.items():
                of.write(str(k) + ':' + str(v) + '\n')

            for outline in outlines:
                of.write(outline)
                of.write('\n')
            of.close()


if __name__ == '__main__':
    print ('Number of arguments:', len(sys.argv), 'arguments.')
    print ('Argument List:', str(sys.argv))


    if len(sys.argv) < 4 or '-i' not in sys.argv or '-o' \
        not in sys.argv:
        print('Usage: python Assembler.py -i <inputfile.asm> -o <outputfile.hex>')
        sys.exit(2)

    inputfiles = sys.argv[sys.argv.index('-i') + 1]
    outputfile = sys.argv[sys.argv.index('-o') + 1]

    assembler = Assembler(inputfiles, outputfile)
    assembler.AssemblyToHex()
