#DEVELOPMENT
import wpilib
import rev
from Clases.drivetrain import DriveTrain
from Clases.limelight import LimelightCam

class MyRobot(wpilib.TimedRobot):
    def robotInit(self):
        self.neo_lb = rev.CANSparkMax(1, rev.MotorType.kBrushless)
        self.neo_lf = rev.CANSparkMax(2, rev.MotorType.kBrushless)
        self.neo_rb = rev.CANSparkMax(3, rev.MotorType.kBrushless)
        self.neo_rf = rev.CANSparkMax(4, rev.MotorType.kBrushless)
        self.shooter = rev.CANSparkMax(8, rev.MotorType.kBrushless)

        self.chasis = DriveTrain(self.neo_rf, self.neo_rb, self.neo_lf, self.neo_lb)
        self.xbox1= wpilib.XboxController(0)
        self.camera = LimelightCam()

    def autonomousInit(self):
        pass

    def autonomousPeriodic(self):
        self.camera.grabar()


    def teleopInit(self):
        pass

    def teleopPeriodic(self):
        self.chasis.manejar(self.xbox1) #Manejar chasis
        aim_x = LimelightCam.aimX(self.camera)
        aim_y = LimelightCam.aimY(self.camera)

        #SHOOTER
        if self.xbox1.getAButton() and not self.xbox1.getBButton():
            self.shooter.set(1)

        elif not self.xbox1.getAButton() and self.xbox1.getBButton():
            self.shooter.set(-1)

        else:
            self.shooter.set(0)

if __name__ == "__main__":
    wpilib.run(MyRobot)