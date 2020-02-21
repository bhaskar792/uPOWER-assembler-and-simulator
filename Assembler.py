# =+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+
# MIPS Assembly to Hex Converter. 													 		     |
# =+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+
# Akshay Kashyap, Union College, Winter 2017. 										 			 |
# Built using code by Prof. John Rieffel, Union College, for CSC-270: Compiter Organization. 	 |
# =+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+

import sys
import getopt

from InstructionParser import InstructionParser

class Assembler(object):
	def __init__(self, infilenames, outfilename):
		self.infilenames = infilenames
		self.outfilename = outfilename

	def stripComments(self, line):				
		if not line:
			return ''

		cleaned = line
		if line.find('#') != -1:
			cleaned = line[0:line.find('#')] # Get rid of anything after a comment(#).

		return cleaned

	def buildLabelsMap(self, lines):					#build label map
		labelsMap = {}

		for lineNo, line in enumerate(lines):
			split = line.split(':', 1)
			if len(split) > 1:
				label = split[0]
				labelsMap[label] = lineNo

		return labelsMap

	def mergeInputFiles(self):						#given list of all input lines
		outlines = []

		for filename in self.infilenames:
			with open(filename) as f:
				outlines += f.readlines()

			f.close()

		return outlines				#return all the lines of assembly file

	def AssemblyToHex(self):
		'''given an ascii assembly file , read it in line by line and convert each line of assembly to machine code
		then save that machinecode to an outputfile'''
		inlines = self.mergeInputFiles()		#get all the lines from input in list
		outlines = []

		lines = map(lambda line: self.stripComments(line.rstrip()), inlines)  #get rid of \n whitespace at end of line #return either proper lines or empty item
		lines = filter(lambda line: line, lines)			#remove empty items

		labelsMap = self.buildLabelsMap(lines)				#build labelsmap like {'bro': 0, 'there': 2, 'hey': 3} and line numbers are correct
		parser = InstructionParser(labelsMap=labelsMap)

		outlines = map(lambda line: parser.convert(line, format='hex'), lines)

		with open(self.outfilename,'w') as of:
			of.write('v2.0 raw\n')
			for outline in outlines:
				of.write(outline)
				of.write("\n")
		of.close()

if __name__ == "__main__":
	print 'Number of arguments:', len(sys.argv), 'arguments.'
	print 'Argument List:', str(sys.argv)

	# try:
	# 	opts, args = getopt.getopt(sys.argv[1:], "hi:o:", ["ifile=","ofile="])
    # except getopt.GetoptError:
	# 	print 'Usage: python Assembler.py -i <inputfile.asm>[ <inputfile2.asm> <inputfile3.asm> ...] -o <outputfile.hex>'
	# 	sys.exit(2)
	#
	# inputfiles = map(lambda t: t[1], filter(lambda (opt, arg): opt == '-i', opts))
	# outputfile = map(lambda t: t[1], filter(lambda (opt, arg): opt == '-o', opts))

	if (len(sys.argv) < 4) or ('-i' not in sys.argv) or ('-o' not in sys.argv):
		print('Usage: python Assembler.py -i <inputfile.asm>[ <inputfile2.asm> <inputfile3.asm> ...] -o <outputfile.hex>')
		sys.exit(2)

	inputfiles = sys.argv[sys.argv.index('-i') + 1: sys.argv.index('-o')]
	outputfile = sys.argv[sys.argv.index('-o') + 1]

	assembler = Assembler(inputfiles, outputfile)
	assembler.AssemblyToHex()
