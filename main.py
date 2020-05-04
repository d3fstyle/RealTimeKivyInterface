"""
    Kivy interface to show data received from UDP in real time.
"""
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.label import Label
from kivy.properties import StringProperty, NumericProperty, ObjectProperty
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.uix.screenmanager import ScreenManager, Screen, NoTransition
from kivy.uix.checkbox import CheckBox
from kivy.uix.textinput import TextInput
from Queue import Queue
from kivy.core.text import LabelBase


import random
import logging
import select
import socket
import threading
import sys
import struct


"""
    Defines
"""
Window.clearcolor = (.93, .93, .93, 1)
columns = ['one', 'two', 'three', 'four', 'five']
rows = ['one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight']
dataqueue = Queue()
UPDATE_DELAY = 0.5

"""
    Interface font
"""
KIVY_FONTS = [
    {
        "name": "Xolonium",
        "fn_regular": "data/fonts/Xolonium-Regular.otf",
        "fn_bold": "data/fonts/Xolonium-Bold.otf"
    },
    {
        "name": "IconFont",
        "fn_regular": "data/fonts/guifont.otf"
    }
]

for font in KIVY_FONTS:
    LabelBase.register(**font)

"""
    UDP listener
"""
open_sockets = []


class UDPClient(threading.Thread):
    def __init__(self, queue, IPAddress, portNumber):
        threading.Thread.__init__(self)
        self.bufferSize = 28
        self.queue = dataqueue
        self.IPAddress = IPAddress
        self.portNumber = portNumber
        self.client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        try:
            self.client.bind((self.IPAddress, self.portNumber))
            self.client.setblocking(1)
            self.client.listen(5)

        except:
            logging.info('[UDPclient | connect] - Exception')

    def run(self):
        while True:
            read_sockets, write_sockets, error_sockets = select.select([self.client]+open_sockets, [], [])
            message = read_sockets[0].recv(27)
            if message == "":
                logging.info('[UDPClient | run ] - Message empty')
            else:
                command, user, measure1, measure2, measure3, measure4, measure5 = struct.unpack('<I3sIffff', message)
                unpackedList = [command, user, measure1, measure2, measure3, measure4, measure5]
                self.queue.put(unpackedList)

    def close(self):
        try:
            self.client.close()
        except:
            pass
"""
    Kivy Interface: main screen
"""


class MainScreen(Screen):

    def __init__(self, **kwargs):
        super(MainScreen, self).__init__(**kwargs)
        Clock.schedule_interval(self.updateGui, UPDATE_DELAY)  
        self.measureToShow = 'A'

    def updateGui(self, *args):
        try:
            dataList = dataqueue.get(False)  
        except:
            pass
        else:
            self.ids[rows[dataList[0]-1]+'_'+columns[0]].text = str(dataList[1])

            if dataList[2] > 110:
                self.ids[rows[dataList[0]-1]+'_'+columns[1]].text = str('[color=ff0000]<[/color]' + str(dataList[2]) + '[color=ff0000]>[/color]')
            elif dataList[2] < 90:
                self.ids[rows[dataList[0]-1]+'_'+columns[1]].text = str('[color=00ff00]<[/color]' + str(dataList[2]) + '[color=00ff00]>[/color]')
            else:
                self.ids[rows[dataList[0]-1]+'_'+columns[1]].text = str(dataList[2])

            aux = float('%.2f'%dataList[3])
            self.ids[rows[dataList[0]-1]+'_'+columns[2]].text = str(aux)

            if self.measureToShow == 'A':
                aux = float('%.2f'%dataList[4])
                self.ids[rows[dataList[0]-1]+'_'+columns[3]].text = str(aux)
            else:
                aux = float('%.2f'%dataList[5])
                self.ids[rows[dataList[0]-1]+'_'+columns[3]].text = str(aux)

            aux = float('%.2f'%dataList[6])
            self.ids[rows[dataList[0]-1]+'_'+columns[4]].text = str(aux)

    def alternateMeasure(self, *args):
        if self.measureToShow == 'A':
            self.ids['AoB'].text = 'd'
            self.measureToShow = 'B'
        else:
            self.ids['AoB'].text = 'c'
            self.measureToShow = 'A'


"""
    Kivy Interface: settings screen
"""


class MenuScreen(Screen):
    pass

"""
    Create the screen manager
"""


class Manager(ScreenManager):

    screen_menu = ObjectProperty(None)
    screen_main = ObjectProperty(None)

"""
    Main
"""


class PaddleBeatApp(App):

    def build(self):
        m = Manager(transition=NoTransition())
        m.current = 'screenMain'
        crudeclock = MainScreen()
        listenerThread = UDPClient(dataqueue, '192.168.1.40', 2222)
        listenerThread.setDaemon(True)
        listenerThread.start()
        return m

"""
    Where magic occurs!
"""
if __name__ == '__main__':
    PaddleBeatApp().run()
