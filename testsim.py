x=10000000
REG=[0]*32
REG[0]=1
REG[1]=1
REG[2]=3
REG[3]=4
REG[4]=5
while(x<10000005):
    if(x==10000000):
        REG[0]=REG[0]+REG[1]
        print(REG[0])
    if(x==10000004):
        if(REG[4]>REG[0]):
            x=10000000
            continue

    x=x+4

