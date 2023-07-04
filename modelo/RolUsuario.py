class RolUsuario():
    def __init__(self,fkEmail,fkIdRol):
        self.fkEmail=fkEmail
        self.fkIdRol=fkIdRol

    def setFkEmail(self,fkEmail):
        self.fkEmail=fkEmail
    def getFkEmail(self):
        return self.fkEmail

    def setFkIdRol(self,fkIdRol):
        self.fkIdRol=fkIdRol
    def getFkIdRol(self):
        return self.fkIdRol