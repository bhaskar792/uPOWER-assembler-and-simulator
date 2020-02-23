class map(object):
    def __init__(self):
        pass
    def buildTextMap(self,lines):
        labelsMap = {}
        count = 400000
        for lineNo, line in enumerate(lines):
            split = line.split(':', 1)
            if len(split) > 1:
                label = split[1].strip()
                labelsMap[label] = count
                count = count + 4

        return labelsMap


