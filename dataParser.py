from HTMLParser import HTMLParser
from htmlentitydefs import name2codepoint
import re
import time

class sipMsg:
    def __init__(self, direction = '', \
            msgFrom = '', to = '', time = '', method = '', \
            statuscode = '', sipCallId = '', isRequest = '', msg = ''):

        self.direction = direction
        self.msgFrom = msgFrom
        self.to = to
        self.time = time
        self.method = method
        self.statuscode = statuscode
        self.sipCallId = sipCallId
        self.isRequest = isRequest
        self.msg = msg
    def parseMsg(self):
        print 'parseMsg'

class MyHTMLParser(HTMLParser):
    def setMsgFlow(self, msgArr):
        self.msgArr = msgArr
        self.tmpMsg = sipMsg()
    def handle_starttag(self, tag, attrs):
        # print "Start tag:", attrs
        for attr in attrs:
            if attr[0] == 'direction':
                self.tmpMsg.direction = attr[1]
            if attr[0] == 'from':
                self.tmpMsg.msgFrom = attr[1]
            if attr[0] == 'to':
                self.tmpMsg.to = attr[1]
            if attr[0] == 'time':
                self.tmpMsg.time = attr[1]
            if attr[0] == 'method':
                self.tmpMsg.method = attr[1]
            if attr[0] == 'statuscode':
                self.tmpMsg.statuscode = attr[1]
            if attr[0] == 'sipCallId':
                self.tmpMsg.sipCallId = attr[1]
            if attr[0] == 'isRequest':
                self.tmpMsg.isRequest = attr[1]
        
    def handle_endtag(self, tag):
        self.msgArr.append(self.tmpMsg) 
        self.tmpMsg = sipMsg()
    # def handle_data(self, data):
    #     #self.tmpMsg.msg = data
    #     print "data     :", data
    def handle_comment(self, data):
        if (data.find('CDATA') != -1):
            self.tmpMsg.msg = data
    def handle_entityref(self, name):
        c = unichr(name2codepoint[name])
        print "Named ent:", c
    def handle_charref(self, name):
        if name.startswith('x'):
            c = unichr(int(name[1:], 16))
        else:
            c = unichr(int(name))
        print "Num ent  :", c
    def handle_decl(self, data):
        print "Decl     :", data
    # def get_starttag_text(self, data):
    #     print "message  :", data
def main():
    
    msgFlow = list()
    parser = MyHTMLParser()
    parser.setMsgFlow(msgFlow)

    f = open('sipserver118.1.trace', 'r')
    fileData = f.read()
    repData = fileData.replace('<![', '<!--[')
    repData = repData.replace(']>', ']-->')
    # print repData
    parser.feed(repData)
    flow = parser.msgArr
    for m in flow:
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
    f.close()
    # print parser.msgArr
    # print parser.get_starttag_text()

if __name__ == '__main__':
    main()