#datos entradas en DB
import hashlib
import random

class Profesor():

    def __init__(self, name, cedula, password, email, carrera):
        self.name = name
        self.cedula = cedula
        self.password = self.code_pass(password)
        self.email = email
        self.carrera = carrera
        self.registro_actividad = []

    def validate_uce(self, email):
        return email.endswith("@uce.edu.ec")
    
    def validate_ced(self, cedula):
        if len(cedula) != 10:
            raise ValueError("LA CEDULA DEBE SER DE 10 DIGITOS")
        return True

    def code_pass(self, password):
        return hashlib.sha256(password.encode()).hexdigest()
    
    def auth(self, password):
        return self.password == self.code_pass(password)
    
    def update_pass(self, password_new):
        self.password = self.code_pass(password_new)

    def update_informacion(self, name, carrera):
        if name:
            self.name = name
        if carrera:
            self.carrera = carrera
    
    def registro_act(self, materia, hora, fecha):
        self.registro_actividad.append({
            'materia': materia,
            'hora': hora,
            'fecha': fecha
        })

    def validate_pass(self, password):
        if password is None or len(password) > 8:
            raise ValueError("La contraseña debe tener máximo 8 caracteres")
        return self.auth(password)
    
    def recuperar_pass(self, correo):
        if correo.endswith("@uce.edu.ec"):
            new_password = ''.join(random.choices(''.join(map(chr, range(32, 127))),k=8))  
            self.password = self.code_pass(new_password)
            return new_password