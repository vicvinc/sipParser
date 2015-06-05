import sys
import SocketServer
import urlparse
import json
from dataParser import *
from BaseHTTPServer import HTTPServer, BaseHTTPRequestHandler

class data:
	def __init__(self, file):
		self.msgFlow  = ''
		self.msgFlowJson = ''
		self.filePath = file

	def formate(self):
		data = dataFormat(self.filePath)
		data.readData()
		data.formatData()
		
		parser = dataParser()
		parser.init()
		parser.feed(data.getFormatedData())
		self.msgFlow = parser.getMsgFlow()
		# printFlow(parser.getMsgFlow())

	def getMsgFlow(self):
		return self.msgFlow

	def getMsgFlowJson(self):
		self.msgFlowJson = json.dumps(self.msgFlow)
		return self.msgFlowJson

	def printFlow(self):
		for m in self.msgFlow:
			print m.direction
			print m.msgFrom
			print m.to
			# print time.strftime("%D %H:%M", time.localtime(int(m.time + '')))
			print m.time
			print m.method
			print m.statuscode
			print m.sipCallId
			print m.isRequest
			print m.msg

	def toJson(self):
		kvpair = dict()
		jsonList = list()
		for m in self.msgFlow:
			kvpair['direction'] = m.direction
			kvpair['msgFrom'] = m.msgFrom
			kvpair['to'] = m.to
			kvpair['time'] = m.time			
			# print time.strftime("%D %H:%M", time.localtime(int(m.time + '')))
			kvpair['method'] = m.method
			kvpair['statuscode'] = m.statuscode
			kvpair['sipCallId'] = m.sipCallId
			kvpair['isRequest'] = m.isRequest
			kvpair['msg'] = m.msg
			jsonList.append(json.dumps(kvpair))
		return json.dumps(jsonList)

	def __enter__(self):
		return self

	def __exit__(self, type, value, traceback):
		for file in self.files:
			os.unlink(file)
		del self

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

		if uri == '/':
			#response index file /
			page = self.getFile('public/index.html')
			self.protocal_version = 'HTTP/1.1'
			self.send_response(200)  
			self.send_header("Content-Type", "text/html")         
			self.end_headers()
			self.wfile.write(page)
			del page
		elif uri.endswith('.js'):
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
		elif uri.endswith('.ico'):
			ico = self.getFile(uri)
			self.protocal_version = 'HTTP/1.1'
			self.send_response(200)  
			self.send_header("Content-Type", "image/png")         
			self.end_headers()
			self.wfile.write(ico)
		elif uri.endswith('.map'):
			#deal with .map request which I dont quite understand comes from where
			self.protocal_version = 'HTTP/1.1'
			self.send_response(404)  
			self.send_header("Content-Type", "application/json")         
			self.end_headers()
			self.wfile.write('404 not found')
		elif uri.endswith('.data'):
			self.protocal_version = 'HTTP/1.1'
			self.send_response(200)  
			self.send_header("Content-Type", "application/json")         
			self.end_headers()
			tmpData = data('data/sipserver130.1.trace')
			tmpData.formate()
			# tmpData.printFlow() 
			buf = tmpData.getMsgFlow()
			jsonData = tmpData.toJson()
			# print jsonData
			self.wfile.write(jsonData)
			del tmpData

# if self.path.endswith(".map"):
# 				mimetype = "application/json"
# 				sendReply = Tru

	def start_server(port):  
		http_server = HTTPServer(('[IP]', int(port)), routeHandler)  
		http_server.serve_forever()

	def __enter__(self):
		return self

	def __exit__(self, type, value, traceback):
		for file in self.files:
			os.unlink(file)
		del self
		
def main():
	PORT = 3000

	httpd = SocketServer.TCPServer(('0.0.0.0', PORT), routeHandler)

	print "serving at port", PORT
	httpd.serve_forever()

if __name__ == '__main__':
	main()