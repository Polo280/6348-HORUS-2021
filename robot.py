#DEVELOPMENT
import wpilib
import rev
from Clases.drivetrain import DriveTrain

class MyRobot(wpilib.TimedRobot):
    def robotInit(self):
        self.xbox1 = wpilib.XboxController(0)

        self.timer = wpilib.Timer()
        self.timer.start()

        #Init chasis
        self.shooter = rev.CANSparkMax(7, rev.MotorType.kBrushless)
        self.neo_lb = rev.CANSparkMax(5, rev.MotorType.kBrushless)
        self.neo_lf = rev.CANSparkMax(2, rev.MotorType.kBrushless)
        self.neo_rb = rev.CANSparkMax(3, rev.MotorType.kBrushless)
        self.neo_rf = rev.CANSparkMax(4, rev.MotorType.kBrushless)
        self.chasis = DriveTrain(self.neo_rf, self.neo_rb, self.neo_lf, self.neo_lb)

        self.conversionFactor = 0.1524 * 3.1416
        self.shooterEnc = self.shooter.getEncoder()
        self.shooterReset = self.shooterEnc.getPosition() * self.conversionFactor

    def robotPeriodic(self): #Run while robot is on
        wpilib.SmartDashboard.putNumber("Encoder shooter", self.shooterEnc.getPosition() * self.conversionFactor - self.shooterReset)
        wpilib.SmartDashboard.putNumber("Shooter RPM", self.shooterEnc.getVelocity())

    def autonomousInit(self):
        self.brakeMotors(True)

    def autonomousPeriodic(self):
        self.chasis.autoStraight(1)

    def teleopInit(self):
        self.brakeMotors(True)
        self.shooterReset = self.shooterEnc.getPosition() * self.conversionFactor

    def teleopPeriodic(self):
        if(self.xbox1.getAButton() and not self.xbox1.getBButton()):
            self.shooter.set(.9)
        elif(self.xbox1.getBButton() and not self.xbox1.getAButton()):
            pass
        else:
            self.shooter.set(0)

        self.chasis.manejar(self.xbox1)

    def disabledInit(self):
        self.brakeMotors(False)

    #CUSTOM
    def brakeMotors(self, isEnabled): #Brake motors when autonomus & teleop
        if isEnabled == True:
            mode = rev.CANSparkMax.IdleMode.kBrake
        else:
            mode = rev.CANSparkMax.IdleMode.kCoast

        self.neo_lb.setIdleMode(mode)
        self.neo_lf.setIdleMode(mode)
        self.neo_rb.setIdleMode(mode)
        self.neo_rf.setIdleMode(mode)

if __name__ == "__main__":
    wpilib.run(MyRobot)