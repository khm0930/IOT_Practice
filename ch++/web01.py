from flask import Flask, render_template
import RPi.GPIO as GPIO
import time

app = Flask(__name__)
GPIO.setwarnings(False)

# GPIO 핀 설정 (초음파 센서)
GPIO.setmode(GPIO.BCM)
GPIO.setup(14, GPIO.OUT)  # Trig 핀
GPIO.setup(15, GPIO.IN)   # Echo 핀

# GPIO 핀 설정 (모터 드라이버)
ENA = 26
IN1 = 19
IN2 = 13
ENB = 0
IN3 = 6
IN4 = 5

GPIO.setup(ENA, GPIO.OUT)
GPIO.setup(IN1, GPIO.OUT)
GPIO.setup(IN2, GPIO.OUT)
GPIO.setup(ENB, GPIO.OUT)
GPIO.setup(IN3, GPIO.OUT)
GPIO.setup(IN4, GPIO.OUT)

motor_left_pwm = GPIO.PWM(ENA, 100)
motor_right_pwm = GPIO.PWM(ENB, 100)
motor_left_pwm.start(0)
motor_right_pwm.start(0)

# 부저를 위한 핀 설정
BUZZER_PIN = 4
GPIO.setup(BUZZER_PIN, GPIO.OUT)
p = GPIO.PWM(BUZZER_PIN, 100)  # PWM 인스턴스 생성

def stop_motors():
    GPIO.output(IN1, GPIO.LOW)
    GPIO.output(IN2, GPIO.LOW)
    GPIO.output(IN3, GPIO.LOW)
    GPIO.output(IN4, GPIO.LOW)
    motor_left_pwm.ChangeDutyCycle(0)
    motor_right_pwm.ChangeDutyCycle(0)

def beep():
    p.start(10)  # 부저 울리기 시작
    time.sleep(0.5)  # 0.5초 동안 소리 유지
    p.stop()  # 부저 중지

def ultrasonic_distance():
    GPIO.output(14, False)
    time.sleep(0.5)

    GPIO.output(14, True)
    time.sleep(0.00001)
    GPIO.output(14, False)

    while GPIO.input(15) == 0:
        start = time.time()

    while GPIO.input(15) == 1:
        stop = time.time()

    time_interval = stop - start
    distance = time_interval * 17000
    distance = round(distance, 2)

    return distance

@app.route('/')
def index():
    return render_template('web01.html')



@app.route('/forward')
def forward():
    GPIO.output(IN1, GPIO.HIGH)
    GPIO.output(IN2, GPIO.LOW)
    GPIO.output(IN3, GPIO.HIGH)
    GPIO.output(IN4, GPIO.LOW)
    motor_left_pwm.ChangeDutyCycle(100)
    motor_right_pwm.ChangeDutyCycle(100)
    distance = ultrasonic_distance()  # 초음파 센서로 거리 측정
    if distance <= 10:  # 10cm 이하일 경우에 부저 울림
        beep()
        stop()
    return 'Forward'

@app.route('/backward')
def backward():
    GPIO.output(IN1, GPIO.LOW)
    GPIO.output(IN2, GPIO.HIGH)
    GPIO.output(IN3, GPIO.LOW)
    GPIO.output(IN4, GPIO.HIGH)
    motor_left_pwm.ChangeDutyCycle(100)
    motor_right_pwm.ChangeDutyCycle(100)
    return 'Backward'

@app.route('/left')
def left():
    GPIO.output(IN1, GPIO.LOW)
    GPIO.output(IN2, GPIO.HIGH)
    GPIO.output(IN3, GPIO.HIGH)
    GPIO.output(IN4, GPIO.LOW)
    motor_left_pwm.ChangeDutyCycle(50)
    motor_right_pwm.ChangeDutyCycle(100)
    distance = ultrasonic_distance()  # 초음파 센서로 거리 측정
    if distance <= 10:  # 10cm 이하일 경우에 부저 울림
        beep()
    return 'Left'

@app.route('/right')
def right():
    GPIO.output(IN1, GPIO.HIGH)
    GPIO.output(IN2, GPIO.LOW)
    GPIO.output(IN3, GPIO.LOW)
    GPIO.output(IN4, GPIO.HIGH)
    motor_left_pwm.ChangeDutyCycle(50)
    motor_right_pwm.ChangeDutyCycle(100)
    distance = ultrasonic_distance()  # 초음파 센서로 거리 측정
    if distance <= 10:  # 10cm 이하일 경우에 부저 울림
        beep()
    return 'Right'

@app.route('/stop')
def stop():
    stop_motors()
    distance = ultrasonic_distance()  # 초음파 센서로 거리 측정
    if distance <= 10:  # 10cm 이하일 경우에 부저 울림
        beep()
    return 'Stopped'

if __name__ == '__main__':
    try:
        app.run(debug=True, host='0.0.0.0')
    except KeyboardInterrupt:
        stop_motors()
        GPIO.cleanup()
