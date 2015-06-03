from HTMLParser import HTMLParser
from htmlentitydefs import name2codepoint
import re

class sipMsg:
    def __init__(self, direction, msgFrom, to, time, method, statuscode, sipCallId, isRequest, msg):
        self.direction = direction
        self.msgFrom = msgFrom
        self.to = to
        self.time = time
        self.method = method
        self.statuscode = statuscode
        self.sipCallId = sipCallId
        self.isRequest = isRequest
        self.meg = msg
    def parseMsg(self):
        print 'parseMsg'

class MyHTMLParser(HTMLParser):
    def handle_starttag(self, tag, attrs):
        print "Start tag:", tag
        return
        tmpMsg = sipMsg()
        for attr in attrs:
            if attr[0] == 'direction':
                tmpMsg.direction = attr[1]
            if attr[0] == 'from':
                tmpMsg.msgFrom = attr[1]
            if attr[0] == 'to':
                tmpMsg.to = attr[1]
            if attr[0] == 'time':
                tmpMsg.time = attr[1]
            if attr[0] == 'method':
                tmpMsg.method = attr[1]
            if attr[0] == 'statuscode':
                tmpMsg.statuscode = attr[1]
            if attr[0] == 'sipCallId':
                tmpMsg.sipCallId = attr[1]
            if attr[0] == 'isRequest':
                tmpMsg.isRequest = attr[1]
        return tmpMsg

    def handle_endtag(self, tag):
        print "End tag  :", tag

    def handle_data(self, data):
        print "     DATA:", data

    def handle_comment(self, data):
        if (data.find('CDATA') != -1):
            print "MSG     :", data
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
    parser = MyHTMLParser()
    f = open('sipserver118.1.trace', 'r')
    fileData = f.read()
    repData = fileData.replace('<![', '<!--[')
    repData = repData.replace(']>', ']-->')
    parser.feed(repData)
    f.close()
    # print parser.get_starttag_text()

if __name__ == '__main__':
    main()