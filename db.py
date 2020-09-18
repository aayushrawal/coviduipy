import mysql.connector
from random import randint
import time
import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from time import strftime

#TODO: Condition to enter user data if userid already in database or if test result negative

mydb = mysql.connector.connect(host = "localhost", user = "root", password = "root", database = "user_info")

testtimer = time.strftime('%Y-%m-%d %H:%M:%S')

userid = 2

imgpath = "imgpath"

vals = input().split(",")

FinalReadings = {"temp":vals[0],"hr":vals[1],"o2levels":vals[2],"rpm":vals[3],"ld":vals[4]}

if vals[-1]=="0":
  FinalResult = "Negative"
else: FinalResult = "Positive"



#insert into database

mycursor = mydb.cursor()
timelog = [userid,imgpath,testtimer, FinalResult,FinalReadings["temp"],FinalReadings["hr"],FinalReadings["o2levels"],FinalReadings["rpm"],FinalReadings["ld"]]
sql = "INSERT INTO positive (id, imgpath, time, result, temp, hr, o2, rpm, ld ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
mycursor.execute(sql, timelog)

mydb.commit()

mycursor.execute("SELECT * FROM positive where id IN (SELECT id FROM positive group by ID having count(id)>2)")


res_data = mycursor.fetchall()

print(res_data)

if res_data!=[]:
  sender_email = "coviduipy@gmail.com"
  receiver_email = "aayushrawal98@gmail.com"
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
            display:none;
            border: none;
            clip: rect(0 0 0 0);
            height: 0px;
            margin: 0px;
            overflow: hidden;
            padding: 0;
            max-width:0px;
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
            float: left;
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
                              <td data-label="Scan 1" valign="top" style="padding:5px; font-family: Arial,sans-serif; font-size: 16px; line-height:20px;">"{}"</td>
                              <td data-label="Scan 2" valign="top" style="padding:5px; font-family: Arial,sans-serif; font-size: 16px; line-height:20px;">{}</td>
                              <td data-label="Scan 3" valign="top" style="padding:5px; font-family: Arial,sans-serif; font-size: 16px; line-height:20px;">{}</td>
                              
                            </tr>
                            <tr>
                              <th data-label="Name" valign="top" style="padding:5px; font-family: Arial,sans-serif; font-size: 16px; line-height:20px;">Heart Rate</th>
                              <td data-label="Scan 1" valign="top" style="padding:5px; font-family: Arial,sans-serif; font-size: 16px; line-height:20px;">{}</td>
                              <td data-label="Scan 2" valign="top" style="padding:5px; font-family: Arial,sans-serif; font-size: 16px; line-height:20px;">"{}"</td>
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
                      <tr>
                        <th scope="col" style="padding:5px; font-family: Arial,sans-serif; font-size: 16px; line-height:20px;line-height:30px">Image taken during scan:</th>
                          </tr>
                        </thead>
                        <tbody>
                        <tr>
                          <td data-label="User Image" valign="top" style="padding:5px; font-family: Arial,sans-serif; font-size: 16px; line-height:20px;">
                              <img alt="" src="https://picsum.photos/200" width="200" style="display: inline-block;" />
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
              
              <!--<table width="100%" cellpadding="0" cellspacing="0" border="0" style="min-width:100%;">
                <tr>
                  <td width="100%" style="min-width:100%;">
                    <table cellpadding="0" cellspacing="0" border="0" width="100%">
                      <tr>
                        <td style="padding:30px;background-color:#58585a;color:#ffffff;">
                          <p style="font-family:Georgia, Arial, sans-serif;font-size:16px;line-height:20px;text-align: center;">2020 @ <a href="www.github.com/aayushrawal">aayushrawal</a></p>
                        </td>
                      </tr>
                    </table>
                  </td>
                </tr>
              </table>-->
            </td>
          </tr>
        </table>

        <!--[if gte mso 9]></td></tr></table>
                      <![endif]-->
      </center>
    </body>
  </html>
  """.format(res_data[0][4],res_data[1][4],res_data[2][4],res_data[0][5],res_data[1][5],res_data[2][5],res_data[0][6],res_data[1][6],res_data[2][6],res_data[0][7],res_data[1][7],res_data[2][7],res_data[0][8],res_data[1][8],res_data[2][8],res_data[0][3],res_data[1][3],res_data[2][3],res_data[0][0],res_data[0][2].strftime('%Y-%m-%d %H:%M:%S'))


  # Turn these into plain/html MIMEText objects
  part1 = MIMEText(html, "html")


  # Add HTML/plain-text parts to MIMEMultipart message
  # The email client will try to render the last part first
  message.attach(part1)

  # Create secure connection with server and send email
  context = ssl.create_default_context()
  with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
      server.login(sender_email, password)
      server.sendmail(
          sender_email, receiver_email, message.as_string()
      )
  
  mycursor = mydb.cursor()

  sql = "DELETE FROM positive WHERE id={}".format(res_data[0][0])

  mycursor.execute(sql)

  mydb.commit()