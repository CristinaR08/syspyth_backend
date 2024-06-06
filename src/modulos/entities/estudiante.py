class Estudiante:

    def __init__(self, cedula, name, correo, carrera):
        if self.validate_ced(cedula):
            self.cedula = cedula
        self.name = name.upper()
        self.carrera = carrera
        if self.validate_uce(correo):
            self.correo = correo
        else:
            raise ValueError("EL CORREO DEBE SER DE LA UCE!!!")
    
    def validate_uce(self, email):
        return email.endswith("@uce.edu.ec")
    
    def validate_ced(self, cedula):
        if len(cedula) != 10:
            raise ValueError("LA CEDULA DEBE SER DE 10 DIGITOS")
        return True
    
