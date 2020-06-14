from Assembler import Assembler
from InstructionParser import InstructionParser


def stripComments( line):
    if not line:
        return ''

    cleaned = line
    if line.find('#') != -1:
        cleaned = line[0:line.find('#')]  # Get rid of anything after a comment(#).
    return cleaned


def buildLabelsMap( lines):
    labelsMap = {}
    textmap = {}
    for i in lines:
        if (len(list(filter(None, i.split(':')))) > 1):
            textmap[list(filter(None, i.split(':')))[0]] = bin(int(list(filter(None, i.split(':')))[1].strip(), 16))[2:]
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
    #labelsMap = labelsMap - textmap
    return labelsMap


def buildtextmap( lines):
    textmap = {}
    for i in lines:
        if (len(list(filter(None, i.split(':')))) > 1):
            textmap[list(filter(None, i.split(':')))[0]] = bin(int(list(filter(None, i.split(':')))[1].strip(), 16))[2:]

    return textmap


infilename = 'test.txt'
outlines = []
with open(infilename) as f:
    outlines += f.readlines()
inlines = outlines
f.close()
print(outlines)


lines = list(map(lambda line: stripComments(line.rstrip()), inlines))
print(lines)

textmap = buildtextmap(lines)
print(textmap)

labelsmap = buildLabelsMap(lines)
print (labelsmap)

instrlines = []
for i in lines:
    stripped = i.split(':', 1)
    if len(stripped) > 1:
        i = ''
    instrlines.append(i)

instrlines = filter(None, instrlines)
parser = InstructionParser(labelsmap)
instr = 'bca $1 $2 hey'
outlines = map(lambda line: parser.convert(line), instrlines)
print("############################")
print (list (outlines))




type,operator,operands=parser.parse(instr)
print(type)
print(operator)
print(operands)
binary = parser.convert(instr)
print (binary)