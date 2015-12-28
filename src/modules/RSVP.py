from framework.latentmodule import LatentModule
from serial import *
from direct.gui.OnscreenImage import OnscreenImage
import io, os, glob
# import matplotlib.pyplot as plt
from numpy import *
import time
import pylsl.pylsl as pylsl


class Main (LatentModule):
    def __init__ (self):
        LatentModule.__init__(self)

    def ReadData (self,f):
        data=[]
        marker=[]

        for columns in (raw.strip().split() for raw in f):
            data.append(columns[0])
            marker.append(columns[1])

        data.remove(data[0])
        marker.remove(marker[0])
        marker.remove(marker[1])
        marker.remove(marker[-1])
        num=len(data) - 2
        f.close()
        return data,marker,num

    def PlotTime(self, time_interval):

        plt.hist(time_interval)
        plt.title('Histogram of actural time interval')
        plt.xlabel('Time interval (s)')
        plt.ylabel('Number')
        plt.show()

    #-----------------------------------display stimulus--------------------------
    def ImageStimulus (self,data):
        # self.write('We will present image stimulus.\n Press the space bar when you are ready','space')
        # self.marker(11)
        # self.write('We will display a crossshair on the screen, please fix it',duration=1)
        # self.crosshair(duration=0.1)

        # preloading images
        image=[]

        for i in range(0,len(data)):
            image.append(OnscreenImage(data[i]))

        # display images
        image_time=[] # get time


        ti=0.125 # timer interval
        for i in range(0,len(data)-1):
            image_time.append(time.time())
            if i != 0:
                self.marker(1)
            self.picture(image[i],duration=ti,scale=1.2)
            image[i] = None

        self.picture(image[i+1],duration=ti,scale=1)
        image[i+1] = None
        image_time=array(image_time)
        time_interval=diff(image_time)



        return time_interval[1:-1], image_time[1:-1]
    #-----------------------------------------------------------------------------
    def run (self):
        # f=open('C:\\Users\\villa_000\\Dropbox\\python\\labstreaminglayer-master\\App\\SNAP\\src\\studies'
        #        '\\Image1\\RSVP.txt','rb')
        # data,marker,num=self.ReadData()
        # print '\n\nImage name:\n'
        # print data[1:-1]
        # print '\nMarker:\n'
        # print marker
        # time_interval,image_time, image=self.ImageStimulus(data)
        # print time_interval[1:-1], num
        # self.PlotTime(time_interval[1:])
        # print image_time[1:-1]



        # --------------------------------trial1-----------------------------------------------------

        # mac

        f1=open('/Users/Villa/Dropbox/python/labstreaminglayer-master/App/SNAP/src/studies'
                   '/trial1/RSVP.txt','rb')

        # win

        # f1=open('C:\\Users\\Villa_000\\Dropbox\\python\\labstreaminglayer-master\\App\\SNAP\\src\\studies'
        #        '\\trial1\\RSVP.txt','rb')


        data,marker1,num=self.ReadData(f1)
        self.write('We will present image stimulus.\n Press the space bar when you are ready','space')
        self.write('Trial1',duration=2)
        self.crosshair(duration=0.1)
        time_interval1,image_time1=self.ImageStimulus(data)

        # ----------------------------------trial2-----------------------------------------------------

        # mac

        f2=open('/Users/Villa/Dropbox/python/labstreaminglayer-master/App/SNAP/src/studies'
               '/trial2/RSVP.txt','rb')

        # win

        # f2=open('C:\\Users\\Villa_000\\Dropbox\\python\\labstreaminglayer-master\\App\\SNAP\\src\\studies'
        #        '\\trial2\\RSVP.txt','rb')

        data,marker2,num=self.ReadData(f2)
        self.write('Trial2',duration=2)
        self.crosshair(duration=0.1)
        time_interval2,image_time2=self.ImageStimulus(data)


        print time_interval1, time_interval2





        # self.PlotTime([time_interval1,time_interval2])



