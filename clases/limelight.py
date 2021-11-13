from networktables import NetworkTables

class LimelightCam():
    def __init__(self):
        self.dist_y = 0.3       # Distancia del suelo hasta la camara (m)
        self.targetDist_y = 2.5 # Distancia del suelo a cinta en el objeto

    def grabar(self):
        table = NetworkTables.getTable("limelight")
        tx = table.getNumber('tx', None)  #Anglo en x
        ty = table.getNumber('ty', None)  #Angulo en y
        ta = table.getNumber('ta', None)  #Porcentaje del area de imagen del target
        tv = table.getNumber('tv', None)  #Bool, si hay un objetivo detectado

        if ta < 1.5:
            return 1
        if ta > 3:
            return -1




