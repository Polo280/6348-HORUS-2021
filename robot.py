#DEVELOPMENT
import wpilib
import rev
import navx
from Clases.drivetrain import DriveTrain
from Clases.limelight import LimelightCam
from Clases.navxCode import Navx

class MyRobot(wpilib.TimedRobot):
    def robotInit(self):
        #Init chasis
        self.neo_lb = rev.CANSparkMax(1, rev.MotorType.kBrushless)
        self.neo_lf = rev.CANSparkMax(2, rev.MotorType.kBrushless)
        self.neo_rb = rev.CANSparkMax(3, rev.MotorType.kBrushless)
        self.neo_rf = rev.CANSparkMax(4, rev.MotorType.kBrushless)
        self.chasis = DriveTrain(self.neo_rf, self.neo_rb, self.neo_lf, self.neo_lb)

        self.shooter = rev.CANSparkMax(8, rev.MotorType.kBrushless)
        self.xbox1 = wpilib.XboxController(0)

        self.camera = LimelightCam()
        self.navx = navx.AHRS.create_spi()

    def robotPeriodic(self): #Run while robot is on
        wpilib.SmartDashboard.putNumber("Encoder right front", self.neo_rf.getEncoder().getPosition())

    def autonomousInit(self):
        pass

    def autonomousPeriodic(self):
        Navx.getValues(self.navx)

    def teleopInit(self):
        pass

    def teleopPeriodic(self):
        self.chasis.manejar(self.xbox1) #Manejar chasis

        #SHOOTER
        if self.xbox1.getAButton() and not self.xbox1.getBButton():
            self.shooter.set(1)

        elif not self.xbox1.getAButton() and self.xbox1.getBButton():
            self.shooter.set(-1)

        else:
            self.shooter.set(0)


if __name__ == "__main__":
    wpilib.run(MyRobot)