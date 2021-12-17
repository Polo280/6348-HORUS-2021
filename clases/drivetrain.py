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
        if degrees <= 90:
            return gatillo
        elif degrees <= 180:
            return self.smooth_between(180, 90, degrees) * (-1 * gatillo)
        elif degrees <= 270:
            return -1 * gatillo
        elif degrees <= 360:
            return self.smooth_between(270, 360, degrees) * (-1 * gatillo)
        else:
            return 0


    def get_right_motor(self, degrees, gatillo):
        #se asume que para avanzar derecho los dos motores se ponen en 1
        if degrees <= 90:
            return self.smooth_between(90, 0, degrees) * (-1 * gatillo)
        elif degrees <= 180:
            return (-1 * gatillo)
        elif degrees <= 270:
            return self.smooth_between(180, 270, degrees) * (-1 * gatillo)
        elif degrees <= 360:
            return gatillo
        else:
            return 0


    def to_degrees(self, radians):
        degrees = math.degrees(radians)
        if degrees < 0:
            degrees = 360 + degrees

        degrees += 90   # Se suman 90 grados para ...
        if degrees > 360:
            degrees -= 360

        return degrees


    def manejar(self, xbox1):
        x = -(xbox1.getX(wpilib.XboxController.Hand.kLeftHand))
        y = xbox1.getY(wpilib.XboxController.Hand.kLeftHand)

        trigger_left = xbox1.getTriggerAxis(wpilib.XboxController.Hand.kLeftHand)
        trigger_right = xbox1.getTriggerAxis(wpilib.XboxController.Hand.kRightHand)
        multiplicador = (trigger_left * 0.3) + (trigger_right * 0.7)

        deadZone = 0.15  #Avoid unwanted movement
        if math.fabs(x) <= deadZone and math.fabs(y) <= deadZone:
            x, y = 0, 0

        angle = math.atan2(y, x)
        heading = self.to_degrees(angle)
        left_power = self.get_left_motor(heading, multiplicador)
        right_power = self.get_right_motor(heading, multiplicador)
        self.drive.tankDrive(left_power, right_power)


    def displayValues(self):
        wpilib.SmartDashboard.putNumber("Encoder NEO 1:", self.left_f.getEncoder().getPosition())
        wpilib.SmartDashboard.putNumber("Temp NEO 1: ", self.left_f.getMotorTemperature())


    def seek(self, forward: int):
        if forward == 1:
            self.drive.tankDrive(-0.5, -0.5)
        elif forward == 0:
            pass
        elif forward == -1:
            self.drive.tankDrive(0.5, 0.5)
        elif forward == 2:
            self.drive.tankDrive(0.2, -0.2) #Spin