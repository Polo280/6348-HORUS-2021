#DEVELOPMENT
import navx
import wpilib
import rev
from Clases.drivetrain import DriveTrain

class MyRobot(wpilib.TimedRobot):
    def robotInit(self):
        self.xbox1 = wpilib.XboxController(0)

        self.timer = wpilib.Timer()
        self.timer.start()

        self.navx = navx.AHRS.create_spi()

        #Init chasis
        self.shooter = rev.CANSparkMax(7, rev.CANSparkMax.MotorType.kBrushless)
        self.neo_lb = rev.CANSparkMax(5, rev.CANSparkMax.MotorType.kBrushless)
        self.neo_lf = rev.CANSparkMax(2, rev.CANSparkMax.MotorType.kBrushless)
        self.neo_rb = rev.CANSparkMax(3, rev.CANSparkMax.MotorType.kBrushless)
        self.neo_rf = rev.CANSparkMax(4, rev.CANSparkMax.MotorType.kBrushless)
        self.chasis = DriveTrain(self.neo_rf, self.neo_rb, self.neo_lf, self.neo_lb)

        self.shooterEnc = self.shooter.getEncoder()
        self.shooterEnc.setPositionConversionFactor(0.1524 * 3.1416)
        self.shooterReset = self.shooterEnc.getPosition()
        self.encoderPos = 0

        self.KP = 0.05 # 0.5
        self.KI = 0.01
        self.KD = 0.02
        self.errorSum = 0

    def robotPeriodic(self): #Run while robot is on
        #self.encoderPos = self.shooterEnc.getPosition() - self.shooterReset
        #wpilib.SmartDashboard.putNumber("Encoder shooter", self.encoderPos)
        #wpilib.SmartDashboard.putNumber("Shooter RPM", self.shooterEnc.getVelocity())
        #wpilib.SmartDashboard.putNumber("Temperature", self.navx.getTempC())
        wpilib.SmartDashboard.putNumber("Angle Z", self.navx.getAngle())
        wpilib.SmartDashboard.putNumber("Angle X", self.navx.getRoll())
        wpilib.SmartDashboard.putNumber("Yaw", self.navx.getYaw())


    def autonomousInit(self):
        self.brakeMotors(True)
        self.shooterReset = self.shooterEnc.getPosition()

    def autonomousPeriodic(self):
        setpoint = 0
        KP = 0.05
        KI = 0.02
        KD = 0.03

        if(self.xbox1.getAButton()):
            setpoint = 10
        elif self.xbox1.getBButton():
            setpoint = 0

        self.encoderPos = self.shooterEnc.getPosition()
        error = setpoint - self.encoderPos
        out = error * KP
        wpilib.SmartDashboard.putNumber("Error", error)
        wpilib.SmartDashboard.putNumber("Output", out)
        self.shooter.set(out)

    def teleopInit(self):
        self.brakeMotors(True)
        self.shooterReset = self.shooterEnc.getPosition()

    def teleopPeriodic(self):
        self.chasis.manejar(self.xbox1)
        if(self.xbox1.getAButton()):
            self.shooter.set(-0.9)
        elif self.xbox1.getBButton():
            self.shooter.set(-0.5)
        else:
            self.shooter.set(0)

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