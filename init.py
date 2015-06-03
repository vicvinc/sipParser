import sys
import getopt

print 'env test ok'
class sipEnv:
	def __init__(self, path, logFile, resultFile):
		self.path = path
		self.logFile = logFile
		self.resultFile = resultFile
	def getPath(self):
		return self.path
	def getLogFile(self):
		return self.logFile
	def getResultFile(self):
		return self.reusltFile
#class parser:
	
def main():
	try:
		opts,args = getopt.getopt(sys.argv[1:], 'h', ['help'])
	except getopt.error, msg:
		print msg
		print 'for help use --help'
		sys.exit(2)
	for o, a in opts:
		if o in ('-h', '--help'):
			print __doc__
			sys.exit(0)
	for arg in args:
		#process(arg) # process defs processor
		print arg

if __name__ == '__main__':
	main()


