# Regular Expression

# XO   #done
# add rt, ra, rb  -   add $1 $2 $3
# subf rt, ra, rb -   subf $1 $2 $3
# (add)\s+(\$\d+)\s+(\$\d+)\s+(\$\d+)|(subf)\s+(\$\d+)\s+(\$\d+)\s+(\$\d+)



# DS            #done
# ld RT,DS(RA)  -  ld $1 6($3)
# std RS,DS(RA) -  std $1 7($6)
# r'(ld)\s+(\$\d+)\s+(\d+)+\(+(\$\d+)+\)|(std)\s+(\$\d+)\s+(\d+)+\(+(\$\d+)+\)'


# SC
# sc LEV
#r'(sc)'



# I         #done
# b li, ba li, bl li
# (bl)\s+(\w+)|(ba)\s+(\w+)|(li)\s+(\w+)



# X         Done
# and RA,RS,RB
# nand RA,RS,RB
# extsw RA, RS
# or RA,RS,RB
# xor RA RS RB
# sld RA, RS, RB
# srd RA, RS, RB
# srad RA, RS, RB
# cmp BF,L,RA,RB0 not in RE

# r'(and)\s+(\$\d+)\s+(\$\d+)\s+(\$\d+)|(nand)\s+(\$\d+)\s+(\$\d+)\s+(\$\d+)|(extsw)\s+(\$\d+)\s+(\$\d+)|(or)\s+(\$\d+)\s+(\$\d+)\s+(\$\d+)|(xor)\s+(\$\d+)\s+(\$\d+)\s+(\$\d+)|(sld)\s+(\$\d+)\s+(\$\d+)\s+(\$\d+)|(srd)\s+(\$\d+)\s+(\$\d+)\s+(\$\d+)|(srad)\s+(\$\d+)\s+(\$\d+)\s+(\$\d+)'



# XS        #done
# sradi RA,RS, SH
# r'(sradi)\s+(\$\d+)\s+(\$\d+)\s+(\d+)'


#D
# addi RT,RA,SI
# addis RT, RA, SI
# andi RA,RS,UI
# ori RA,RS,UI
# xori RA,RS,UI
# lwz RT,D(RA)
# stw RS,D(RA)
# stwu RS,D(RA)
# lhz RT,D(RA)
# lha RT,D(RA)
# sth RS,D(RA)
# lbz RT,D(RA)
# stb RS,D(RA)

#  r'(addi)\s+(\$\d+)\s+(\$\d+)\s+(\d+)|(addis)\s+(\$\d+)\s+(\$\d+)\s+(\d+)|(andi)\s+(\$\d+)\s+(\$\d+)\s+(\d+)|(ori)\s+(\$\d+)\s+(\$\d+)\s+(\d+)|(xori)\s+(\$\d+)\s+(\$\d+)\s+(\d+)|(lwz)\s+(\$\d+)\s+(\d+)+\(+(\$\d+)+\)|(swz)\s+(\$\d+)\s+(\d+)+\(+(\$\d+)+\)|(stwz)\s+(\$\d+)\s+(\d+)+\(+(\$\d+)+\)|(lhz)\s+(\$\d+)\s+(\d+)+\(+(\$\d+)+\)|(lha)\s+(\$\d+)\s+(\d+)+\(+(\$\d+)+\)|(sth)\s+(\$\d+)\s+(\d+)+\(+(\$\d+)+\)|(lbz)\s+(\$\d+)\s+(\d+)+\(+(\$\d+)+\)|(stb)\s+(\$\d+)\s+(\d+)+\(+(\$\d+)+\)'

#B          #done
#bc $1 $2 label
#r'(bc)\s+(\$\d+)\s+(\$\d+)\s+(\d+)|(bca)\s+(\$\d+)\s+(\$\d+)\s+(\d+)'

# XL
# (bclr)