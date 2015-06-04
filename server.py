import sys
import SocketServer
import urlparse
from BaseHTTPServer import HTTPServer, BaseHTTPRequestHandler  
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

class routeHandler(BaseHTTPRequestHandler):

	def getFile(self, filename):
		filename = filename.replace('/public','public')
		try:
			f = open(filename, 'rb')
		except Exception, e:
			raise e
		buf = f.read()
		f.close()
		return buf
	def do_GET(self):
		urlArg = urlparse.urlparse(self.path)
		uri = urlArg.path
		print 'REQUEST URI:: ' + uri
		if uri.endswith('.js'):
			#response js files
			js = self.getFile(uri)
			self.protocal_version = 'HTTP/1.1'
			self.send_response(200)
			self.send_header('Content-Type', 'text/javascript')
			# self.send_header('Content-Disposition', 'attachment;''filename=%s' % filename)      
			self.end_headers()
			self.wfile.write(js)
			del js
		elif uri.endswith('.html'):
			page = self.getFile(uri)
			self.protocal_version = 'HTTP/1.1'
			self.send_response(200)  
			self.send_header("Content-Type", "text/html")         
			self.end_headers()
			self.wfile.write(page)
			del page
		elif uri.endswith('.css'):
			#response css files
			css = self.getFile(uri)
			self.protocal_version = 'HTTP/1.1'
			self.send_response(200)  
			self.send_header("Content-Type", "text/css")         
			self.end_headers()
			self.wfile.write(css)
			del css
		elif uri == '/':
			#response index file /
			page = self.getFile('public/index.html')
			self.protocal_version = 'HTTP/1.1'
			self.send_response(200)  
			self.send_header("Content-Type", "text/html")         
			self.end_headers()
			self.wfile.write(page)
			del page
		elif uri.endswith('.map'):
			#deal with .map request which I dont quite understand comes from where
			self.protocal_version = 'HTTP/1.1'
			self.send_response(404)  
			self.send_header("Content-Type", "application/json")         
			self.end_headers()
			self.wfile.write('404 not found')

# if self.path.endswith(".map"):
# 				mimetype = "application/json"
# 				sendReply = Tru

	def start_server(port):  
		http_server = HTTPServer(('[IP]', int(port)), routeHandler)  
		http_server.serve_forever()

def main():
	PORT = 3000

	httpd = SocketServer.TCPServer(('0.0.0.0', PORT), routeHandler)

	print "serving at port", PORT
	httpd.serve_forever()

if __name__ == '__main__':
	main()