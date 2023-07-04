class Usuario():
    def __init__(self,email,contrasena):
        self.email=email
        self.contrasena=contrasena

    def setEmail(self,email):
        self.email=email
    def getEmail(self):
        return self.email

    def setContrasena(self,contrasena):
        self.contrasena=contrasena
    def getContrasena(self):
        return self.contrasena