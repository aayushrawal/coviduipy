#!/usr/bin/env python3
import sys
from os import path
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import (QWidget, QPushButton, QHBoxLayout, QVBoxLayout, QApplication,)
from radialbar import RadialBar
import serial
import serial.tools.list_ports
from cvwidget import MainWidget as FDWidget
from cvfrwidget import MainWidget as FRWidget
import pyqtgraph as pg
import time
import radardata
import csv
from datetime import datetime

import mysql.connector
import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from time import strftime
#from email.MIMEImage import MIMEImage
from email.mime.image import MIMEImage



""" ports = list(serial.tools.list_ports.comports())
for p in ports:
    if("XeThru" in p.description):
        print("XeThru found at:",p.device)
        RadarPort = p.device
    elif("CDC" in p.description):
        print("Max found at:",p.device)
        MaxPort = p.device """

class SerialThread(QtCore.QThread):
    change_value = QtCore.pyqtSignal(str)
    #ser = serial.Serial("/dev/ttyACM2", 250000, timeout=0.1)
    _break = False
    #x4m200 = radardata.configure_x4m200(RadarPort, False, radardata.x4m200_par_settings)


    def run(self):

        
        #record = False
        """ x4m200 = radardata.configure_x4m200(RadarPort, False, radardata.x4m200_par_settings)
        ser = serial.Serial(MaxPort, 9600, timeout = 1)
        ser.write(str.encode("reset\n"))
        ser.write(str.encode("set_cfg sys_bp 121 119 122\n"))
        ser.write(str.encode("set_cfg bpt dia_bp 91 79 82\n"))
        ser.write(str.encode("read bpt 1\n"))
         """
        
        while True:
            if self._break:
                return
            recv = ["X4M200","RPM","0","State","NO DATA","LD","0","MAX3266BPM","HR","0","C","0","Oxygen Levels","0", "Status","status_Code", "Ext_status", "ext_status", "OxygenRvalue", "96"]
            """ radar_data = radardata.print_x4m200_messages(x4m200).split()
            recv[2] = str(int(float(radar_data[1])))
            recv[6] = str(int(float(radar_data[3])))
            recv[4] = radar_data[5]
            reader = ser.readline().decode("utf-8")
            reader = reader.split(",")
            if len(reader) == 15:
                recv[9] = str(int(float(reader[3])))
                recv[11] = str(int(float(reader[11])))
                recv[13] = str(int(float(reader[7]))) """
                
            recv[2]="12"
            recv[6]="9"
            recv[9]="72"
            recv[13]="98"
            recv[4]="BREATHING"
            #print(radar_data)
            
            
            

            recv=",".join(recv)
            print(recv)
            #print(" ")

            if(len(recv)>5):
                self.change_value.emit(recv)
            else:
                continue
            

    def stopthread(self):
        self._break =True
        self.ser.close()




class HandleScan(QtCore.QThread):

    _gauge1value = QtCore.pyqtSignal(int)
    _gauge2value = QtCore.pyqtSignal(int)
    _gauge3value = QtCore.pyqtSignal(int)
    _gauge4value = QtCore.pyqtSignal(int)


    InstructionssetText = QtCore.pyqtSignal(str)

    graphWidgetclear = QtCore.pyqtSignal(int)

    checktraintrigger = QtCore.pyqtSignal(int)

    #restraintrig = QtCore.pyqtSignal(int)

    debugWindowsetText = QtCore.pyqtSignal(str)

    usermsgsetText = QtCore.pyqtSignal(str)

    graphdata = QtCore.pyqtSignal(list)

    def __init__(self):
        QtCore.QThread.__init__(self)
        self.tempval = 0
        self.FinalReadings = {"temp": 0, "hr": 0, "rpm": 0, "o2levels": 0, "ld": 0}
        self.scanprogress = 0
        self.StartScan = False
        self.scanmode = 0

        self.zerotrigger = False
        self.startldplot =False

        self.flirreading = 0
        self._gauge3value.emit(0)
        self._gauge1value.emit(0)
        self._gauge2value.emit(0)
        self._gauge4value.emit(0)
        self.graphWidgetclear.emit(1)
        self.GraphX = [0]
        self.GraphY = [0]
        self.tempHR = 0
        self.tempRPM = 0
        self.tempval = 0
        self.tempOxyMeterV = 0
        self.startplotting = False

        self.radarstatus = ""

        self._gauge1_normalMaxValue = 0
        self._gauge1_normalMinValue = 0

        self._gauge2_normalMaxValue = 0
        self._gauge2_normalMinValue = 0

        self._gauge3_normalMaxValue = 0
        self._gauge3_normalMinValue = 0

        self._gauge4_normalMaxValue = 0
        self._gauge4_normalMinValue = 0

        self.rpmlist = []
        self.rpmtrig = False
        self.lcflag = 0

        self.StartSerialThread()


    def setGaugeParams(self,g1_nmin, g1_nmax,g2_nmin, g2_nmax,g3_nmin, g3_nmax,g4_nmin, g4_nmax):
        self._gauge1_normalMinValue = g1_nmin
        self._gauge1_normalMaxValue = g1_nmax
        self._gauge2_normalMinValue = g2_nmin
        self._gauge2_normalMaxValue = g2_nmax
        self._gauge3_normalMinValue = g3_nmin
        self._gauge3_normalMaxValue = g3_nmax
        self._gauge4_normalMinValue = g4_nmin
        self._gauge4_normalMaxValue = g4_nmax

    def updatetemp(self, tempval=None):
        if tempval != None:
            self.tempval = tempval

    def updatefaceID(self, faceID=None):
        if faceID !=None:
            self.faceID = faceID

    def startscan(self,startscan,scanmode):
        #self.StartSerialThread()

        self.scanprogress = 0
        self.graphWidgetclear.emit(1)
        self.GraphY = [0]
        self.GraphX = [0]

        """  device_name = '/dev/ttyACM0'
        record = False
        x4m200 = radardata.configure_x4m200(device_name, record, radardata.x4m200_par_settings) """
        
        self.triggraphupdate()
        self.StartScan = startscan
        self.scanmode = scanmode

    def updateserinput(self, ser_HR=None, ser_RPM=None,ser_oxy=None, ser_ld=None):
        if ser_HR != None:
            self.tempHR = ser_HR

        if ser_RPM != None:
            self.tempRPM = ser_RPM

        if ser_oxy != None:
            self.tempOxyMeterV = ser_oxy

        if ser_ld != None:
            tval = int(ser_ld)
            if (tval != 0):
                self.zerotrigger = True
            if self.startldplot:
                if (self.zerotrigger == True):
                    self.GraphY.append(tval)
                    self.GraphX.append(self.GraphX[-1] + 1)


    def StartSerialThread(self):
        self.thread = SerialThread()
        self.thread.change_value.connect(self.setgaugevalues)
        self.thread.start()

    def ResetSerialThread(self):
        self.thread.change_value.disconnect(self.setgaugevalues)
        self.thread.stopthread()
        """ device_name = '/dev/ttyACM0'
        record = False
        x4m200 = radardata.configure_x4m200(device_name, record, radardata.x4m200_par_settings)
         """
        self.thread = SerialThread()
        self.thread.change_value.connect(self.setgaugevalues)
        self.thread.start

    def StopSerialThread(self):
        self.thread.stopthread()

    def setgaugevalues(self,_str):
        if(_str == ""):
            return
        try:
            #self.debugWindowsetText.emit("Debug Info: "+_str)
            if(("X4M200" in _str) and ("MAX3266BPM" in _str)):
                self.debugWindowsetText.emit("Debug Info: " + _str)
                data = _str.split(",")
                #self._gauge1.value = int(data[7])
                #self._gauge2.value = int(data[11])
                #self._gauge3.value = int(data[2])

                self.tempRPM = int(data[2])
                self.tempHR = int(data[9])
                self.tempOxyMeterV = int(data[13])

                self.radarstatus = data[4]

                self.tinst = int(float(data[6]))

                #self.debugWindowsetText.emit("Radar Info: "+self.radarstatus)

                if(self.startplotting):
                    tinst = int(float(data[6]))
                    if tinst!=0:
                        self.zerotrigger = True

                    if self.zerotrigger == True:
                        self.GraphY.append(tinst)
                        self.GraphX.append(self.GraphX[-1] + 1)
                    self.triggraphupdate() #stopped graph plotting for testing

                elif(self.rpmtrig):

                    if(self.tempRPM>5 and len(self.rpmlist)<6):

                       

                        self.rpmlist.append(self.tempRPM)
                        """ if(count(self.rpmlist>5)):
                            self.rpmtrig = False """
                    else: pass


                elif(self.scanprogress == 3):
                    temptemp = self.tempval

                    self.flirreading = max(temptemp, self.flirreading)
                else:
                    pass
                    #time.sleep(0.5)
            else:
                self.tempRPM = self.tempRPM
                self.tempHR = self.tempHR
                self.tempOxyMeterV = self.tempOxyMeterV
        except(IndexError):
            print("Device not a Embedded Bridge")
        except(ValueError):
            print("Value not valid")


    def triggraphupdate(self):
        graph = [self.GraphY,self.GraphX]
        self.graphdata.emit(graph)


    def run(self):
        while True:
            #self.usermsgsetText.emit(str("Maximum Temperature\n" + str(self.tempval)))
            if self.StartScan:
                if self.scanprogress == 0:
                    self.FinalReadings["o2levels"] = 0
                    self.FinalReadings["temp"] = 0
                    self.FinalReadings["rpm"] = 0
                    self.FinalReadings["hr"] = 0
                    self.FinalReadings["ld"] = 0

                    self._gauge3value.emit(0)
                    self._gauge1value.emit(0)
                    self._gauge2value.emit(0)
                    self._gauge4value.emit(0)

                    self.flirreading = 0

                    self.radarstatus = ""



                    self.graphWidgetclear.emit(1)
                    self.GraphX = [0]
                    self.GraphY = [0]
                    self.InstructionssetText.emit("Starting Scan\nPlease Look Into The Screen")
                    time.sleep(2)
                    self.scanprogress = 2

                    #self.restraintrig.emit(1)
                    '''
                    self.fr.face_detection_widget.resMeanFRSession()
                    '''
                    #self.graphWidgetclear.emit(1)
                    self.zerotrigger = False

                    self.localtimer = time.strftime("%X %x")
                    self.dbtime = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    self.timer = time.time()
                    self.temptimer = 0
                    self.hrtimer = 0
                    self.oxytimer = 0
                    self.rpmtimer = 0
                    self.lctimer = 0
                    self.testtimer = 0
                    self.timelog = ""

                    
                    self.meanrpm = 0
                    self.rpmtrig = False


                if self.scanprogress == 2:
                    self.InstructionssetText.emit("Detecting Temperature")
                    time.sleep(1)
                    self.scanprogress = 3

                if self.scanprogress == 3:
                    self.insttemp = self.tempval
                    if self.insttemp == 0:
                        self.InstructionssetText.emit("Error Finding Face\nPlease Look Straight and Retry Again")
                        time.sleep(0.5)
                        return
                    elif (self.insttemp > 10) and (self.FinalReadings["temp"] == 0):
                        self.FinalReadings["temp"] = self.insttemp
                        self.InstructionssetText.emit("Temperature Captured Succesfully  :" + str(self.insttemp) + "\nPlease stand Straight and stay still")
                        self.usermsgsetText.emit("Max Temperature:" + str(self.insttemp))
                        time.sleep(1)
                        self.temptimer = round((time.time() - self.timer),2)
                        self.scanprogress = 7

                if self.scanprogress == 4:
                    self.InstructionssetText.emit("Please Stand Still for RPM capture")
                    time.sleep(1) 
                    self.scanprogress = 5

                if self.scanprogress == 5:
                    self.tempRPM = 0
                    self.GraphX = [0]
                    self.GraphY = [0]
                    self.scanprogress = 6

                if(self.scanprogress == 6):
                    if(self.lcflag==0):
                        
                        self.rpmtrig = True
                    
                        #if(self.tempRPM > 5):
                            #self.FinalReadings["rpm"] = self.tempRPM
                            #self.InstructionssetText.emit("RPM Captured Succesfully")
                        
                        #while True:print(self.rpmlist,self.meanrpm)
                        if(len(self.rpmlist)>=5):
                            
                            self.rpmtrig = False
                            self.meanrpm = sum(self.rpmlist)/len(self.rpmlist)
                            #while True:print(self.rpmlist,self.meanrpm)
                            if(self.meanrpm>2):
                                self.rpmtrig = False

                            self.FinalReadings["rpm"] = self.meanrpm
                            
                            self.rpmtimer = round((time.time() - self.timer),2)
                            #while True:print(self.meanrpm)
                            self._gauge3value.emit(self.meanrpm)
                            
                            self.lcflag=1
                            #while True:print(self.lcflag)
                            self.InstructionssetText.emit("RPM Captured")
                            #time.sleep(1) 
                            #self.scanprogress = 10
                            #self.InstructionssetText.emit("Resetting Graphs")
                            #self.graphWidgetclear.emit(1)
                            
                            time.sleep(0.2)
                        else:
                            #while True: print(self.lcflag)
                            self.InstructionssetText.emit("Movement Detected\nPlease Stand Still")
                            time.sleep(1)
                    if (self.lcflag ==1):
                        self.InstructionssetText.emit("Please Stand Straight and Take 6 Deep Breaths")
                        self.startplotting = True 
                        self.scanprogress = 10
                    #print(self.graphX[-1])
                    
                    


                if(self.scanprogress == 7):
                    self.timerStarted = False
                    self.InstructionssetText.emit("Please Put your Finger on Oximeter")
                    time.sleep(1)
                    self.scanprogress = 8

                if(self.scanprogress == 8):
                    if(self.tempHR>10):
                        self.InstructionssetText.emit("Heart Rate Captured Successfully")
                        self._gauge1value.emit(self.tempHR)
                        self.FinalReadings["hr"] = self.tempHR
                        time.sleep(1)
                        self.hrtimer = round((time.time() - self.timer),2)
                        self.scanprogress = 9
                    else:
                        self.InstructionssetText.emit("Please Wait for HR")
                        time.sleep(1)

                if (self.scanprogress == 9):
                    if (self.tempOxyMeterV > 10):# and (self.FinalReadings["o2levels"] == 0):
                        self.InstructionssetText.emit("Oxygen Levels Captured Successfully")
                        self._gauge2value.emit(self.tempOxyMeterV)
                        self.FinalReadings["o2levels"] = self.tempOxyMeterV
                        self.InstructionssetText.emit("Done\nPlease Lift your Finger off")
                        #self.graphWidgetclear.emit(1)
                        time.sleep(1)
                        self.oxytimer = round((time.time() - self.timer),2)
                        self.scanprogress = 4
                    else:
                        self.InstructionssetText.emit("Please Wait for Oxygen levels")
                        time.sleep(1)

                if(self.scanprogress == 10):
                    
                    """ self.InstructionssetText.emit("Please Stand Straight and Take 6 Deep Breaths")
                    #while True: print(self.tinst)
                    #if self.tinst!=0:
                    #    self.zerotrigger = True

                    #if self.zerotrigger == True:
                    #    self.GraphY.append(self.tinst)
                    #    self.GraphX.append(self.GraphX[-1] + 1)
                    self.startplotting = True 
                    #print(self.graphX[-1])
                    if(self.GraphX[-1]>100):
                        self.startplotting = False """
                    
                    """ self.InstructionssetText.emit("Please Stand Straight and Take 6 Deep Breaths")
                    self.startplotting = True  """

                    if(self.GraphX[-1]>100):
                        self.startplotting = False
                        lc = 0
                        ld = int(abs(max(self.GraphY, key=abs)))
                        #print(self.GraphX[-1],ld,lc)

                        if(self.scanmode == 0):
                            thrval = 7
                        else:
                            thrval = 6
                        if(ld>=thrval):
                            lc = 100
                        elif(ld<thrval):
                            lc = (ld/thrval)*100
                        #if(lc>50): # thresh value for lung capacity
                        self.InstructionssetText.emit("Lung Capacity Captured Successfully")
                        self.lctimer = round((time.time() - self.timer),2)
                        self._gauge4value.emit(int(lc))
                        self.FinalReadings["ld"] = int(lc)
                        time.sleep(1)
                        self.scanprogress = 11
                    else:
                        time.sleep(1)
                    #else:
                    #    self.InstructionssetText.emit("Please Stand Still")
                    #    time.sleep(0.5)


                if (self.scanprogress == 11):

                    """ mydb = mysql.connector.connect(host = "localhost", user = "root", password = "root", database = "user_info")
                    print("1")
                    
                    mycursor = mydb.cursor()
                    print("2")
                    userid = [self.faceID,str("/home/sensor/Desktop/coviduipy/"+self.faceID+"-0.jpg"),self.localtimer, "Positive",self.FinalReadings["temp"],self.FinalReadings["hr"],self.FinalReadings["o2levels"],self.FinalReadings["rpm"],self.FinalReadings["ld"]]
                    print("3")

                    sql = "INSERT INTO positive (id, imgpath, time, result, temp, hr, o2, rpm, ld ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s);"

                    print("4")

                    mycursor.execute(sql, userid)
                    print("5")
                    mydb.commit() """

                    self.thread.quit()
                    self.StartScan = False
                    self.scanprogress = 0
                    self.startplotting = False
                    self.GraphY = [0]
                    self.GraphX = [0]
                    #self.emaildata = {}
                    #self.emaildata["emailo2"] = str(self.FinalReadings["o2levels"])
                    #self.emaildata["emailtemp"] = str(self.FinalReadings["temp"])
                    #self.emaildata["emailrpm"] = str(self.FinalReadings["rpm"])
                    #self.emaildata["emailld"] = str(self.FinalReadings["ld"])
                    #self.emaildata["emailhr"] = str(self.FinalReadings["hr"])
                    

                    status = 1
                    if(self.FinalReadings["o2levels"]>self._gauge2_normalMaxValue) or (self.FinalReadings["o2levels"]<self._gauge2_normalMinValue):
                        status = 0
                        #self.emaildata["emailo2"] = "<p style=\"color=red\">"+strself.emaildata["emailo2"]+"</p>"
                    if(self.FinalReadings["temp"]>99) or (self.FinalReadings["temp"]<90):
                        status = 0
                        #self.emaildata["emailtemp"] = "<p style=\"color=red\">"+self.emaildata["emailtemp"]+"</p>"
                    if(self.FinalReadings["rpm"]>self._gauge3_normalMaxValue) or (self.FinalReadings["rpm"]<self._gauge3_normalMinValue):
                        status = 0
                        #self.emaildata["emailrpm"] = "<p style=\"color=red\">"+self.emaildata["emailrpm"]+"</p>"
                    if (self.FinalReadings["ld"] > self._gauge4_normalMaxValue) or (self.FinalReadings["ld"] < self._gauge4_normalMinValue):
                        status = 0
                        #self.emaildata["emailld"] = "<p style=\"color=red\">"+self.emaildata["emailld"]+"</p>"
                    if (self.FinalReadings["hr"] > self._gauge1_normalMaxValue) or (
                            self.FinalReadings["hr"] < self._gauge1_normalMinValue):
                        status = 0
                        #self.emaildata["emailhr"] = "<p style=\"color=red\">"+self.emaildata["emailhr"]+"</p>"
                    self.InstructionssetText.emit("Scan Completed")
                    time.sleep(1)
                    
                    
                   
                    
                    if(status==0):
                        self.InstructionssetText.emit("Test Positive\nSTOP")
                        #self.InstructionssetText.emit("User Identified as :",self.faceID)
                        #time.sleep(2)
                        self.result = "Positive"
                        self.checktraintrigger.emit(1)

                    elif status == 1:
                        self.InstructionssetText.emit("Test Negative\nGo")
                        self.result = "Negative"

                    self.testtimer = round((time.time() - self.timer),2)
                    
                    self.timelog = [self.dbtime,self.temptimer,self.FinalReadings["temp"],self.hrtimer,self.FinalReadings["hr"],self.oxytimer,self.FinalReadings["o2levels"],self.rpmtimer,self.FinalReadings["rpm"],self.lctimer,self.FinalReadings["ld"],self.testtimer]
                   

                    with open("/home/sensor/Desktop/coviduipy/log.csv","a+",newline = "") as file:
                        writer = csv.writer(file)
                        writer.writerow(self.timelog)

                    mydb = mysql.connector.connect(host = "localhost", user = "root", password = "root", database = "user_info")
                   
                    
                    mycursor = mydb.cursor()
                
                    
                    
                    #timelog = [userid,imgpath,testtimer, FinalResult,FinalReadings["temp"],FinalReadings["hr"],FinalReadings["o2levels"],FinalReadings["rpm"],FinalReadings["ld"]]
                    userid = [int(self.faceID),"/home/sensor/Desktop/coviduipy/Face_Gallery/"+self.faceID+"-0.jpg",self.dbtime, self.result,int(self.FinalReadings["temp"]),int(self.FinalReadings["hr"]),int(self.FinalReadings["o2levels"]),int(self.FinalReadings["rpm"]),int(self.FinalReadings["ld"])]
                    
                    sql = "INSERT INTO positive (id, imgpath, time, result, temp, hr, o2, rpm, ld ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s);"
                    
                    mycursor.execute("SELECT count(id) from positive WHERE id=%s;",(self.faceID,))
                    userstatus = mycursor.fetchall()

                    #while True: print(userstatus)

                    if self.result=="Positive" or userstatus[0][0]!=0:
                        mycursor.execute(sql, userid)
                        mydb.commit()
                    #while True: print(sql)

                    


                    mycursor.execute("SELECT * FROM positive where id IN (SELECT id FROM positive group by ID having count(id)>2);")


                    res_data = mycursor.fetchall()

                    
                    


                    if res_data!=[]:

                        res_vals = {}
                        res_vals["temp"]=[]
                        res_vals["o2"]=[]
                        res_vals["hr"]=[]
                        res_vals["ld"]=[]
                        res_vals["rpm"]=[]

                        
                        
                            
                        for i in range(0,3):
                            if (res_data[i][6] > self._gauge2_normalMaxValue) or (res_data[i][6] < self._gauge2_normalMinValue):
                                #o2str="""<p style="color=red !important;">"""+str(res_data[i][6])+"</p>"
                                o2str="\""+str(res_data[i][6])+"\""
                            else:
                                o2str=str(res_data[i][6])
                            res_vals["o2"].append(o2str)
                            #res_data[i][6] = "<p style=\"color=red\">"+str(res_data[i][6])+"</p>"
                            if (res_data[i][4] > 99) or (res_data[i][4] < 90):
                                tempstr="\""+str(res_data[i][4])+"\""
                                #tempstr="""<p style="color=red !important;">"""+str(res_data[i][4])+"</p>"
                            else:
                                tempstr=str(res_data[i][4])
                            res_vals["temp"].append(tempstr)
                            #res_data[i][4] = "<p style=\"color=red\">"+str(res_data[i][4])+"</p>"
                            if (res_data[i][7] > self._gauge3_normalMaxValue) or (res_data[i][7] < self._gauge3_normalMinValue):
                                #rpmstr="""<p style="color=red !important;">"""+str(res_data[i][7])+"</p>"
                                rpmstr="\""+str(res_data[i][7])+"\""
                            else:
                                rpmstr=str(res_data[i][7])
                            res_vals["rpm"].append(rpmstr)
                            #res_data[i][7] = "<p style=\"color=red\">"+str(res_data[i][7])+"</p>"
                            
                            if (res_data[i][8] > self._gauge4_normalMaxValue) or (res_data[i][8] < self._gauge4_normalMinValue):
                                #ldstr="""<p style="color=red !important;">"""+str(res_data[i][8])+"</p>"
                                ldstr="\""+str(res_data[i][8])+"\""
                            else:
                                ldstr=str(res_data[i][8])
                            res_vals["ld"].append(ldstr)
                            #res_data[i][8] = "<p style=\"color=red\">"+str(res_data[i][8])+"</p>"
                            if (res_data[i][5] > self._gauge1_normalMaxValue) or (res_data[i][5] < self._gauge1_normalMinValue):
                                hrstr="\""+str(res_data[i][5])+"\""
                                #hrstr="""<p style="color=red !important;">"""+str(res_data[i][5])+"</p>"
                            else:
                                hrstr=str(res_data[i][5])
                            res_vals["hr"].append(hrstr)
                            #res_data[i][5] = "<p style=\"color=red\">"+str(res_data[i][5])+"</p>"

                       

                       
                        sender_email = "coviduipy@gmail.com"
                        receiver_email = "keithscheffler@me.com"
                        receiver_email2 = "jayvikram001@gmail.com"
                        receiver_email3 = "aayushrawal98@gmail.com"
                        password = "sensor1!" #input("Type your password and press enter:")

                        message = MIMEMultipart("alternative")
                        message["Subject"] = "Test Report"
                        message["From"] = sender_email
                        message["To"] = receiver_email

                        # Create the plain-text and HTML version of your message

                        html = """\
                        <!DOCTYPE html>
                        <html>
                            <head>
                            <meta charset="utf-8">
                            <meta name="viewport" content="width=device-width, initial-scale=1.0">
                            <title>One column layout</title>
                            <style>
                                html,body,table,tbody,tr,td,div,p,ul,ol,li,h1,h2,h3,h4,h5,h6 
                                {{
                                margin: 0;
                                padding: 0;
                                }}
                                
                                body {{
                                margin: 0;
                                padding: 0;
                                font-size: 0;
                                line-height: 0;
                                -ms-text-size-adjust: 100%;
                                -webkit-text-size-adjust: 100%;
                                }}
                                
                                table {{
                                border-spacing: 0;
                                mso-table-lspace: 0pt;
                                mso-table-rspace: 0pt;
                                }}
                                
                                table td {{
                                border-collapse: collapse;
                                }}
                                
                                .ExternalClass {{
                                width: 100%;
                                }}
                                
                                .ExternalClass,
                                .ExternalClass p,
                                .ExternalClass span,
                                .ExternalClass font,
                                .ExternalClass td,
                                .ExternalClass div {{
                                line-height: 100%;
                                }}
                                /* Outermost container in Outlook.com */
                                
                                .ReadMsgBody {{
                                width: 100%;
                                }}
                                
                                img {{
                                -ms-interpolation-mode: bicubic;
                                }}
                            </style>
                            <style>
                                .container600 {{
                                width: 600px;
                                max-width: 100%;
                                }}
                                
                                @media all and (max-width: 600px) {{
                                .container600 {{
                                    width: 100% !important;
                                }}
                                }}
                                
                                @media all and (max-width: 599px) {{

                                .container600 {{
                                    width: 100% !important;
                                }}

                                .smarttable {{
                                    border: 0;
                                    
                                    
                                }}
                                .smarttable thead {{
                                            
                                    max-height:0px;
                                }}
                                .smarttable tr {{
                                    display: block;
                                    width:90%;
                                    margin:20px auto;

                                    margin-bottom: 10px !important;
                                }}
                                .smarttable td {{
                                    border-bottom: 1px solid #ddd;
                                    display: block;
                                    font-size: 15px;
                                    text-align: right;
                                    background: #fdfdfd;
                                }}
                                .smarttable td img {{
                                    border-bottom: 1px solid #ddd;
                                    display: inline-block;
                                    font-size: 15px;
                                    text-align: right;
                                }}
                                .smarttable td:before {{
                                    content: attr(data-label);
                                    float: left;self.emaildata["emailtemp"]
                                    font-weight: bold;
                                    text-transform: uppercase;
                                }}

                                }}
                            </style>

                            <!--[if gte mso 9]>
                                <style>
                                    .ol {{
                                        width: 100%;
                                    }}
                                </style>
                            <![endif]-->
                            </head>
                            <body style="background-color: #f4f4f4;">
                            <center>

                                <!--[if gte mso 9]><table width="600" cellpadding="0" cellspacing="0"><tr><td>
                                            <![endif]-->
                                <table class="container600" cellpadding="0" cellspacing="0" border="0" width="100%" style="width:calc(100%);max-width:calc(800px);margin: 0 auto;">
                                <tr>
                                    <td width="100%" style="text-align: left;">
                                    <table width="100%" cellpadding="0" cellspacing="0" border="0" style="min-width:100%;">
                                        <tr>
                                        <td width="100%" style="min-width:100%;background-color:#ffffff;padding:30px;">
                                            <h1 style="font-family:Arial;font-size:28px;line-height:32px;">Test Report</h1>
                                        </td>
                                        </tr>
                                    </table>
                                    <table width="100%" cellpadding="0" cellspacing="0" border="0" style="min-width:100%;">
                                        <tr>
                                        <td style="background-color:#F8F7F0;padding:20px;">

                                            <table class="smarttable" width="100%" cellpadding="0" cellspacing="0" style="min-width:100%;">
                                                <thead>
                                                    <tr>
                                                    <th scope="col" style="padding:5px; font-family: Arial,sans-serif; font-size: 16px; line-height:20px;line-height:30px"> Vitals</th>
                                                    <th scope="col" style="padding:5px; font-family: Arial,sans-serif; font-size: 16px; line-height:20px;line-height:30px">Scan 1</th>
                                                    <th scope="col" style="padding:5px; font-family: Arial,sans-serif; font-size: 16px; line-height:20px;line-height:30px">Scan 2</th>
                                                    <th scope="col" style="padding:5px; font-family: Arial,sans-serif; font-size: 16px; line-height:20px;line-height:30px">Scan 3</th>
                                                    </tr>
                                                </thead>
                                                <tbody>
                                                    <tr>
                                                    <th data-label="Name" valign="top" style="padding:5px; font-family: Arial,sans-serif; font-size: 16px; line-height:20px;">Thermal Temperature</th>
                                                    <td data-label="Scan 1" valign="top" style="padding:5px; font-family: Arial,sans-serif; font-size: 16px; line-height:20px;">{}</td>
                                                    <td data-label="Scan 2" valign="top" style="padding:5px; font-family: Arial,sans-serif; font-size: 16px; line-height:20px;">{}</td>
                                                    <td data-label="Scan 3" valign="top" style="padding:5px; font-family: Arial,sans-serif; font-size: 16px; line-height:20px;">{}</td>
                                                    
                                                    </tr>
                                                    <tr>
                                                    <th data-label="Name" valign="top" style="padding:5px; font-family: Arial,sans-serif; font-size: 16px; line-height:20px;">Heart Rate</th>
                                                    <td data-label="Scan 1" valign="top" style="padding:5px; font-family: Arial,sans-serif; font-size: 16px; line-height:20px;">{}</td>
                                                    <td data-label="Scan 2" valign="top" style="padding:5px; font-family: Arial,sans-serif; font-size: 16px; line-height:20px;">{}</td>
                                                    <td data-label="Scan 3" valign="top" style="padding:5px; font-family: Arial,sans-serif; font-size: 16px; line-height:20px;">{}</td>
                                                    </tr>
                                                    <tr>
                                                    <th data-label="Name" valign="top" style="padding:5px; font-family: Arial,sans-serif; font-size: 16px; line-height:20px;">Blood Oxygen</th>
                                                    <td data-label="Scan 1" valign="top" style="padding:5px; font-family: Arial,sans-serif; font-size: 16px; line-height:20px;">{}</td>
                                                    <td data-label="Scan 2" valign="top" style="padding:5px; font-family: Arial,sans-serif; font-size: 16px; line-height:20px;">{}</td>
                                                    <td data-label="Scan 3" valign="top" style="padding:5px; font-family: Arial,sans-serif; font-size: 16px; line-height:20px;">{}</td>
                                                    </tr>
                                                    <tr>
                                                    <th data-label="Name" valign="top" style="padding:5px; font-family: Arial,sans-serif; font-size: 16px; line-height:20px;">Breath Per Minute</th>
                                                    <td data-label="Scan 1" valign="top" style="padding:5px; font-family: Arial,sans-serif; font-size: 16px; line-height:20px;">{}</td>
                                                    <td data-label="Scan 2" valign="top" style="padding:5px; font-family: Arial,sans-serif; font-size: 16px; line-height:20px;">{}</td>
                                                    <td data-label="Scan 3" valign="top" style="padding:5px; font-family: Arial,sans-serif; font-size: 16px; line-height:20px;">{}</td>
                                                    </tr>
                                                    <tr>
                                                    <th data-label="Name" valign="top" style="padding:5px; font-family: Arial,sans-serif; font-size: 16px; line-height:20px;">Lung Capacity</th>
                                                    <td data-label="Scan 1" valign="top" style="padding:5px; font-family: Arial,sans-serif; font-size: 16px; line-height:20px;">{}</td>
                                                    <td data-label="Scan 2" valign="top" style="padding:5px; font-family: Arial,sans-serif; font-size: 16px; line-height:20px;">{}</td>
                                                    <td data-label="Scan 3" valign="top" style="padding:5px; font-family: Arial,sans-serif; font-size: 16px; line-height:20px;">{}</td>
                                                    </tr>
                                                    <tr>
                                                    <th data-label="Name" valign="top" style="padding:5px; font-family: Arial,sans-serif; font-size: 16px; line-height:20px;">Test Result</th>
                                                    <td data-label="Scan 1" valign="top" style="padding:5px; font-family: Arial,sans-serif; font-size: 16px; line-height:20px;">{}</td>
                                                    <td data-label="Scan 2" valign="top" style="padding:5px; font-family: Arial,sans-serif; font-size: 16px; line-height:20px;">{}</td>
                                                    <td data-label="Scan 3" valign="top" style="padding:5px; font-family: Arial,sans-serif; font-size: 16px; line-height:20px;">{}</td>
                                                    </tr>
                                                </tbody>                         
                                            </table>
                                        </td>
                                        </tr>
                                    </table>

                                    <table width="100%" cellpadding="0" cellspacing="0" style="min-width:100%;">
                                        <tr>
                                        <td style="background-color:#FFFFFF;padding:20px;">
                                            <table class="smarttable" width="100%" cellpadding="0" cellspacing="0" style="min-width:100%;">
                                                <thead>
                                                <tr>
                                                <td data-label="Note" valign="top" style="padding:5px; font-family: Arial,sans-serif; font-size: 12px; line-height:20px;">Please note values denoted with " " are not normal.</td>
                                                </tr>
                                            
                                                
                                                </thead>
                                                
                                           
                                                
                                                <tbody>
                                                
                                                <tr>
                                                <td valign="top" style="padding:5px; font-family: Arial,sans-serif; font-size: 16px; line-height:20px;">User Image:</td>
                                                </tr>

                                                <tr>
                                                

                                                    <td data-label="User Image" valign="top" style="padding:5px; font-family: Arial,sans-serif; font-size: 16px; line-height:20px;">
                                                    <img alt="" src="cid:image1"  style="display: inline-block; width: 100px;" />
                                                    </td>
                                                </tr>

                                                <tr>
                                                <td data-label="User ID" valign="top" style="padding:5px; font-family: Arial,sans-serif; font-size: 16px; line-height:20px;">User ID: {}</td>
                                                </tr>
                                                <tr>
                                                <td data-label="Timer" valign="top" style="padding:5px; font-family: Arial,sans-serif; font-size: 16px; line-height:20px;">Test Time: {}</td>
                                                </tr>
                                                
                                            
                                                </tbody>
                                            </table>
                                        </td>
                                        </tr>
                                    </table>
                                    
                                    
                                    </td>
                                </tr>
                                </table>

                                <!--[if gte mso 9]></td></tr></table>
                                            <![endif]-->
                            </center>
                            </body>
                        </html>
                        """.format(res_vals["temp"][0],res_vals["temp"][1],res_vals["temp"][2],res_vals["hr"][0],res_vals["hr"][1],res_vals["hr"][2],res_vals["o2"][0],res_vals["o2"][1],res_vals["o2"][2],res_vals["rpm"][0],res_vals["rpm"][1],res_vals["rpm"][2],res_vals["ld"][0],res_vals["ld"][1],res_vals["ld"][2],res_data[0][3],res_data[1][3],res_data[2][3],res_data[0][0],res_data[0][2].strftime('%Y-%m-%d %H:%M:%S'))

                        #
                        #format(res_data[0][4],res_data[1][4],res_data[2][4],res_data[0][5],res_data[1][5],res_data[2][5],res_data[0][6],res_data[1][6],res_data[2][6],res_data[0][7],res_data[1][7],res_data[2][7],res_data[0][8],res_data[1][8],res_data[2][8],res_data[0][3],res_data[1][3],res_data[2][3],res_data[0][0],res_data[0][2].strftime('%Y-%m-%d %H:%M:%S'))

                        # Turn these into plain/html MIMEText objects
                        part1 = MIMEText(html, "html")


                        # Add HTML/plain-text parts to MIMEMultipart message
                        # The email client will try to render the last part first
                        message.attach(part1)

                        imgfile = res_data[0][1]

                        #fp=open(imgfile,"rb")
                        fp=open(imgfile,"rb")
                        emailimage = MIMEImage(fp.read())
                        fp.close()

                        emailimage.add_header('Content-ID','<image1>')
                        message.attach(emailimage)

                        # Create secure connection with server and send email
                        context = ssl.create_default_context()
                        with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
                            server.login(sender_email, password)
                            server.sendmail(
                                sender_email, receiver_email, message.as_string()
                            )
                        
                        with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
                            server.login(sender_email, password)
                            server.sendmail(
                                sender_email, receiver_email2, message.as_string()
                            )
                        
                        with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
                            server.login(sender_email, password)
                            server.sendmail(
                                sender_email, receiver_email3, message.as_string()
                            )



                        self.InstructionssetText.emit("Email Sent")

                        sql = "DELETE FROM positive WHERE id={}".format(res_data[0][0])

                        mycursor.execute(sql)

                        mydb.commit()
                     

                    self.FinalReadings["o2levels"] = 0
                    self.FinalReadings["temp"] = 0
                    self.FinalReadings["rpm"] = 0
                    self.FinalReadings["hr"] = 0
                    self.FinalReadings["ld"] = 0

                    self.flirreading = 0
                    self.GraphX = [0]
                    self.GraphY = [0]

                    
            else:
                time.sleep(0.5)
                continue


class MainWindow(QWidget):

    user_name = QtCore.pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):

        dialwidth = self.geometry().width()*0.04
        LabelFont = QtGui.QFont('Arial',14)
        self.dividerRatio = 0.3


        self.Platform = 2
        self.gtv = 0
        self.gtvp = 2

        self._gauge1 = RadialBar(self)
        self._gauge1.foregroundColor = QtGui.QColor("#181c24")
        self._gauge1.dialWidth = dialwidth
        self._gauge1.startAngle = 90
        self._gauge1.spanAngle = 180
        self._gauge1.textColor = QtGui.QColor("#FFFFFF")
        self._gauge1.penStyle = QtCore.Qt.RoundCap
        self._gauge1.dialType = RadialBar.DialType.MinToMax
        self._gauge1.suffixText = ""
        self._gauge1.maxValue = 200
        self._gauge1.minValue = 0
        self._gauge1.value = 0
        self.myfont = QtGui.QFont()
        #self._gauge1.textFont = self.myfont
        self._gauge1._normalMinValue = 70
        self._gauge1._normalMaxValue = 120

        self._gauge2 = RadialBar(self)
        self._gauge2.foregroundColor = QtGui.QColor("#181c24")
        self._gauge2.dialWidth = dialwidth
        self._gauge2.startAngle = 90
        self._gauge2.spanAngle = 180
        self._gauge2.textColor = QtGui.QColor("#FFFFFF")
        self._gauge2.penStyle = QtCore.Qt.RoundCap
        self._gauge2.dialType = RadialBar.DialType.MinToMax
        self._gauge2.suffixText = ""
        self._gauge2.maxValue = 100
        self._gauge2.minValue = 0
        self._gauge2.value = 0
        self._gauge2._normalMinValue = 90
        self._gauge2._normalMaxValue = 100
        #self._gauge2.textFont = self.myfont

        self._gauge3 = RadialBar(self)
        self._gauge3.foregroundColor = QtGui.QColor("#181c24")
        self._gauge3.dialWidth = dialwidth
        self._gauge3.startAngle = 90
        self._gauge3.spanAngle = 180
        self._gauge3.textColor = QtGui.QColor("#FFFFFF")
        self._gauge3.penStyle = QtCore.Qt.RoundCap
        self._gauge3.dialType = RadialBar.DialType.MinToMax
        self._gauge3.suffixText = ""
        self._gauge3.maxValue = 40
        self._gauge3.minValue = 5
        self._gauge3.value = 0
        self._gauge3._normalMinValue = 11
        self._gauge3._normalMaxValue = 18
        #self._gauge3.textFont = self.myfont

        self._gauge4 = RadialBar(self)
        self._gauge4.foregroundColor = QtGui.QColor("#181c24")
        self._gauge4.dialWidth = dialwidth
        self._gauge4.startAngle = 90
        self._gauge4.spanAngle = 180
        self._gauge4.textColor = QtGui.QColor("#FFFFFF")
        self._gauge4.penStyle = QtCore.Qt.RoundCap
        self._gauge4.dialType = RadialBar.DialType.MinToMax
        self._gauge4.suffixText = ""
        self._gauge4.maxValue = 100
        self._gauge4.minValue = 0
        self._gauge4.value = 0
        self._gauge4._normalMinValue = 80
        self._gauge4._normalMaxValue = 100
        #self._gauge4.textFont = self.myfont

        self.vbox = QVBoxLayout()
        self.vbox.setContentsMargins(self.geometry().height()*0.087, 10, 10, 10) # Centers Gauges

        self.LabelHeading = QtWidgets.QLabel("Sensor Data")
        self.label1 = QtWidgets.QLabel("Heart Rate")
        self.label2 = QtWidgets.QLabel("Blood Oxygen")
        self.label3 = QtWidgets.QLabel("Breath per Minute")
        self.label4 = QtWidgets.QLabel("Lung Capacity")

        self.label1.setFont(LabelFont)
        self.label2.setFont(LabelFont)
        self.label3.setFont(LabelFont)
        self.label4.setFont(LabelFont)
        self.LabelHeading.setFont(LabelFont)


        self.label1.setStyleSheet("color: white; padding-bottom:10px; text-align: center;")
        self.label2.setStyleSheet("color: white; padding-bottom:10px; text-align: center;")
        self.label3.setStyleSheet("color: white; padding-bottom:10px; text-align: center;")
        self.label4.setStyleSheet("color: white; padding-bottom:10px; text-align: center;")
        self.LabelHeading.setStyleSheet("color: white; padding-bottom:10px; text-align: center;")

        self.label1.setAlignment(QtCore.Qt.AlignCenter)
        self.label2.setAlignment(QtCore.Qt.AlignCenter)
        self.label3.setAlignment(QtCore.Qt.AlignCenter)
        self.label4.setAlignment(QtCore.Qt.AlignCenter)
        self.LabelHeading.setAlignment(QtCore.Qt.AlignCenter)



        #label1.setContentsMargins(self.geometry().height() * 0.11 -(self.geometry().width() *0.005 ), 10, 10, 10)
        #label1.setAlignment(QtCore.Qt.AlignCenter)

        self.vbox.addWidget(self.LabelHeading)
        self.vbox.addSpacing(45)
        self.vbox.addWidget(self.label1)
        self.vbox.addWidget(self._gauge1,1)
        self.vbox.addStretch()
        self.vbox.addWidget(self.label2)
        self.vbox.addWidget(self._gauge2, 1)
        self.vbox.addStretch()
        self.vbox.addWidget(self.label3)
        self.vbox.addWidget(self._gauge3, 1)
        self.vbox.addStretch()
        self.vbox.addWidget(self.label4)
        self.vbox.addWidget(self._gauge4, 1)
        self.vbox.addStretch()
        self.vrect = QtCore.QRect(0, 0, (self.geometry().height() * self.dividerRatio), self.geometry().height())
        self.vbox.setGeometry(self.vrect)

        self.GraphicsWindow = QVBoxLayout()
        #GraphicsWindow.addStretch()
        #vrectGW = QtCore.QRect((self.geometry().width()*0.3), 0, (self.geometry().width()*1.5), self.geometry().height())
        #GraphicsWindow.setGeometry(vrectGW);


        self.debugWindow = QtWidgets.QLabel()
        self.debugWindow.setSizePolicy(
            QtWidgets.QSizePolicy.Maximum,
            QtWidgets.QSizePolicy.Fixed
        )
        #debugWindow.setSizePolicy(QtWidgets.QSizePolicy.Expanding,QtWidgets.QSizePolicy.Fixed)
        self.debugWindow.setStyleSheet("background-color: white; padding: 4px; qproperty-alignment: AlignRight; margin-left:50%;")
        self.debugWindow.setText("Debug Window")
        self._debugWindow = QtWidgets.QHBoxLayout()
        self._debugWindow.addSpacerItem(QtWidgets.QSpacerItem(250,10,QtWidgets.QSizePolicy.Expanding))
        self._debugWindow.addWidget(self.debugWindow)


        """ script_dir = path.dirname(path.realpath(__file__))
        cascade_filepath = path.join(script_dir, '/home/sensor/Desktop/coviduipy/haarcascade_frontalface_default.xml')
        cascade_filepath = path.abspath(cascade_filepath) """

        self.div = 350

            
        self.fd = FDWidget(scale=(self.geometry().height()/self.div), feed="/dev/video0")
        #self.fr = FRWidget(scale=(self.geometry().height()/self.div), feed="/dev/video3")
        self.fr = FRWidget()
        #print(self.fr.face_detection_widget.text)

        self.usermsg = QtWidgets.QLabel()
        self.usermsg.setText("Max Temperature: 0")
        self.usermsg.setFont(self.myfont)
        self.usermsg.setAlignment(QtCore.Qt.AlignCenter)
        self.usermsg.setStyleSheet("color: white; padding-bottom:10px; text-align: center;")

        self.Instructions = QtWidgets.QLabel()
        self.Instructions.setText("Ready")
        self.Instructions.setFont(self.myfont)
        self.Instructions.setAlignment(QtCore.Qt.AlignCenter)
        self.Instructions.setStyleSheet("color: orange; padding-bottom:10px; text-align: center;")

        self.fr_id = QtWidgets.QLabel()
        #self.fr_id.setText("Last Record Sno: None")
        self.fr_id.setText("")
        self.fr_id.setFont(self.myfont)
        self.fr_id.setAlignment(QtCore.Qt.AlignCenter)
        self.fr_id.setStyleSheet("color: orange; padding-bottom:10px; text-align: center;")


        self.messagepanellayout = QVBoxLayout()
        self.messagepanellayout.addSpacerItem(QtWidgets.QSpacerItem(250,100,QtWidgets.QSizePolicy.Expanding))
        self.messagepanellayout.addWidget(self.Instructions)
        self.messagepanellayout.addSpacerItem(QtWidgets.QSpacerItem(250, 100, QtWidgets.QSizePolicy.Expanding))
        self.messagepanellayout.addWidget(self.usermsg)
        self.messagepanellayout.addSpacerItem(QtWidgets.QSpacerItem(250, 100, QtWidgets.QSizePolicy.Expanding))
        self.messagepanellayout.addWidget(self.fr_id)
        self.messagepanellayout.addSpacerItem(QtWidgets.QSpacerItem(250, 100, QtWidgets.QSizePolicy.Expanding))

        

        self.CVPanel = QHBoxLayout()
        self.CVPanel.addSpacerItem(QtWidgets.QSpacerItem(220, 10, QtWidgets.QSizePolicy.Maximum))
        self.CVPanel.addWidget(self.fd.face_detection_widget)
        self.CVPanel.addSpacerItem(QtWidgets.QSpacerItem(45,100,QtWidgets.QSizePolicy.MinimumExpanding))
        self.CVPanel.addLayout(self.messagepanellayout)
        self.CVPanel.addSpacerItem(QtWidgets.QSpacerItem(25, 10, QtWidgets.QSizePolicy.Expanding))


        self.CVPanelHeading = QHBoxLayout()
        self.H1 = QtWidgets.QLabel()
        self.H1.setText("Thermal Feed")
        self.H1.setStyleSheet("color: white; padding-bottom:10px; text-align: center;")
        self.H2 = QtWidgets.QLabel()
        self.H2.setText("Info Panel")
        self.H2.setStyleSheet("color: white; padding-bottom:10px; text-align: center;")
        self.CVPanelHeading.addSpacerItem(QtWidgets.QSpacerItem(70, 10, QtWidgets.QSizePolicy.Maximum))
        self.CVPanelHeading.addWidget(self.H1)
        self.CVPanelHeading.addSpacerItem(QtWidgets.QSpacerItem(250, 10, QtWidgets.QSizePolicy.Expanding))
        self.CVPanelHeading.addWidget(self.H2)
        self.CVPanelHeading.addSpacerItem(QtWidgets.QSpacerItem(250, 10, QtWidgets.QSizePolicy.Expanding))

        self.InfoPanelLabels = QHBoxLayout()
        self.i1 = QtWidgets.QLabel()
        self.i1.setText("Face Recognition")
        self.i1.setStyleSheet("color: white; padding-bottom:10px; text-align: center;")
        self.i2 = QtWidgets.QLabel()
        self.i2.setText("Lungs Displacement")
        self.i2.setStyleSheet("color: white; padding-bottom:10px; text-align: center;")
        self.InfoPanelLabels.addSpacerItem(QtWidgets.QSpacerItem(70, 10, QtWidgets.QSizePolicy.Maximum))
        self.InfoPanelLabels.addWidget(self.i1)
        self.InfoPanelLabels.addSpacerItem(QtWidgets.QSpacerItem(250, 10, QtWidgets.QSizePolicy.Expanding))
        self.InfoPanelLabels.addWidget(self.i2)
        self.InfoPanelLabels.addSpacerItem(QtWidgets.QSpacerItem(250, 10, QtWidgets.QSizePolicy.Expanding))

        self.InfoPanel = QHBoxLayout()
        self.graphWidget = pg.PlotWidget()
        self.GraphY = [0,0]
        self.GraphX = [0,0]
        self.graphWidget.setYRange(-10, 10, padding=0)
        self.graphWidget.setXRange(0, 100, padding=0)

        self.GraphBorder = QtWidgets.QVBoxLayout()
        self.GraphBorder.addWidget(self.graphWidget)

        self.InfoPanel.addSpacerItem(QtWidgets.QSpacerItem(70, 10, QtWidgets.QSizePolicy.Maximum))
        self.InfoPanel.addWidget(self.fr)
        self.InfoPanel.addSpacerItem(QtWidgets.QSpacerItem(25, 10, QtWidgets.QSizePolicy.Expanding))
        self.InfoPanel.addLayout(self.GraphBorder)
        self.InfoPanel.addSpacerItem(QtWidgets.QSpacerItem(25, 10, QtWidgets.QSizePolicy.Expanding))
        #InfoPanel.setAlignment(QtCore.Qt.AlignRight)

        self.startscanM = QtWidgets.QPushButton("Start Scan - Male")
        self.startscanF = QtWidgets.QPushButton("Start Scan - Female")
        self.startscanM.clicked.connect(self.RunScanM)
        self.startscanF.clicked.connect(self.RunScanF)
        self.controls = QtWidgets.QHBoxLayout()
        self.controls.addSpacerItem(QtWidgets.QSpacerItem(25, 10, QtWidgets.QSizePolicy.Expanding))
        self.controls.addWidget(self.startscanM)
        self.controls.addSpacerItem(QtWidgets.QSpacerItem(25, 10, QtWidgets.QSizePolicy.Expanding))
        self.controls.addWidget(self.startscanF)
        self.controls.addSpacerItem(QtWidgets.QSpacerItem(25, 10, QtWidgets.QSizePolicy.Expanding))

        self.GraphicsWindow.addLayout(self.CVPanelHeading)
        self.GraphicsWindow.addLayout(self.CVPanel)
        self.GraphicsWindow.addSpacerItem(QtWidgets.QSpacerItem(250, 40, QtWidgets.QSizePolicy.Maximum))
        self.GraphicsWindow.addLayout(self.InfoPanelLabels)
        self.GraphicsWindow.addSpacerItem(QtWidgets.QSpacerItem(250,60, QtWidgets.QSizePolicy.Minimum))
        self.GraphicsWindow.addLayout(self.InfoPanel)
        self.GraphicsWindow.addSpacerItem(QtWidgets.QSpacerItem(250, 40, QtWidgets.QSizePolicy.Maximum))
        self.GraphicsWindow.addLayout(self.controls)
        self.GraphicsWindow.addStretch()
        self.GraphicsWindow.addLayout(self._debugWindow)

        self._gauge1.value = self.gtv
        self._gauge2.value = self.gtv
        self._gauge3.value = self.gtv
        self._gauge4.value = self.gtv


        self.hbox = QHBoxLayout()
        self.hbox.setContentsMargins(self.geometry().height() * 0.1, 10, 10, 10)
        self.hbox.addLayout(self.vbox)
        self.hbox.addStretch()
        self.hbox.addLayout(self.GraphicsWindow)


        self.setLayout(self.hbox)


        #painter = QtGui.QPainter(self)

        #brush = QtGui.QBrush()

        self.setMinimumSize(900,600)
        self.showMaximized()
        self.setWindowTitle('Dashboard')

        self.scanthread = HandleScan()
        self.scanthread.setGaugeParams(self._gauge1._normalMinValue, self._gauge1._normalMaxValue,
                                       self._gauge2._normalMinValue, self._gauge2._normalMaxValue,
                                       self._gauge3._normalMinValue, self._gauge3._normalMaxValue,
                                       self._gauge4._normalMinValue, self._gauge4._normalMaxValue)

        self.show()


    def gomessage(self):
        self.Instructions.setStyleSheet("color: green; padding-bottom:10px; text-align: center;")
        self.setmsg("Test Negative\nGo")

    def stopmessage(self):
        self.Instructions.setStyleSheet("color: red; padding-bottom:10px; text-align: center;")
        self.setmsg("Test Positive\nStop")

    def setmsg(self,str):
        self.Instructions.setText(str)

    def setdebugwin(self,str):
        self.debugWindow.setText(str)

    def RunScanM(self):
        self.scanthread.start()
        self.connectscansignals()
        self.scanthread.startscan(True, 0)

    def RunScanF(self):
        self.scanthread.start()
        self.connectscansignals()
        self.scanthread.startscan(True, 1)


    def setgauge1val(self,val):
        self._gauge1.value = val

    def setgauge2val(self,val):
        self._gauge2.value = val

    def setgauge3val(self,val):
        self._gauge3.value = val

    def setgauge4val(self,val):
        self._gauge4.value = val

    def setinstruction(self,str):
        self.Instructions.setText(str)

    def setlivetemp(self,val):
        self.usermsg.setText(str(val))

    def cleargraph(self):
        self.graphWidget.clear()

    def setgraph(self, val_list):
        self.GraphY = val_list[0]
        self.GraphX = val_list[1]
        #self.graphWidget.plot(val_list[1], val_list[0])


    def trigFRTrain(self,val):
        if val:
            self.fr.face_detection_widget.CheckTrainTrigger()
        #return(self.fr.face_detection_widget.faceID())

    """ def resFRTraintrig(self,val):
        if val:
            self.fr.face_detection_widget.resMeanFRSession() """

    def connectscansignals(self):
        self.scanthread._gauge1value.connect(self.setgauge1val)
        self.scanthread._gauge2value.connect(self.setgauge2val)
        self.scanthread._gauge3value.connect(self.setgauge3val)
        self.scanthread._gauge4value.connect(self.setgauge4val)
        self.scanthread.InstructionssetText.connect(self.setinstruction)
        self.scanthread.debugWindowsetText.connect(self.setdebugwin)
        self.scanthread.usermsgsetText.connect(self.setlivetemp)
        self.scanthread.graphWidgetclear.connect(self.cleargraph)
        self.scanthread.graphdata.connect(self.setgraph)
        self.scanthread.checktraintrigger.connect(self.trigFRTrain)
        #self.scanthread.restraintrig.connect(self.resFRTraintrig)



    def paintEvent(self, e):
        #self.fd.face_detection_widget.update()
        self.fr.face_detection_widget.update()
        #self.fd.update()
        self.fr.update()

        painter = QtGui.QPainter(self)

        self.brush = QtGui.QBrush()

        self.brush.setColor(QtGui.QColor('#242a30'))
        self.brush.setStyle(QtCore.Qt.SolidPattern)
        self.rect = QtCore.QRect(0, 0, painter.device().height() * self.dividerRatio, painter.device().height())
        painter.fillRect(self.rect, self.brush)

        self.brush.setColor(QtGui.QColor('#363a42'))
        self.brush.setStyle(QtCore.Qt.SolidPattern)
        self.rect = QtCore.QRect(painter.device().height()*self.dividerRatio, 0, painter.device().width(), painter.device().height())
        painter.fillRect(self.rect, self.brush)
        #self.debugWindow.adjustSize()

        self.myfont = QtGui.QFont()
        self.myfont.setPixelSize(painter.device().height() * 0.032)
        dw = painter.device().height() * 0.022
        sclabelfont = QtGui.QFont('Arial',(painter.device().height() * 0.012))
        sclabelfontH = QtGui.QFont('Arial',(painter.device().height() * 0.016))
        sclabelfontH1 = QtGui.QFont('Arial',(painter.device().height() * 0.016))
        self.vrecti = QtCore.QRect(0, 0, (painter.device().height() * 0.29), painter.device().height())

        self.vbox.setContentsMargins(painter.device().height() * 0.06, 10, 10, 10)  # Centers Gauges
        self.vbox.setGeometry(self.vrecti)
        self._gauge1.textFont = self.myfont
        self._gauge2.textFont = self.myfont
        self._gauge3.textFont = self.myfont
        self._gauge4.textFont = self.myfont
        self._gauge1.dialWidth = dw
        self._gauge2.dialWidth = dw
        self._gauge3.dialWidth = dw
        self._gauge4.dialWidth = dw
        self.label1.setFont(sclabelfont)
        self.label2.setFont(sclabelfont)
        self.label3.setFont(sclabelfont)
        self.label4.setFont(sclabelfont)
        self.LabelHeading.setFont(sclabelfontH)
        self.usermsg.setFont(sclabelfontH1)
        self.Instructions.setFont(sclabelfontH1)
        self.H1.setFont(sclabelfont)
        self.H2.setFont(sclabelfont)
        self.i1.setFont(sclabelfont)
        self.i2.setFont(sclabelfont)
        self.Instructions.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Maximum)
        self.usermsg.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Maximum)
        self.debugWindow.setMaximumSize((painter.device().width() * 0.75), painter.device().height()*0.03)
        self.debugWindow.setMinimumSize((painter.device().width() * 0.75), painter.device().height()*0.03)
        self.GraphBorder.setGeometry(QtCore.QRect(painter.device().width()*0.62, painter.device().height()*0.55, painter.device().width()*0.35, painter.device().height()*0.35))
        self.fr.setGeometry(QtCore.QRect(painter.device().width()*0.25, painter.device().height()*0.55, painter.device().width()*0.35, painter.device().height()*0.35))
        #self.fd.face_detection_widget.setGeometry(QtCore.QRect(painter.device().width()*0.25, painter.device().height()*0.06, painter.device().width()*0.35, painter.device().height()*0.35))
        self.messagepanellayout.setGeometry(QtCore.QRect(painter.device().width()*0.62, painter.device().height()*0.06, painter.device().width()*0.35, painter.device().height()*0.35))

        self.Instructions.setStyleSheet("color: orange; padding-bottom:10px; text-align: center;")
        # plot data: x, y values
        self.graphWidget.clear()
        self.graphWidget.plot(self.GraphX, self.GraphY)

        self.ttemp = self.fd.face_detection_widget.gettemp()
        #self.ttemp = 100
        self.scanthread.updatetemp(self.ttemp)

        self.faceID = self.fr.face_detection_widget.faceID()
        self.scanthread.updatefaceID(self.faceID)


def main():
    try:

        start = time.time()
        startt = time.strftime("%X %x")
        app = QApplication(sys.argv)
        ex = MainWindow()
        #self.frID = ex.fr.face_detection_widget.faceID()
        #self.frID.connect(self.trigFRTrain) 
        ex.show()
        sys.exit(app.exec_())
        sys.exit(app.scanthread.StopSerialThread())
    finally:
        execution_time = round((time.time() - start),2)
        with open("/home/sensor/Desktop/coviduipy/totalexec.csv","a+",newline = "") as file:
                        writer = csv.writer(file)
                        writer.writerow([startt, execution_time])


        


if __name__ == '__main__':
    main()