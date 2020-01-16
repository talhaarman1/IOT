import RPi.GPIO as GPIO  # calling for header file which helps in using GPIOs of PI
import time
from flask import Flask, jsonify
from flask_cors import CORS, cross_origin
from flask_httpauth import HTTPBasicAuth
import Adafruit_DHT
from time import sleep


app = Flask(__name__)
cors = CORS(app)
auth = HTTPBasicAuth()
users = {
    "Talha" : "abc",
    "Arslan" : "123",
    
}
employees = [
    {
        'id': 1,
        'name': 'Talha'
    },
    {
        'id': 2,
        'title': 'Arslan'
    }
]

app.config['CORS_HEADERS'] = 'Content-Type'

TRIG = 18
ECHO = 22
servo_pin = 40
servo_pin1 = 38
duty_cycle = 7.5

GPIO.setmode(GPIO.BOARD)
GPIO.setup(TRIG, GPIO.OUT)
GPIO.setup(ECHO, GPIO.IN)
GPIO.setup(servo_pin, GPIO.OUT)
GPIO.setup(11, GPIO.OUT)
GPIO.setup(13, GPIO.OUT)
GPIO.setup(15, GPIO.OUT)
GPIO.setup(16, GPIO.OUT)
GPIO.setup(33, GPIO.OUT)
GPIO.setup(35, GPIO.OUT)
GPIO.setup(36, GPIO.OUT)
GPIO.setup(38, GPIO.OUT)
GPIO.setwarnings(False)


@auth.get_password
def GetPassword(username):
    if(username in users):
        return  users.get(username)
    return None

def ResetServoToFront():

    GPIO.output(TRIG, False)
    pwm_servo = GPIO.PWM(servo_pin, 50)
    pwm_servo.start(7.5)
    pwm_servo.ChangeDutyCycle(7.5)
    time.sleep(0.1)


def SetAngle(angle):
    pwm=GPIO.PWM(servo_pin1, 50)
    pwm.start(0)
    duty = angle / 18 + 2
    GPIO.output(servo_pin1, True)
    pwm.ChangeDutyCycle(duty)
    sleep(1)
    GPIO.output(servo_pin1, False)
    pwm.ChangeDutyCycle(0)
    


def ReadSensorReading():
    GPIO.output(TRIG, True)
    time.sleep(0.00001)
    GPIO.output(TRIG, False)

    while GPIO.input(ECHO) == 0:
        pulse_start = time.time()

    while GPIO.input(ECHO) == 1:
        pulse_end = time.time()

    pulse_duration = pulse_end - pulse_start
    distance = pulse_duration * 17150
    distance = round(distance, 2)
    return distance

def GetSensorReadingsWithServo():
    GPIO.output(TRIG, False)
    pwm_servo = GPIO.PWM(servo_pin, 50)
    pwm_servo.start(duty_cycle)
    pwm_servo.ChangeDutyCycle(7.5)
    time.sleep(0.1)

    pwm_servo.ChangeDutyCycle(13)
    time.sleep(0.1)
    distincmsleft = ReadSensorReading()
    print "distincmsleft " + str(distincmsleft)

    time.sleep(0.1)
    pwm_servo.ChangeDutyCycle(10)
    time.sleep(0.1)
    distincmsleft1 = ReadSensorReading()
    print "distincmsleft1 " + str(distincmsleft1)

    time.sleep(0.1)
    pwm_servo.ChangeDutyCycle(7.5)
    time.sleep(0.1)
    distincmsstraight = ReadSensorReading()
    print "distincmsstraight " + str(distincmsstraight)

    time.sleep(0.1)
    pwm_servo.ChangeDutyCycle(5)
    time.sleep(0.1)
    distincmsright1 = ReadSensorReading()
    print "distincmsright1 " + str(distincmsright1)

    time.sleep(0.1)
    pwm_servo.ChangeDutyCycle(3)
    time.sleep(0.1)
    distincmsright = ReadSensorReading()
    print "distincmsright " + str(distincmsright)
    time.sleep(0.1)

    pwm_servo.start(duty_cycle)
    time.sleep(0.1)

    return distincmsleft, distincmsleft1, distincmsstraight, distincmsright1, distincmsright


#checking
def HornOn():
    GPIO.output(33, 1)
def HornOff():
    GPIO.output(33, 0)
def FanOn():
    GPIO.output(36, 1)
def FanOff():
    GPIO.output(36, 0)



def Forward():
    GPIO.output(11, 1)
    GPIO.output(13, 0)
    GPIO.output(15, 1)
    GPIO.output(16, 0)
    ResetServoToFront()

def LightOn():
    GPIO.output(35, 1)

def LightOff():
    GPIO.output(35, 0)

def Reverse():
    GPIO.output(11, 0)
    GPIO.output(13, 1)
    GPIO.output(15, 0)
    GPIO.output(16, 1)
    ResetServoToFront()

def Left():
    GPIO.output(11, 1)
    GPIO.output(13, 0)
    GPIO.output(15, 0)
    GPIO.output(16, 1)
    ResetServoToFront()

def Right():
    GPIO.output(11, 0)
    GPIO.output(13, 1)
    GPIO.output(15, 1)
    GPIO.output(16, 0)
    ResetServoToFront()

def Brake():
    GPIO.output(11, 1)
    GPIO.output(13, 1)
    GPIO.output(15, 1)
    GPIO.output(16, 1)
    ResetServoToFront()

@app.route('/api/login', methods=['POST'])
@cross_origin()
@auth.login_required
def index():
    return jsonify({'Login':'Success'})

@app.route('/api/employees', methods=['GET'])
def get_users():
    return jsonify({'employees': employees})

@app.route('/api/forward', methods=['GET'])
@cross_origin()
@auth.login_required
def forward():
    try:
        Forward()
        return jsonify({'forward': "1"})
    except:
        return jsonify({'forward': "0"})

@app.route('/api/lighton', methods=['GET'])
@cross_origin()
@auth.login_required
def lighton():
    try:
        LightOn()
        return jsonify({'light': "1"})
    except:
        return jsonify({'light': "-1"})


@app.route('/api/lightoff', methods=['GET'])
@cross_origin()
@auth.login_required
def lightoff():
    try:
        LightOff()
        return jsonify({'light': "0"})
    except:
        return jsonify({'light': "-1"})

@app.route('/api/reverse', methods=['GET'])
@cross_origin()
@auth.login_required
def reverse():
    try:
        Reverse()
        return jsonify({'reverse': "1"})
    except:
        return jsonify({'reverse': "0"})

@app.route('/api/left', methods=['GET'])
@cross_origin()
@auth.login_required
def left():
    try:
        for x in range(1, 3, 1):
            Left()
            time.sleep(0.1)
        Brake()
        return jsonify({'left': "1"})
    except:
        return jsonify({'left': "0"})

@app.route('/api/right', methods=['GET'])
@cross_origin()
@auth.login_required
def right():
    try:
        for x in range(1, 3, 1):
            Right()
            time.sleep(0.1)
        Brake()
        return jsonify({'right': "1"})
    except:
        return jsonify({'right': "0"})

@app.route('/api/brake', methods=['GET'])
@cross_origin()
@auth.login_required
def brake():
    try:
        Brake()
        return jsonify({'brake': "1"})
    except:
        return jsonify({'brake': "0"})


        #cheking
@app.route('/api/seearound', methods=['GET'])
@cross_origin()
@auth.login_required
def seearound():
    try:
        SeeAround()
        return jsonify({'seearound': "1"})
    except:
        return jsonify({'seearound': "-1"})
@app.route('/api/hornon', methods=['GET'])
@cross_origin()
@auth.login_required
def hornon():
    try:
        HornOn()
        return jsonify({'Horn': "1"})
    except:
        return jsonify({'Horn': "-1"})
@app.route('/api/hornoff', methods=['GET'])
@cross_origin()
@auth.login_required
def hornoff():
    try:
        HornOff()
        return jsonify({'Horn': "0"})
    except:
        return jsonify({'Horn': "-1"})


@app.route('/api/fanon', methods=['GET'])
@cross_origin()
@auth.login_required
def fanon():
    try:
        FanOn()
        return jsonify({'Fan': "1"})
    except:
        return jsonify({'Fan': "-1"})
@app.route('/api/fanoff', methods=['GET'])
@cross_origin()
@auth.login_required
def fanoff():
    try:
        FanOff()
        return jsonify({'Fan': "0"})
    except:
        return jsonify({'Fan': "-1"})


@app.route('/api/humidity', methods=['GET'])
@cross_origin()
@auth.login_required
def humidity():
    try:
        humidity, temperature = Adafruit_DHT.read_retry(11, 26)
        return jsonify({'humidity':humidity})
    except:
        return jsonify({'humidity':'-1'})
@app.route('/api/temperature', methods=['GET'])
@cross_origin()
@auth.login_required
def temperature():
    try:
        humidity, temperature = Adafruit_DHT.read_retry(11, 26)
        return jsonify({'temperature':temperature})
    except:
        return jsonify({'temperature':'-1'})


@app.route('/api/frontsensor', methods=['GET'])
@cross_origin()
@auth.login_required
def frontsensor():
    try:
        return jsonify({'reading': ReadSensorReading()})
    except:
        return jsonify({'reading': "-1"})

@app.route('/api/detailsensorreadings', methods=['GET'])
@cross_origin()
@auth.login_required
def detailsensorreadings():
    try:
        return jsonify({'detailsensorreadings': GetSensorReadingsWithServo()})
    except:
        return jsonify({'detailsensorreadings': "-1"})
@app.route('/api/move/<int:value>' , methods=['GET','POST'])
@cross_origin()
@auth.login_required
def setangle(value):
    try:
        print(value)
        SetAngle(value)
        pwm.stop()
        GPIO.cleanup()

        return jsonify({'Angle': value})
    
    except:
        return jsonify({'Angle': "-1"})

if __name__ == '__main__':
    try:
        app.run(debug=True, host='0.0.0.0', port=9000)
    finally:
        print("Cleaning Up!")
        GPIO.cleanup()