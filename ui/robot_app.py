from flask import Flask, render_template, request ,Response
import RPi.GPIO as GPIO
import serial
from time import sleep      # Import sleep module from time library to add delays
from camera_pi import Camera
import os
 
app = Flask(__name__)

arduino = serial.Serial('/dev/ttyACM1', 9600)  # invertir 1 x 0 segun los arduinos 
servo = serial.Serial('/dev/ttyACM0', 9600)
m18= 12
m11=18
m12=23
m21=24
m22=25

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(m11, GPIO.OUT)
GPIO.setup(m12, GPIO.OUT)
GPIO.setup(m21, GPIO.OUT)
GPIO.setup(m22, GPIO.OUT)
GPIO.setup(m18, GPIO.OUT)
GPIO.output(m11 , 0)
GPIO.output(m12 , 0)
GPIO.output(m21, 0)
GPIO.output(m22, 0)
GPIO.output(m18, 0)
print "DOne"

a=1

def gen(camera):
    """Video streaming generator function."""
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


@app.route('/video_feed')
def video_feed():
    """Video streaming route. Put this in the src attribute of an img tag."""
    return Response(gen(Camera()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')    
   

@app.route("/")
def index():
    return render_template('robot.html' )


@app.route('/left_side')
def left_side():
    data1="LEFT"
    GPIO.output(m11 , 0)
    GPIO.output(m12 , 0)
    GPIO.output(m21 , 1)
    GPIO.output(m22 , 0)
    return 'true'

@app.route('/right_side')
def right_side():
   data1="RIGHT"
   GPIO.output(m11 , 1)
   GPIO.output(m12 , 0)
   GPIO.output(m21 , 0)
   GPIO.output(m22 , 0)
   return 'true'

@app.route('/up_side')
def up_side():
   data1="FORWARD"
   GPIO.output(m11 , 1)
   GPIO.output(m12 , 0)
   GPIO.output(m21 , 1)
   GPIO.output(m22 , 0)
   return 'true'

@app.route('/down_side')
def down_side():
   data1="BACK"
   GPIO.output(m11 , 0)
   GPIO.output(m12 , 1)
   GPIO.output(m21 , 0)
   GPIO.output(m22 , 1)
   return 'true'

@app.route('/stop')
def stop():
   data1="STOP"
   GPIO.output(m11 , 0)
   GPIO.output(m12 , 0)
   GPIO.output(m21 , 0)
   GPIO.output(m22 , 0)
   return  'true'

@app.route('/ZO_side')
def ZO():
   data1="Z+"
   servo.write("75" + '\n')
   return  'true'

@app.route('/zo_side')
def zo():
   data1="Z-"
   servo.write("120" + '\n')
   return  'true'

@app.route('/centro')
def centro():
   data1="centro"
   servo.write("90" + '\n' )
   return  'true'
   
@app.route('/enableOFF')
def enableOFF():
   data1="motorOFF"
   GPIO.output(m18,1)
   return  'true'  
@app.route('/enableON')
def enableON():
   data1="motorON"
   GPIO.output(m18,0)
   sleep(1)
   return  'true'   

   
@app.route("/test", methods=["GET" ,"POST"])
def test():
    # Get slider Values
    AZ= request.form["AZ"]
    returnString = AZ  
    print(returnString)
    returnString = " {}".format(AZ)
    arduino.write(returnString +'\n' )
    return render_template('robot.html')
   

if __name__ == "__main__":
   app.run(host='0.0.0.0', port=8083, debug=True , threaded=True)