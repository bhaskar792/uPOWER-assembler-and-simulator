infilename='test.txt'
from InstructionParser import  InstructionParser
import re
from Utils import Utils
outlines = []
print('#########################################')
XOTypeRegex=r'(add)\s+(\$\d+)\s+(\$\d+)\s+(\$\d+)|(subf)\s+(\$\d+)\s+(\$\d+)\s+(\$\d+)'
instrreg=re.compile(XOTypeRegex)
instr='add $1 $2 $3'
match=instrreg.match(instr)


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
print('**********************************')
#lines = list(map(lambda line: stripComments(line.rstrip()), inlines))
lines = list(map(lambda line: stripComments(line.rstrip()), inlines))  #get rid of \n whitespace at end of line #return either proper lines or empty item

print(lines)
lines=list(filter(None,lines))
labelsMap = buildLabelsMap(lines)

#lines=list(lines)
print(lines)
print('for loop')
instrlines=[]
for i in lines:
    stripped=i.split(':',1)
    if(len(stripped)>1):
        i=''
    instrlines.append(i)

lines = filter(None, instrlines)
print(list(lines))


print(labelsMap)
parser=InstructionParser(labelsMap=labelsMap)
instr='add $1 $2 $3'
outlines=map(lambda line: parser.convert(line), lines)
print(list(outlines))
print('###########################')
type,operator,operands=parser.parse(instr)
print(type)
print(operator)
print(operands)
operand=[]
if(operator=='add'):
    opcode='001110'
    binary=opcode
    operands=list(operands)
    for i in operands:
        i=i.split('$')[1]
        operand.append(i)
    rt=operand[0]
    ra=operand[1]
    rb=operand[2]
    u=Utils()
    rt = u.int2bs(rt, 5)
    ra = u.int2bs(ra, 5)
    rb = u.int2bs(rb, 5)
    binary=binary+rt+ra+rb

    print(binary)

split = instr.split(':', 1)

print('################################')
#lines = list(filter(None, lines))
#print(str(lines))

groups = ('add', '$1', '$2', 'hey')
#print(type(groups))
operand=groups[1:]
#print(operand)
operand=list(operand)
lastOfoperand=operand[-1]
lastOfoperand=lastOfoperand.split('$',1)

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
