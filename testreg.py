infilename='test.txt'
from InstructionParser import  InstructionParser
import re
import simple_pickle as pickle
from Utils import Utils
outlines = []
print('#########################################')
BTypeRegex=r'(sc)'
instrreg=re.compile(BTypeRegex)
instr='sc'
match=instrreg.match(instr)
if match:
    print('matched')

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
    count=0
    for lineNo, line in enumerate(lines):
        split = line.split(':', 1)
        if len(split) > 1:

            label = split[0]
            labelsMap[label] = lineNo-count
            count=count+1

    return labelsMap


print('**********************************')
#lines = list(map(lambda line: stripComments(line.rstrip()), inlines))
lines = list(map(lambda line: stripComments(line.rstrip()), inlines))  #get rid of \n whitespace at end of line #return either proper lines or empty item

print(lines)
lines=list(filter(None,lines))

labelsMap = buildLabelsMap(lines)





#text = list(filter(None,lines[0].split(':')))
#textmap[text[0]]=text[1].strip()
#print(textmap)
#print(list(filter(None,lines[0].split(':'))))
#lines=list(lines)
#print(len())
print('for loop')
instrlines=[]
for i in lines:
    stripped=i.split(':',1)
    if(len(stripped)>1):
        i=''
    instrlines.append(i)

instrlines = list(filter(None, instrlines))
print(list(instrlines))
print(instrlines)

print(labelsMap)

print(labelsMap)
parser=InstructionParser(labelsMap=labelsMap)
#instr='sc'
instr='add $1 $2 $3'

outlines=list(map(lambda line: parser.convert(line), instrlines))
print(outlines)

outfilename='out.txt'
with open(outfilename, 'w') as of:
    of.write('v2.0 raw\n')
    for outline in outlines:
        of.write(outline)
        of.write("\n")
of.close()

print('###########################')
type,operator,operands=parser.parse(instr)
print(type)
print(operator)
print(operands)



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


def buildtextmap(lines):
    textmap={}
    for i in lines:
        if (len(list(filter(None, i.split(':')))) > 1):
            textmap[list(filter(None, i.split(':')))[0]] = list(filter(None, i.split(':')))[1].strip()

    return textmap

textmap=buildtextmap(lines)
fout = "out.txt"
fo = open(fout, "w")

for k, v in textmap.items():
    fo.write(str(k) + ':'+ str(v) + '\n')
for outline in outlines:
        fo.write(outline)
        fo.write("\n")

fo.close()
print(len(textmap))
labelsMap.update(textmap)
print(labelsMap)
