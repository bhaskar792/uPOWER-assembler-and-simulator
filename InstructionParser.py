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
        groups = filter(lambda x: x is not None, match.groups())      #to remove none from the tuples
        groups  =  tuple(groups)                                       #groups = ('add', '$1', '$2', '$3')
        operator = groups[0]
        operands = groups[1:]

        return operator, operands

class RTypeInstruction(BaseInstruction):    
    def __init__(self):
        RTypeRegex = r'(add)\s+(\$\d+)\s+(\$\d+)\s+(\$\d+)|(subf)\s+(\$\d+)\s+(\$\d+)\s+(\$\d+)'            #whenever this class is called it calls base instruction and send instruction regex

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

        self.labelsMap = labelsMap#taking labelmap from assembler which made proper labelmap


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
       # return instrType,operator,instr.split(' ')[1:]
        if not instrType:                               #if intruction not available
            return '', '', None 

        instrObj = self.instrObjMap[instrType]()           #instrObj became an object of RTypeInstruction(class above)
     
        operator, operands = instrObj.parseInstr(instr)     #operator=add and operand=$1 $2 $3
        return instrType,operator,operands
        if label:
            operands = list(operands)                       #converting operand to list
            if label not in self.labelsMap:
                operands[-1] = None                 

            operands[-1] = str(self.labelsMap[label])
            operands = tuple(operands)
        
        ###added by bhaskar     #if label is there at last then replace with address
        operands=list(operands)
        lastOfoperand=operands[-1]
        print(type(operands))
        lastOfoperand=lastOfoperand.split('$',1)
        #print(lastOfoperand)
        if(len(lastOfoperand)>1):
            pass
        else:
            label=str(operands[-1])
            if  label not in self.labelsMap:
                operands[-1] = None
                print('not there')
            else:
                operands[-1] = str(self.labelsMap[label])
        operands=tuple(operands)
        ###added by bhaskar

        return instrType, operator, operands

    def convert(self, instr):
        if not instr:
            return ''
        ###added by bhaskar
        instrType, operator, operands = self.parse(instr)
        if not operator:
            return ''
        operand=[]
        if (operator == 'add'):
            opcode = '001110'
            binary = opcode
            operands = list(operands)
            u = Utils()
            for i in operands:
                i = i.split('$')[1]
                operand.append(i)
            
            rt = u.int2bs(operand[0], 5)
            ra = u.int2bs(operand[1], 5)
            rb = u.int2bs(operand[2], 5)
            binary = binary + rt + ra + rb
            return(binary)
        ###added by bhaskar
'''
if __name__ == '__main__':
    # Test
    ip = InstructionParser()
    print ip.convert('add $6 $2 $4')
    print ip.convert('addi $2 $0 2', format='binary')
    print hex(int(ip.convert('addi $2 $0 2', format='binary'), 2))
'''

