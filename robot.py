#DEVELOPMENT
import wpilib
import rev
from    Clases.drivetrain import DriveTrain

class MyRobot(wpilib.TimedRobot):
    def robotInit(self):
        self.neo_rf = rev.CANSparkMax(1, rev.MotorType.kBrushless)
        self.neo_lf = rev.CANSparkMax(2, rev.MotorType.kBrushless)
        self.neo_rb = rev.CANSparkMax(3, rev.MotorType.kBrushless)
        self.neo_lb = rev.CANSparkMax(4, rev.MotorType.kBrushless)
        self.chasis = DriveTrain(self.neo_rf, self.neo_rb, self.neo_lf, self.neo_lb)

        self.xbox1= wpilib.XboxController(0)

    def autonomousInit(self):
        pass

    def autonomousPeriodic(self):
        pass

    def teleopInit(self):
        pass

    def teleopPeriodic(self):
        self.chasis.manejar(self.xbox1)

if __name__ == "__main__":
    wpilib.run(MyRobot)