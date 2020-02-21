infilename='test.txt'
#from InstructionParser import  InstructionParser

outlines = []


with open(infilename) as f:
    outlines += f.readlines()

f.close()
print(outlines)
inlines=outlines



def stripComments(line):
    if not line:
        return ''

    cleaned = line
    if line.find('#') != -1:
        cleaned = line[0:line.find('#')] # Get rid of anything after a comment.

    return cleaned

def buildLabelsMap(lines):
    labelsMap = {}

    for lineNo, line in enumerate(lines):
        split = line.split(':', 1)
        if len(split) > 1:
            label = split[0]
            labelsMap[label] = lineNo

    return labelsMap

#lines = list(map(lambda line: stripComments(line.rstrip()), inlines))
lines = map(lambda line: stripComments(line.rstrip()), inlines)  #get rid of \n whitespace at end of line #return either proper lines or empty item
print(lines)
lines = filter(None, lines)
print(lines)
labelsMap = buildLabelsMap(lines)

print(labelsMap)
#parser=InstructionParser(labelsMap=labelsMap)

#rint(parser)
instr='hey:'
split = instr.split(':', 1)

print(len(split))
#lines = list(filter(None, lines))
#print(str(lines))

groups = ('add', '$1', '$2', 'hey')
#print(type(groups))
operand=groups[1:]
#print(operand)
operand=list(operand)
lastOfoperand=operand[-1]
lastOfoperand=lastOfoperand.split('$',1)
print(lastOfoperand)
if(len(lastOfoperand)>1):
    pass
else:
    label=str(operand[-1])
    if  label not in labelsMap:
        operand[-1] = None
        print('not there')
    else:

        operand[-1] = str(labelsMap[label])

operand=tuple(operand)
