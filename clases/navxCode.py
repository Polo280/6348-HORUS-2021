import navx
import wpilib

class Navx():
    def __init__(self, navx: navx.AHRS):
        self.navx = navx

    def getValues(self):
        wpilib.SmartDashboard.putNumber("Accel X: ", self.navx.getRawAccelX())
        wpilib.SmartDashboard.putNumber("Pressure: ", self.navx.getPressure())