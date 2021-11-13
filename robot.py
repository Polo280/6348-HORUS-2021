#DEVELOPMENT
import wpilib
import rev
from Clases.drivetrain import DriveTrain
from Clases.limelight import LimelightCam

class MyRobot(wpilib.TimedRobot):
    def robotInit(self):
        self.neo_rf = rev.CANSparkMax(1, rev.MotorType.kBrushless)
        self.neo_lf = rev.CANSparkMax(2, rev.MotorType.kBrushless)
        self.neo_rb = rev.CANSparkMax(3, rev.MotorType.kBrushless)
        self.neo_lb = rev.CANSparkMax(4, rev.MotorType.kBrushless)
        self.chasis = DriveTrain(self.neo_rf, self.neo_rb, self.neo_lf, self.neo_lb)

        self.shooter = rev.CANSparkMax(5, rev.MotorType.kBrushless)
        self.camera = LimelightCam()
        self.xbox1= wpilib.XboxController(0)

    def autonomousInit(self):
        pass

    def autonomousPeriodic(self):
        movedir = self.camera.grabar()
        self.chasis.move(movedir)

    def teleopInit(self):
        pass

    def teleopPeriodic(self):
        self.chasis.manejar(self.xbox1)

        if self.xbox1.getAButton() and self.xbox1.getBButton() == False:
            self.shooter.set(0.8)

        elif self.xbox1.getAButton() == False and self.xbox1.getBButton():
            self.shooter.set(-0.8)
            
        else:
            self.shooter.set(0)



if __name__ == "__main__":
    wpilib.run(MyRobot)