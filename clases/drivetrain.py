#DEVELOPMENT
<<<<<<< HEAD
=======

>>>>>>> e81de67d240b9edba17627dbc07885aa8cf79902
import wpilib
import rev
from math import fabs
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

    def manejar(self, xbox1):
        x = -(xbox1.getX(wpilib.XboxController.Hand.kLeftHand))
        y = xbox1.getY(wpilib.XboxController.Hand.kLeftHand)

        R1 = (100 - fabs(x)) * (y / 100) + y  # R + L
        R2 = (100 - fabs(y)) * (x / 100) + x  # R - L
        right = (R1 + R2) / 2
        left = (R1 - R2) / 2

        trigger_left = xbox1.getTriggerAxis(wpilib.XboxController.Hand.kLeftHand)
        trigger_right = xbox1.getTriggerAxis(wpilib.XboxController.Hand.kRightHand)
        multiplicador = (trigger_left * 0.7) + (trigger_right * 0.3)

        self.drive.tankDrive(left * multiplicador, right * multiplicador)

