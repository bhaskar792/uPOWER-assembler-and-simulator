import re

from InstructionLookup import InstructionLookup
from Utils import Utils

class BaseInstruction(object):
    def __init__(self, instrRegex):
        self.instrRegex = re.compile(instrRegex)

    def parseInstr(self, instr):                        #instr is given as string like add $1 $2 $3
        match = self.instrRegex.match(instr)            #matching given regex
        if not match:
            return '', ()
                                                                     #if matched then
    #    groups = filter(lambda x: x is not None, match.groups())      #not working due to difference between python 2 and 3
        groups  =  match.groups()                                       #groups = ('add', '$1', '$2', '$3')
        operator = groups[0]
        operands = groups[1:]

        return operator, operands

class RTypeInstruction(BaseInstruction):    
    def __init__(self):
        RTypeRegex = r'(\w+)\s+(\$\d+)\s+(\$\d+)\s+(\$\d+)'             #whenever this class is called it calls base instruction and send instruction regex
        super(RTypeInstruction, self).__init__(RTypeRegex)

    def parseInstr(self, instr):                                        #when this function is called with instruction it calls baseInstruction to parse
        return super(RTypeInstruction, self).parseInstr(instr)

class ITypeInstruction(BaseInstruction):
    def __init__(self):
        ITypeRegex = r'(\w+)\s+(\$\d+)\s?,?\s+(\$\d+)\s?,?\s+(\d+)|(\w+)\s+(\$\d+)\s?,?\s+(-?\d+)\((\$\d+)\)'
        super(ITypeInstruction, self).__init__(ITypeRegex)

    def parseInstr(self, instr):
        operator, operands = super(ITypeInstruction, self).parseInstr(instr)
        if operator == 'sw' or operator == 'lw':
            return operator, (operands[0], operands[2], operands[1])

        return operator, operands

class JTypeInstruction(BaseInstruction):
    def __init__(self):
        JTypeRegex = r'(\w+)\s+(\w+)'
        super(JTypeInstruction, self).__init__(JTypeRegex)

    def parseInstr(self, instr):
        return super(JTypeInstruction, self).parseInstr(instr)

class InstructionParser:
    def __init__(self, labelsMap={}):
        self.instrObjMap = {
            'R-TYPE': RTypeInstruction,
            'I-TYPE': ITypeInstruction,
            'J-TYPE': JTypeInstruction
        }

        ##gives which type of instruction it is

        self.formatFuncMap = {
            'binary': lambda s, n: Utils.int2bs(s, n),
            'hex': lambda s, n: Utils.bs2hex(Utils.int2bs(s, n))
        }

        ##for converting to either binary or hex

        self.labelsMap = labelsMap##current labelmap is an empty dict


        self.instrLookup = InstructionLookup() #each type of instruction is assigned a integer (for now dont know what it represents)
        self.instrObj = None # used to define null object

    def extractLabels(self, instr): #this function extract labels in this
        if not instr:
            return '', ''  #if no intruction is given

        split = instr.split(':', 1) #splitting with : and by 1 it means just splitting into 2 parts left of : and right of :

        if len(split) < 2:          #if : is not there in given instruction then length will be 1
            return '', instr

        return split[0], split[1].strip()  #for now i think if in the same line some intruction is given then this thing is used

    def parse(self, instr):
        label, instr = self.extractLabels(instr)
        if not instr:                       #if no instriction in given line (empty lines)
            return '', '', None

        operator = instr.split(' ')[0]         #splitting by space operator=add in add $1 $2 $3
        instrType = self.instrLookup.type(operator)     #return a type(R-TYPE) corresponding to particular instruction
        if not instrType:                               #if intruction not available
            return '', '', None 

        instrObj = self.instrObjMap[instrType]()           #instrObj became an object of RTypeInstruction(class above)
        operator, operands = instrObj.parseInstr(instr)     #operator=add and operand=$1 $2 $3

        if label:
            operands = list(operands)
            if label not in self.labelsMap:
                operands[-1] = None

            operands[-1] = str(self.labelsMap[label])
            operands = tuple(operands)

        return instrType, operator, operands

    def convert(self, instr, format='binary', formatFunc=None, instrFieldSizes=(6, 4, 4, 4)):
        if not instr:
            return ''

        if formatFunc is None:
            formatFunc = self.formatFuncMap[format]

        instrType, operator, operands = self.parse(instr)
        if not operator:
            return ''

        opcode = self.instrLookup.opcode(operator)
        convertedOpcode = formatFunc(opcode, instrFieldSizes[0])
        operands = map(lambda op: op.strip('$'), operands)
        convertedOperands = map(lambda (i, s): formatFunc(s, instrFieldSizes[i + 1]), enumerate(operands))

        convertedOutput = convertedOpcode + ''.join(convertedOperands)
        return convertedOutput

if __name__ == '__main__':
    # Test
    ip = InstructionParser()
    print ip.convert('add $6 $2 $4')
    print ip.convert('addi $2 $0 2', format='binary')
    print hex(int(ip.convert('addi $2 $0 2', format='binary'), 2))
