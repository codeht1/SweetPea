import sys
from PySide.QtCore import *
from PySide.QtGui import *
import mainGui
import time



import urllib
import re
from bs4 import BeautifulSoup
import summarize



import pyttsx
# NOTE: this requires PyAudio because it uses the Microphone class
import speech_recognition as sr




class SwtPBrowser(QMainWindow,mainGui.Ui_SweetPea):
    def __init__(self,parent=None):
        super(SwtPBrowser,self).__init__(parent)

        self.setupUi(self)

        self.addrsBar.returnPressed.connect(self.search)
        self.back.clicked.connect(self.webView.back)
        self.forward.clicked.connect(self.webView.forward)
        self.cancel.clicked.connect(self.webView.stop)
        self.reload.clicked.connect(self.webView.reload)
        self.mic.clicked.connect(self.startAudioCmds)

        self.webView.titleChanged.connect(self.changeWindowTitle)
        self.webView.urlChanged.connect(self.changeUrl)
        #self.webView.loadFinished.connect(self.startReading)
        # self.readingThread = readingThread()
        # self.startReading.clicked.connect(self.readingThread.read(self.webView.url))





    def search(self):
        #TODO: check out this code, ensure it does cover all the posibilities
        theUrl = self.addrsBar.text()
        regrex = "[*.*]"
        pattern = re.compile(regrex)
        status = re.findall(pattern,theUrl)
        if(status):
            if theUrl[0:4] != 'http':
                theUrl = 'http://' + theUrl
        else:
            theUrl = "https://www.google.co.in/webhp?sourceid=chrome-instant&ion=1&espv=2&ie=UTF-8#q="+theUrl
        self.webView.setUrl(QUrl(theUrl))


    def changeWindowTitle(self):
        """
        Public Slot invoked when the title of the page changes. All we do is to display it as the main window title.
        """
        title = self.webView.title()
        self.setWindowTitle(str(title))


    def changeUrl(self):
        """
        Public Slot invoked when the url changes. All we do is display the current url in txtUrl.
        """
        url = self.webView.url().toString()
        self.addrsBar.setText(url)

    def startReadingPage(self):
        """
        Public Slot invoked when the title of the page changes. All we do is to display it as the main window title.
        """
        theUrl = self.addrsBar.text()
        if theUrl[0:4] != 'http':
            theUrl = 'http://' + theUrl
        url = str(theUrl)
        html = urllib.urlopen(url).read()
        soup = BeautifulSoup(html)

            # kill all script and style elements
        for script in soup(["script", "style"]):
            script.extract()    # rip it out

            # get text
        text = soup.get_text()


        # Adding summarizer code



        #Summarizer Code
        ss = summarize.SimpleSummarizer()
        summary = ss.summarize(text, 10)
        print summary
        #Summarizer code



        # break into lines and remove leading and trailing space on each
        lines = (line.strip() for line in text.splitlines())
            # break multi-headlines into a line each
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
            # drop blank lines
        text = '\n'.join(chunk for chunk in chunks if chunk)

            #print(text)
        engine = pyttsx.init()
        engine.say(text)
            #print "Hello"
        engine.runAndWait()




    def startAudioCmds(self):
        r = sr.Recognizer()
        status = True
        command = "default"

        with sr.Microphone() as source:               # use the default microphone as the audio source
            audio = r.listen(source)                   # listen for the first phrase and extract it into audio data

        try:
            command=r.recognize(audio)
            engine = pyttsx.init()
            engine.say("You said"+command)
            engine.runAndWait()                       
        except LookupError:                            # speech is unintelligible
            engine = pyttsx.init()
            engine.say("Could not understand audio Try again!")
            engine.runAndWait()

        command = command.lower()
        decision = command.split(" ")[0]
        if(decision=="open"):
            print decision
            #theUrl = command.split(" ")[1]
            word, space, rest = command.partition(' ')
            theUrl = rest
            self.addrsBar.setText(theUrl)
            self.search()
        elif(command=="go back"):
            self.webView.back()
        elif(command=="go forward"):
            self.webView.forward()
        elif(command=="cancel"):
            self.webView.stop()
        elif(command=="reload"):
            self.webView.reload()
        elif(command=="read"):
            self.startReadingPage()
            #self.readingThread.start(self.webView.url)   
        else:
            #directly throwing command in google search
            theUrl = command
            self.addrsBar.setText(theUrl)
            self.search()
            #print "command not recognized"

# class readingThread(QThread):
#     def __init__(self,parent=None):
#         super(readingThread,self).__init__(parent)

#     def read(self,url):
#         url = str(url)
#         html = urllib.urlopen(url).read()
#         soup = BeautifulSoup(html)

#             # kill all script and style elements
#         for script in soup(["script", "style"]):
#             script.extract()    # rip it out

#             # get text
#         text = soup.get_text()


#         # Adding summarizer code



#         #Summarizer Code
#         ss = summarize.SimpleSummarizer()
#         summary = ss.summarize(text, 10)
#         print summary
#         #Summarizer code



#         # break into lines and remove leading and trailing space on each
#         lines = (line.strip() for line in text.splitlines())
#             # break multi-headlines into a line each
#         chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
#             # drop blank lines
#         text = '\n'.join(chunk for chunk in chunks if chunk)

#             #print(text)
#         engine = pyttsx.init()
#         engine.say(text)
#             #print "Hello"
#         engine.runAndWait()



app = QApplication(sys.argv)
SweetPea = SwtPBrowser()
SweetPea.show()
app.exec_()