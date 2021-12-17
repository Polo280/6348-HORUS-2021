from networktables import NetworkTables

class LimelightCam():
    def __init__(self):
        self.dist_y = 0.3       # Distancia del suelo hasta la camara (m)
        self.targetDist_y = 2.5 # Distancia del suelo a cinta en el objeto
        self.tx = 0
        self.ty = 0
        self.tv = 0
        self.ta = 0

    def grabar(self):
        table = NetworkTables.getTable("limelight")
        self.tx = table.getNumber('tx', None)  #X
        self.ty = table.getNumber('ty', None)  #Y
        self.ta = table.getNumber('ta', None)  #Porcentaje de area de imagen
        self.tv = table.getNumber('tv', None)  #Bool, si hay un objetivo detectado

    def aimX(self): #rotMode -1 = left, 1 = right, 0 = None
        if self.tv:
            if self.tx < -0.5:
                rotMode = -1
            elif self.tx > 0.5:
                rotMode = 1
            else:
                rotMode = 0
        else:
            rotMode = 0

        return rotMode

    def aimY(self): #rotMode -1 = left, 1 = right, 0 = None
        if self.tv:
            if self.ty < -0.5:
                rotMode = -1
            elif self.ty > 0.5:
                rotMode = 1
            else:
                rotMode = 0
        else:
            rotMode = 0

        return rotMode