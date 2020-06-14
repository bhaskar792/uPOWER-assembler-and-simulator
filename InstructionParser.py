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
        DTypeRegex = r'(addi)\s+(\$\d+)\s+(\$\d+)\s+(\d+)|(addis)\s+(\$\d+)\s+(\$\d+)\s+(\d+)|(andi)\s+(\$\d+)\s+(\$\d+)\s+(\d+)|(ori)\s+(\$\d+)\s+(\$\d+)\s+(\d+)|(xori)\s+(\$\d+)\s+(\$\d+)\s+(\d+)|(lwz)\s+(\$\d+)\s+(\d+)+\(+(\$\d+)+\)|(stw)\s+(\$\d+)\s+(\d+)+\(+(\$\d+)+\)|(stwu)\s+(\$\d+)\s+(\d+)+\(+(\$\d+)+\)|(lhz)\s+(\$\d+)\s+(\d+)+\(+(\$\d+)+\)|(lha)\s+(\$\d+)\s+(\d+)+\(+(\$\d+)+\)|(sth)\s+(\$\d+)\s+(\d+)+\(+(\$\d+)+\)|(lbz)\s+(\$\d+)\s+(\d+)+\(+(\$\d+)+\)|(stb)\s+(\$\d+)\s+(\d+)+\(+(\$\d+)+\)'
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
        ITypeRegex = r'(bl)\s+(\w+)|(ba)\s+(\w+)|(b)\s+(\w+)'          #whenever this class is called it calls base instruction and send instruction regex

        super(ITypeInstruction, self).__init__(ITypeRegex)

    def parseInstr(self, instr):                                        #when this function is called with instruction it calls baseInstruction to parse
        return super(ITypeInstruction, self).parseInstr(instr)

class SCTypeInstruction(BaseInstruction):
    def __init__(self):
        SCTypeRegex = r'(sc)'           #whenever this class is called it calls base instruction and send instruction regex

        super(SCTypeInstruction, self).__init__(SCTypeRegex)

    def parseInstr(self, instr):                                        #when this function is called with instruction it calls baseInstruction to parse
        return super(SCTypeInstruction, self).parseInstr(instr)

class LDATATypeInstruction(BaseInstruction):
    def __init__(self):
        LDATATypeRegex = r'(ldata)\s+(\$\d+)\s+(\w+)'         #whenever this class is called it calls base instruction and send instruction regex

        super(LDATATypeInstruction, self).__init__(LDATATypeRegex)

    def parseInstr(self, instr):                                        #when this function is called with instruction it calls baseInstruction to parse
        return super(LDATATypeInstruction, self).parseInstr(instr)



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
            'SC-TYPE': SCTypeInstruction,
            'LDATA-TYPE': LDATATypeInstruction
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
        #print (operator)
        instrType = self.instrLookup.type(operator)     #return a type(R-TYPE) corresponding to particular instruction

        #return instrType,operator,instr.split(' ')[1:]
        if not instrType:
            print ("here")#if intruction not available
            return '', '', None 
       # print ("not here")
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
        if instrType=='I-TYPE' or instrType=='B-TYPE' or instrType=='LDATA-TYPE':
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
            opcode = '011111'
            binary = opcode
            operands = list(operands)
            u = Utils()
            for i in operands:
                i = i.split('$')[1]
                operand.append(i)

            rt = u.int2bs(operand[0], 5)
            ra = u.int2bs(operand[1], 5)
            rb = u.int2bs(operand[2], 5)
            binary = binary + rt + ra + rb + "0" + "100001010" + "0"
            return (binary)
        elif (operator == 'subf'):
            opcode = '011111'
            binary = opcode
            operands = list(operands)
            u = Utils()
            for i in operands:
                i = i.split('$')[1]
                operand.append(i)

            rt = u.int2bs(operand[0], 5)
            ra = u.int2bs(operand[1], 5)
            rb = u.int2bs(operand[2], 5)
            binary = binary + rt + ra + rb + "0" + "000101000" + "0"
            return (binary)
        elif (operator == 'and'):
            opcode = '011111'
            binary = opcode
            operands = list(operands)
            u = Utils()
            for i in operands:
                i = i.split('$')[1]
                operand.append(i)

            ra = u.int2bs(operand[0], 5)
            rs = u.int2bs(operand[1], 5)
            rb = u.int2bs(operand[2], 5)
            binary = binary + rs + ra + rb + "0000011100" + "0"
            return (binary)
        elif (operator == 'nand'):
            opcode = '011111'
            binary = opcode
            operands = list(operands)
            u = Utils()
            for i in operands:
                i = i.split('$')[1]
                operand.append(i)

            ra = u.int2bs(operand[0], 5)
            rs = u.int2bs(operand[1], 5)
            rb = u.int2bs(operand[2], 5)
            binary = binary + rs + ra + rb + "0111011100" + "0"
            return (binary)
        elif (operator == 'or'):
            opcode = '011111'
            binary = opcode
            operands = list(operands)
            u = Utils()
            for i in operands:
                i = i.split('$')[1]
                operand.append(i)

            ra = u.int2bs(operand[0], 5)
            rs = u.int2bs(operand[1], 5)
            rb = u.int2bs(operand[2], 5)
            binary = binary + rs + ra + rb + "0110111100" + "0"
            return (binary)
        elif (operator == 'xor'):
            opcode = '011111'
            binary = opcode
            operands = list(operands)
            u = Utils()
            for i in operands:
                i = i.split('$')[1]
                operand.append(i)

            ra = u.int2bs(operand[0], 5)
            rs = u.int2bs(operand[1], 5)
            rb = u.int2bs(operand[2], 5)
            binary = binary + rs + ra + rb + "0100111100" + "0"
            return(binary)
        elif (operator == 'sld'):
            opcode = '011111'
            binary = opcode
            operands = list(operands)
            u = Utils()
            for i in operands:
                i = i.split('$')[1]
                operand.append(i)

            ra = u.int2bs(operand[0], 5)
            rs = u.int2bs(operand[1], 5)
            rb = u.int2bs(operand[2], 5)
            binary = binary + rs + ra + rb + "0111011100" + "0"
            return (binary)
        elif (operator == 'srd'):
            opcode = '011111'
            binary = opcode
            operands = list(operands)
            u = Utils()
            for i in operands:
                i = i.split('$')[1]
                operand.append(i)

            ra = u.int2bs(operand[0], 5)
            rs = u.int2bs(operand[1], 5)
            rb = u.int2bs(operand[2], 5)
            binary = binary + rs + ra + rb + "1000011011" + "0"
            return (binary)
        elif (operator == 'srad'):
            opcode = '011111'
            binary = opcode
            operands = list(operands)
            u = Utils()
            for i in operands:
                i = i.split('$')[1]
                operand.append(i)

            ra = u.int2bs(operand[0], 5)
            rs = u.int2bs(operand[1], 5)
            rb = u.int2bs(operand[2], 5)
            binary = binary + rs + ra + rb + "1100011010" + "0"
            return (binary)

        elif (operator == 'sradi'):
            opcode = '011111'
            binary = opcode
            operands = list(operands)
            u = Utils()
            operand.append(operands[0].split('$')[1])
            operand.append(operands[1].split('$')[1])

            ra = u.int2bs(operand[0], 5)
            rs = u.int2bs(operand[1], 5)
            sh = u.int2bs(operand[1], 6)
            binary = binary + rs + ra + sh[0:5] + "110011101" + sh[5:6] + "0"
            return (binary)
        elif (operator == 'addi'):
            opcode = '001110'
            binary = opcode
            operands = list(operands)
            u = Utils()
            operand.append(operands[0].split('$')[1])
            operand.append(operands[1].split('$')[1])
            operand.append(operands[2])
            rt = u.int2bs(operand[0], 5)
            ra = u.int2bs(operand[1], 5)
            si = u.int2bs(operand[2], 16)
            binary = binary + rt + ra + si
            return(binary)
        elif (operator == 'addis'):
            opcode = '001111'
            binary = opcode
            operands = list(operands)
            u = Utils()
            operand.append(operands[0].split('$')[1])
            operand.append(operands[1].split('$')[1])
            operand.append(operands[2])
            rt = u.int2bs(operand[0], 5)
            ra = u.int2bs(operand[1], 5)
            si = u.int2bs(operand[2], 16)
            binary = binary + rt + ra  + si
            return(binary)
        elif (operator == 'andi'):
            opcode = '011100'
            binary = opcode
            operands = list(operands)
            u = Utils()
            operand.append(operands[0].split('$')[1])
            operand.append(operands[1].split('$')[1])
            operand.append(operands[2])
            ra = u.int2bs(operand[0], 5)
            rs = u.int2bs(operand[1], 5)
            si = u.int2bs(operand[2], 16)
            binary = binary + ra + rs  + si
            return(binary)
        elif (operator == 'ori'):
            opcode = '011000'
            binary = opcode
            operands = list(operands)
            u = Utils()
            operand.append(operands[0].split('$')[1])
            operand.append(operands[1].split('$')[1])
            operand.append(operands[2])
            ra = u.int2bs(operand[0], 5)
            rs = u.int2bs(operand[1], 5)
            si = u.int2bs(operand[2], 16)
            binary = binary + ra + rs  + si
            return(binary)
        elif (operator == 'xori'):
            opcode = '011010'
            binary = opcode
            operands = list(operands)
            u = Utils()
            operand.append(operands[0].split('$')[1])
            operand.append(operands[1].split('$')[1])
            operand.append(operands[2])
            ra = u.int2bs(operand[0], 5)
            rs = u.int2bs(operand[1], 5)
            si = u.int2bs(operand[2], 16)
            binary = binary + ra + rs  + si
            return(binary)
        elif (operator == 'lwz'):
            opcode = '100000'
            binary = opcode
            operands = list(operands)
            u = Utils()
            operand.append(operands[0].split('$')[1])
            operand.append(operands[2].split('$')[1])
            operand.append(operands[1])
            rt = u.int2bs(operand[0], 5)
            ra = u.int2bs(operand[1], 5)
            si = u.int2bs(operand[2], 16)
            binary = binary + rt + ra + si
            return(binary)
        elif (operator == 'stw'):
            opcode = '100100'
            binary = opcode
            operands = list(operands)
            u = Utils()
            operand.append(operands[0].split('$')[1])
            operand.append(operands[2].split('$')[1])
            operand.append(operands[1])
            rs = u.int2bs(operand[0], 5)
            ra = u.int2bs(operand[1], 5)
            si = u.int2bs(operand[2], 16)
            binary = binary + rs + ra + si
            return(binary)
        elif (operator == 'stwu'):
            opcode = '100101'
            binary = opcode
            operands = list(operands)
            u = Utils()
            operand.append(operands[0].split('$')[1])
            operand.append(operands[2].split('$')[1])
            operand.append(operands[1])
            rs = u.int2bs(operand[0], 5)
            ra = u.int2bs(operand[1], 5)
            si = u.int2bs(operand[2], 16)
            binary = binary + rs + ra + si
            return(binary)
        elif (operator == 'lhz'):
            opcode = '101000'
            binary = opcode
            operands = list(operands)
            u = Utils()
            operand.append(operands[0].split('$')[1])
            operand.append(operands[2].split('$')[1])
            operand.append(operands[1])
            rt = u.int2bs(operand[0], 5)
            ra = u.int2bs(operand[1], 5)
            si = u.int2bs(operand[2], 16)
            binary = binary + rt + ra + si
            return(binary)
        elif (operator == 'lha'):
            opcode = '101010'
            binary = opcode
            operands = list(operands)
            u = Utils()
            operand.append(operands[0].split('$')[1])
            operand.append(operands[2].split('$')[1])
            operand.append(operands[1])
            rt = u.int2bs(operand[0], 5)
            ra = u.int2bs(operand[1], 5)
            si = u.int2bs(operand[2], 16)
            binary = binary + rt + ra + si
            return(binary)
        elif (operator == 'sth'):
            opcode = '101100'
            binary = opcode
            operands = list(operands)
            u = Utils()
            operand.append(operands[0].split('$')[1])
            operand.append(operands[2].split('$')[1])
            operand.append(operands[1])
            rs = u.int2bs(operand[0], 5)
            ra = u.int2bs(operand[1], 5)
            si = u.int2bs(operand[2], 16)
            binary = binary + rs + ra + si
            return(binary)
        elif (operator == 'lbz'):
            opcode = '100010'
            binary = opcode
            operands = list(operands)
            u = Utils()
            operand.append(operands[0].split('$')[1])
            operand.append(operands[2].split('$')[1])
            operand.append(operands[1])
            rt = u.int2bs(operand[0], 5)
            ra = u.int2bs(operand[1], 5)
            si = u.int2bs(operand[2], 16)
            binary = binary + rt + ra + si
            return(binary)
        elif (operator == 'stb'):
            opcode = '100110'
            binary = opcode
            operands = list(operands)
            u = Utils()
            operand.append(operands[0].split('$')[1])
            operand.append(operands[2].split('$')[1])
            operand.append(operands[1])
            rs = u.int2bs(operand[0], 5)
            ra = u.int2bs(operand[1], 5)
            si = u.int2bs(operand[2], 16)
            binary = binary + rs + ra + si
            return(binary)
        elif (operator == 'ld'):
            opcode = '111010'
            binary = opcode
            operands = list(operands)
            u = Utils()
            operand.append(operands[0].split('$')[1])
            operand.append(operands[2].split('$')[1])
            operand.append(operands[1])
            rt = u.int2bs(operand[0], 5)
            ra = u.int2bs(operand[1], 5)
            si = u.int2bs(operand[2], 14)
            binary = binary + rt + ra + si  + "00"
            return(binary)
        elif (operator == 'std'):
            opcode = '111110'
            binary = opcode
            operands = list(operands)
            u = Utils()
            operand.append(operands[0].split('$')[1])
            operand.append(operands[2].split('$')[1])
            operand.append(operands[1])
            rt = u.int2bs(operand[0], 5)
            ra = u.int2bs(operand[1], 5)
            si = u.int2bs(operand[2], 14)
            binary = binary + rt + ra + si  + "00"
            return(binary)
        elif (operator == 'bca'):
            opcode = '010011'
            binary = opcode
            operands = list(operands)
            u = Utils()
            operand.append(operands[0].split('$')[1])
            operand.append(operands[1].split('$')[1])
            operand.append(operands[2])
            bo = u.int2bs(operand[0], 5)
            bi = u.int2bs(operand[1], 5)
            bd = u.int2bs(operand[2], 14)
            binary = binary + bo + bi + bd  + "00"
            return(binary)
        elif (operator == 'b'):
            opcode = '010010'
            binary = opcode
            operands = list(operands)
            operand=str(operands[0])
            u = Utils()
            li = u.int2bs(operand, 24)
            binary = binary + li + '00'
            return (binary)
        elif (operator == 'ba'):
            opcode = '010010'
            binary = opcode
            operands = list(operands)
            operand = str(operands[0])
            u = Utils()
            li = u.int2bs(operand, 24)
            binary = binary + li + '10'
            return (binary)
        ###added by bhaskar
