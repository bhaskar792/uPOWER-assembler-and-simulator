import re

rtyperegex=r'(\w+)\s+(\$\d+)\s+(\$\d+)\s+(\$\d+)'

instrregex=re.compile(rtyperegex)

match=instrregex.match('add $1 $2 $3')

if match:
    print(" matching")
print(match.groups())
group=match.groups()


print(group[0])