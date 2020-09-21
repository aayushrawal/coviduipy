import mysql.connector
from random import randint
import time
import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from time import strftime
#from email.MIMEImage import MIMEImage
from email.mime.image import MIMEImage
#from email.MIMEImage import MIMEImage

mydb = mysql.connector.connect(host = "localhost", user = "root", password = "root", database = "user_info")
                   
                    
mycursor = mydb.cursor()

#self.mycursor.execute("INSERT INTO positive VALUES (NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL)")
#self.mycursor.execute("SELECT * from positive WHERE id=%s",(self.faceID,))
#while True: print(mycursor.fetchall())

#timelog = [userid,imgpath,testtimer, FinalResult,FinalReadings["temp"],FinalReadings["hr"],FinalReadings["o2levels"],FinalReadings["rpm"],FinalReadings["ld"]]
#userid = [int(self.faceID),str("/home/sensor/Desktop/coviduipy/"+self.faceID+"-0.jpg"),self.localtimer, self.result,int(self.FinalReadings["temp"]),int(self.FinalReadings["hr"]),int(self.FinalReadings["o2levels"]),int(self.FinalReadings["rpm"]),int(self.FinalReadings["ld"])]

userid = [1,"testloc",None, "Positive",98,64,98,14,100]

#while True: print(userid)


#while True: print(self.userid)
sql = "INSERT INTO positive (id, imgpath, time, result, temp, hr, o2, rpm, ld ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s);"
#self.mycursor.execute("SELECT * from positive WHERE id=%s;",(self.faceID,))

#while True: print(sql)

#self.userstatus = mycursor.fetchall()

#while True: print(result, self.userstatus)
#if result=="Positive":# or self.userstatus!=0:
mycursor.execute(sql, userid)

mydb.commit()