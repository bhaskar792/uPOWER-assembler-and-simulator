class LookupTables:
    INSTRUCTIONS = {
        'XO-TYPE': {    # opcode   OE  RC    XO
            'add':      (0b011111,0b0,0b0,0b100001010, ['rt', 'ra', 'rb']),
            'sub':      (0b011111,0b0,0b0,0b000101000, ['rt', 'ra', 'rb']),
        },
        'D-TYPE': {     # opcode    
            'addi':     (0b001110, ['rt', 'ra']),
            'addis':    (0b001111, ['rt', 'ra']),
            'andi':     (0b011100, ['ra', 'rs']),
            'ori':      (0b011000, ['ra', 'rs']),
            'xori':     (0b011010, ['ra', 'rs']),
            'lwz':      (0b100000, ['rt', 'ra']),
            'stw':      (0b100100, ['rs', 'ra']),
            'stwu':     (0b100101, ['rs', 'ra']),
            'lhz':      (0b101000, ['rt', 'ra']),
            'lha':      (0b101010, ['rt', 'ra']),
            'sth':      (0b101100, ['rs', 'ra']),
            'lbz':      (0b100010, ['rt', 'ra']),
            'stb':      (0b100110, ['rs', 'ra']),
            'cmpi':     (0b001011, [])     #Remaining...
        },
        'X-TYPE': {     # opcode    Rc       xo 
            'and':      (0b011111, 0b0, 0b0000011100, ['ra', 'rs', 'rb']),
            'extsw':    (0b011111, 0)
            'nand':     (0b011111, 0b0, 0b0111011100, ['ra', 'rs', 'rb']),
            'or':       (0b011111, 0b0, 0b0110111100, ['ra', 'rs', 'rb']),
            'xor':      (0b011111, 0b0, 0b0100111100, ['ra', 'rs', 'rb']),
            'sld':      (0b011111, 0b0, 0b0111011100, ['ra', 'rs', 'rb']),
            'srd':      (0b011111, 0b0, 0b1000011011, ['ra', 'rs', 'rb']),
            'srad':     (0b011111, 0b0, 0b1100011010, ['ra', 'rs', 'rb']),
            'cmp':
        },
        'DS-TYPE': {    # opcode    Xo
            'ld':       (0b111010, 0b00, ['rt', 'ra']),
            'std':      (0b111110, 0b00, ['rs', 'ra'])
        },
        'XS-TYPE': {    # opcode    Rc       Xo
            'sradi':    (0b011111, 0b0, 0b110011101, ['ra', 'ra'])
        },
        'B-TYPE': {     # opcode   AA   LK
            'bc':       (0b010011, 0b0, 0b0, ['bo', 'bi']),
            'bca':      (0b010011, 0b1, 0b0, ['bo', 'bi'])  
        },
        'I-TYPE': {     # opcode    AA    LK 
            'b':        (0b010010, 0b0, 0b0),
            'ba':       (0b010010, 0b0, 0b0)
        }
        'SC-TYPE': {    # opcode
            'sc':       (0b010001)
        }

    }