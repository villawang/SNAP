from framework.basicstimuli import BasicStimuli
from psychopy import visual,core,event # import some libraries from PsychoPy
from serial import *
import io, os, glob 
import matplotlib.pyplot as plt
from pylab import *

class Main(BasicStimuli):
    def __init__(self):
        BasicStimuli.__init__(self)

    def define_path(self):
        os.chdir("C:\\Users\\villa_000\\Dropbox\\python\\RSVP\\image1")

    # read data from text file
    def read_data(self):
    #    data=[]
    #    f=io.open('RSVP.txt','r')
    #    data0=f.readlines()
    #    for i in range(0,len(data0)):
    #        if data0[i]!='\n':# remove blank newlines
    #            data.append(data0[i])
    #    for i in range(0,len(data)):
    #        data[i]=data[i].replace('\n','')
    #    num=sum(1 for _ in data)
    #    f.close()
        f=open('RSVP.txt','rb')
        data=[]
        marker=[]
        for columns in (raw.strip().split() for raw in f):
            data.append(columns[0])
            marker.append(columns[1])
        data.remove(data[0])
        marker.remove(marker[0])
        num=len(data)

        return data,marker,num       # returns data text file and number images

    # def trigger(marker):
    #    port=parallel.ParallelPort(address=0x0378)
    #    trigger_port=port.setData( int("00000000",2) ),port.setData( int("00000001",2) )#pin2 low      pin2 high
    #    return trigger_port


    def win_display(self):
        win=visual.Window([1000,800])
        return win

    def RSVP_paradigm(sefl,data,ti,win,marker):
    # data is text file, ti is time interval between each image
        result=[] # define output



        message = visual.TextStim(win, text='Loading images.....')
        message.draw()
        win.update()

        image_list=[] # preload image list


        # preload images
        for i in range(0,len(data)):
            image_list.append(visual.ImageStim(win,data[i],size=(2,2)))


        # -----------------------------------------fixation----------------------------
        message1 = visual.TextStim(win, text='Attention please')
        message1.draw()
        win.update()
        core.wait(1.0)
        fixation = visual.ShapeStim(win,
        vertices=((0, -0.2), (0, 0.2), (0,0), (-0.2,0), (0.2, 0)),
        lineWidth=5,
        closeShape=False,
        lineColor='white')
        fixation.draw()
        win.update()
        core.wait(3.0)
        onsetTime=core.getTime()

        #----------------------------------------define timing------------------------
        image_time=[] # interval between two stimuli
        RT=[]         # subjective reaction time and the choice of stimuli target
        t_remaining=[] # time of code exeuating



        # ----------------------------------display stimuli----------------------
        for i in range(0,len(data)):
            t_start=core.getTime()
            image_time.append(core.getTime())
            image=image_list[i]
            # if marker[i]==True:
            #     trigger(marker)[1]
            # else:
            #     trigger(marker)[0]
            image.draw()
            win.flip()
            keys = event.getKeys(keyList=['space', 'escape'])
            if keys:
                RT.append([core.getTime(),i])
            t_elipse=core.getTime()
            t_remaining.append(t_elipse-t_start)
            core.wait(ti-t_remaining[i])
        win.close()

        # store output
        result.append(RT)
        result.append(image_time)
        result.append(t_remaining)
        return result, win

    # ----------------------------check the actual time interval------------------------------
    def plot_ti(self,ti):
        plt.hist(ti)
        plt.title('Histogram of actrual time interval')
        plt.xlabel('Time interval (s)')
        plt.ylabel('Number')
        plt.show()

    def calculate_ti(self,image_time):
        ti=[]     # actual time interval
        for i in range(1,len(image_time)):
            ti.append(image_time[i]-image_time[i-1])
        return ti
    #------------------------------------------------------------------------------------------

    def run(self):
        self.define_path()
        data,marker,num=self.read_data()
        win=self.win_display()
        result,win=self.RSVP_paradigm(data,0.1,win,marker)
        ti=self.calculate_ti(result[1])
        self.plot_ti(ti)
        print data, marker  # 1 is target, 0 is non-target


    # if __name__=='__main__':
    #     main()



