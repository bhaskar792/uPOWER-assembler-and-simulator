class InstructionLookup:
    def __init__(self):
        self.opcodeDict = {
        	'XO-TYPE': {
        		'add': 0,
        		'subf': 1
        	},
            'D-TYPE': {
                'addi': 2,
                'addis': 3,
                'andi': 4,
                'ori': 5,
                'xori': 6,
                'lwz': 7,
                'stw': 8,
                'stwu': 9,
                'lhz': 10,
                'lha': 11,
                'sth': 12,
                'lbz': 13,
                'stb': 14,
                'cmpi': 15
            },
            'X-TYPE':{
                'and': 16,
                'or': 17,
                'nand': 18,
                'extsw': 19,
                'xor': 20,
                'sld': 21,
                'srd': 22,
                'srad': 23,
                'cmp': 24
            },
        	'DS-TYPE': {
                'ld': 25,
                'std': 26
            },
            'XS-TYPE': {
                'sradi': 27
            },
            'B-TYPE': {
                'bc': 28,
                'bca': 29
            },
            'I-TYPE': {
                'b': 30,
                'ba': 31,
                'bl':32
            },
            'SC-TYPE': {
                'sc': 32
            },
            'LDATA-TYPE':{
                'ldata': 33
            }
        }

    def type(self, operator):
        for k in self.opcodeDict:
            if operator in self.opcodeDict[k]:
                return k

        return ''

    def opcode(self, operator):
        k = self.type(operator)
        if k == '':
            return -1

        return self.opcodeDict[k][operator]

