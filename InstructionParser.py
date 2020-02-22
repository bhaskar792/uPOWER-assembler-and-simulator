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

class XOTypeInstruction(BaseInstruction):    
    def __init__(self):
        XOTypeRegex = r'(add)\s+(\$\d+)\s+(\$\d+)\s+(\$\d+)|(subf)\s+(\$\d+)\s+(\$\d+)\s+(\$\d+)'            #whenever this class is called it calls base instruction and send instruction regex

        super(XOTypeInstruction, self).__init__(XOTypeRegex)

    def parseInstr(self, instr):                                        #when this function is called with instruction it calls baseInstruction to parse
        return super(XOTypeInstruction, self).parseInstr(instr)

class DTypeInstruction(BaseInstruction):
    def __init__(self):
        DTypeRegex = r'(addi)\s+(\$\d+)\s+(\$\d+)\s+(\d+)|(addis)\s+(\$\d+)\s+(\$\d+)\s+(\d+)|(andi)\s+(\$\d+)\s+(\$\d+)\s+(\d+)|(ori)\s+(\$\d+)\s+(\$\d+)\s+(\d+)|(xori)\s+(\$\d+)\s+(\$\d+)\s+(\d+)|(lwz)\s+(\$\d+)\s+(\d+)+\(+(\$\d+)+\)|(swz)\s+(\$\d+)\s+(\d+)+\(+(\$\d+)+\)|(stwz)\s+(\$\d+)\s+(\d+)+\(+(\$\d+)+\)|(lhz)\s+(\$\d+)\s+(\d+)+\(+(\$\d+)+\)|(lha)\s+(\$\d+)\s+(\d+)+\(+(\$\d+)+\)|(sth)\s+(\$\d+)\s+(\d+)+\(+(\$\d+)+\)|(lbz)\s+(\$\d+)\s+(\d+)+\(+(\$\d+)+\)|(stb)\s+(\$\d+)\s+(\d+)+\(+(\$\d+)+\)'
        super(DTypeInstruction, self).__init__(DTypeRegex)

    def parseInstr(self, instr):
        operator, operands = super(DTypeInstruction, self).parseInstr(instr)
        if operator == 'sw' or operator == 'lw':
            return operator, (operands[0], operands[2], operands[1])

        return operator, operands

class XTypeInstruction(BaseInstruction):
    def __init__(self):
        XTypeRegex = r'(and)\s+(\$\d+)\s+(\$\d+)\s+(\$\d+)|(nand)\s+(\$\d+)\s+(\$\d+)\s+(\$\d+)|(extsw)\s+(\$\d+)\s+(\$\d+)|(or)\s+(\$\d+)\s+(\$\d+)\s+(\$\d+)|(xor)\s+(\$\d+)\s+(\$\d+)\s+(\$\d+)|(sld)\s+(\$\d+)\s+(\$\d+)\s+(\$\d+)|(srd)\s+(\$\d+)\s+(\$\d+)\s+(\$\d+)|(srad)\s+(\$\d+)\s+(\$\d+)\s+(\$\d+)'
        super(XTypeInstruction, self).__init__(XTypeRegex)

    def parseInstr(self, instr):
        return super(XTypeInstruction, self).parseInstr(instr)

class DSTypeInstruction(BaseInstruction):
    def __init__(self):
        DSTypeRegex = r'(ld)\s+(\$\d+)\s+(\d+)+\(+(\$\d+)+\)|(std)\s+(\$\d+)\s+(\d+)+\(+(\$\d+)+\)'
        super(DSTypeInstruction, self).__init__(DSTypeRegex)

    def parseInstr(self, instr):
        return super(DSTypeInstruction, self).parseInstr(instr)

### for DS operand return for ld $1 6($3) will be ['$1', '6', '$3']


class XSTypeInstruction(BaseInstruction):
    def __init__(self):
        XSTypeRegex = r'(sradi)\s+(\$\d+)\s+(\$\d+)\s+(\d+)'           #whenever this class is called it calls base instruction and send instruction regex

        super(XSTypeInstruction, self).__init__(XSTypeRegex)

    def parseInstr(self, instr):                                        #when this function is called with instruction it calls baseInstruction to parse
        return super(XSTypeInstruction, self).parseInstr(instr)

class BTypeInstruction(BaseInstruction):
    def __init__(self):
        BTypeRegex =  r'(bc)\s+(\$\d+)\s+(\$\d+)\s+(\w+)|(bca)\s+(\$\d+)\s+(\$\d+)\s+(\w+)'          #whenever this class is called it calls base instruction and send instruction regex

        super(BTypeInstruction, self).__init__(BTypeRegex)

    def parseInstr(self, instr):                                        #when this function is called with instruction it calls baseInstruction to parse
        return super(BTypeInstruction, self).parseInstr(instr)


class ITypeInstruction(BaseInstruction):
    def __init__(self):
        ITypeRegex = r'(bl)\s+(\w+)|(ba)\s+(\w+)|(li)\s+(\w+)'          #whenever this class is called it calls base instruction and send instruction regex

        super(ITypeInstruction, self).__init__(ITypeRegex)

    def parseInstr(self, instr):                                        #when this function is called with instruction it calls baseInstruction to parse
        return super(ITypeInstruction, self).parseInstr(instr)

class SCTypeInstruction(BaseInstruction):
    def __init__(self):
        SCTypeRegex = r'(sc)'           #whenever this class is called it calls base instruction and send instruction regex

        super(SCTypeInstruction, self).__init__(SCTypeRegex)

    def parseInstr(self, instr):                                        #when this function is called with instruction it calls baseInstruction to parse
        return super(SCTypeInstruction, self).parseInstr(instr)


class InstructionParser:
    def __init__(self, labelsMap={}):
        self.instrObjMap = {
            'XO-TYPE': XOTypeInstruction,
            'D-TYPE': DTypeInstruction,
            'X-TYPE': XTypeInstruction,
            'DS-TYPE': DSTypeInstruction,
            'XS-TYPE': XSTypeInstruction,
            'B-TYPE': BTypeInstruction,
            'I-TYPE': ITypeInstruction,
            'SC-TYPE': SCTypeInstruction
        }

        ##gives which type of instruction it is


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
        operands=list(filter(None, operands))
        #return instrType,operator,operands
        if label:
            operands = list(operands)                       #converting operand to list
            if label not in self.labelsMap:
                operands[-1] = None                 

            operands[-1] = str(self.labelsMap[label])
            operands = tuple(operands)
        
        ###added by bhaskar     #if label is there at last then replace with address
        #operands=list(operands)
        if instrType=='I-TYPE' or instrType=='B-TYPE':
            lastOfoperand=operands[-1]
            #print(type(operands))
            #lastOfoperand=lastOfoperand.split('$',1)
            #print(lastOfoperand)
            #if(len(lastOfoperand)>1):
            if(lastOfoperand.isdigit()):
                pass
            else:
                label=str(operands[-1])
                if  label not in self.labelsMap:
                    operands[-1] = None
                    print('not there')
                else:
                    operands[-1] = str(self.labelsMap[label])
            operands=list(operands)
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
