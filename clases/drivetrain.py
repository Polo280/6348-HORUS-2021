import wpilib
import rev
import math
from wpilib.drive import DifferentialDrive

class DriveTrain():
    def __init__(self, right_f: rev.CANSparkMax, right_b: rev.CANSparkMax, left_f: rev.CANSparkMax, left_b: rev.CANSparkMax):
        self.right_f = right_f
        self.left_f = left_f
        self.right_b = right_b
        self.left_b = left_b

        self.right = wpilib.SpeedControllerGroup(self.right_f, self.right_b)
        self.left = wpilib.SpeedControllerGroup(self.left_f, self.left_b)
        self.drive = wpilib.drive.DifferentialDrive(self.left, self.right)

        #CIRCUNFERENCE FOR ENCODER CONVERSION
        self.conversionMetres = 0.2 * 3.1416

        #PID Tuning
        self.KP = 0.1
        self.KI = 0.45
        self.KD = 0.8
        self.errorSum = 0
        self.lastError = 0

    @staticmethod
    def smooth_between(min, max, degrees):
        # min (angulo menor del intervalo)  1 --> Cuando deg = min, max - deg = intervalo
        # max (angulo mayor del intervalo) -1 --> Cuando deg = max su diferencia es 0
        # degrees (angulo actual del joystick)
        interval = max - min
        normalized = (max - degrees) / interval
        return 2 * normalized - 1  #Value -1 to 1


    def get_left_motor(self, degrees, gatillo):  #GENIUS Combinar esto con smooth_between
        #se asume que para avanzar derecho los dos motores se ponen en 1
        if 0 < degrees <= 90:
            return gatillo
        elif 90 < degrees <= 180:
            return self.smooth_between(180, 90, degrees) * (-1 * gatillo)
        elif 180 < degrees <= 270:
            return -1 * gatillo
        elif 270 < degrees <= 360:
            return self.smooth_between(270, 360, degrees) * (-1 * gatillo)
        else:
            return 0


    def get_right_motor(self, degrees, gatillo): #get motor power
        #se asume que para avanzar derecho los dos motores se ponen en 1
        if 0 < degrees <= 90:
            return self.smooth_between(90, 0, degrees) * (-1 * gatillo)
        elif 90 < degrees <= 180:
            return (-1 * gatillo)
        elif 180 < degrees <= 270:
            return self.smooth_between(180, 270, degrees) * (-1 * gatillo)
        elif 270 < degrees <= 360:
            return gatillo
        else:
            return 0


    def to_degrees(self, radians):
        degrees = math.degrees(radians)
        if degrees < 0:
            degrees = 360 + degrees

        degrees += 90
        if degrees > 360:
            degrees -= 360

        return degrees


    def manejar(self, xbox1):
        x = xbox1.getX(wpilib.XboxController.Hand.kLeftHand)
        y = -xbox1.getY(wpilib.XboxController.Hand.kLeftHand)

        trigger_left = xbox1.getTriggerAxis(wpilib.XboxController.Hand.kLeftHand)
        trigger_right = xbox1.getTriggerAxis(wpilib.XboxController.Hand.kRightHand)
        multiplicador = (trigger_left * 0.5) + (trigger_right * 0.5)

        deadZone = 0.2  #Avoid unwanted movement
        if math.fabs(x) < deadZone and math.fabs(y) < deadZone:
            multiplicador = 0
            x = 0
            y = 0

        angle = math.atan2(y, x) #Obtener angulo a partir de x,y con respecto a eje x
        heading = self.to_degrees(angle)

        left_power = self.get_left_motor(heading, multiplicador)
        right_power = self.get_right_motor(heading, multiplicador)
        self.drive.tankDrive(left_power, right_power)

    #AUTPILOT
    def autoStraight(self, reference):
        averageDist = ((self.right_f.getEncoder().getPosition() + self.left_f.getEncoder().getPosition())/2) * self.conversionMetres
        error = reference - averageDist
        self.errorSum += error

        output = self.KP * error
        #output = (self.KP * error + self.KI * self.errorSum + self.KD * (error - self.lastError))
        self.lastError = error

        self.left_f.set(output)
        self.left_b.set(output)
        self.right_f.set(-output)
        self.right_b.set(-output)