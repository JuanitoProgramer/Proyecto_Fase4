# -------------------------
# Clases
# -------------------------
import re
import abc

class Cliente:
    def __init__(self, nombre, documento, correo, telefono):
        # Validación del nombre
        if not isinstance(nombre, str) or not nombre.strip():
            raise ValueError("El nombre debe ser una cadena no vacía.")
        
        # Validación del documento (asumiendo cédula colombiana: 8-10 dígitos)
        if not isinstance(documento, str) or not re.match(r'^\d{8,10}$', documento):
            raise ValueError("El documento debe ser una cadena de 8 a 10 dígitos.")
        
        # Validación del correo electrónico
        if not isinstance(correo, str) or not re.match(r'^[\w\.-]+@[\w\.-]+\.\w+$', correo):
            raise ValueError("El correo debe tener un formato válido (ej: usuario@dominio.com).")
        
        # Validación del teléfono (asumiendo 10 dígitos para Colombia)
        if not isinstance(telefono, str) or not re.match(r'^\d{10}$', telefono):
            raise ValueError("El teléfono debe ser una cadena de exactamente 10 dígitos.")
        
        self.nombre = nombre
        self.documento = documento
        self.correo = correo
        self.telefono = telefono


class Servicio(abc.ABC):
    def __init__(self, nombre, costo_base, disponible, codigo, descripcion):
        # Validación del nombre
        if not isinstance(nombre, str) or not nombre.strip():
            raise ValueError("El nombre del servicio debe ser una cadena no vacía.")
        
        # Validación del costo_base
        if not isinstance(costo_base, (int, float)) or costo_base < 0:
            raise ValueError("El costo base debe ser un número positivo.")
        
        # Validación de disponible
        if not isinstance(disponible, bool):
            raise ValueError("Disponible debe ser un valor booleano (True o False).")
        
        # Validación del código
        if not isinstance(codigo, str) or not codigo.strip():
            raise ValueError("El código debe ser una cadena no vacía.")
        
        # Validación de la descripción
        if not isinstance(descripcion, str) or not descripcion.strip():
            raise ValueError("La descripción debe ser una cadena no vacía.")
        
        self.nombre = nombre
        self.costo_base = costo_base
        self.disponible = disponible
        self.codigo = codigo
        self.descripcion = descripcion
    
    @abc.abstractmethod
    def calcular_costo(self):
        pass
    
    @abc.abstractmethod
    def mostrar_descripcion(self):
        pass
    
    @abc.abstractmethod
    def validar_disponibilidad(self):
        pass


class ReservarSala(Servicio):
    def __init__(self, nombre, costo_base, disponible, codigo, descripcion, capacidad, tipo_de_sala, horas):
        super().__init__(nombre, costo_base, disponible, codigo, descripcion)
        
        # Validación de capacidad
        if not isinstance(capacidad, int) or capacidad <= 0:
            raise ValueError("La capacidad debe ser un número entero positivo.")
        
        # Validación de tipo_de_sala
        if not isinstance(tipo_de_sala, str) or not tipo_de_sala.strip():
            raise ValueError("El tipo de sala debe ser una cadena no vacía.")
        
        # Validación de horas
        if not isinstance(horas, (int, float)) or horas <= 0:
            raise ValueError("Las horas deben ser un número positivo.")
        
        self.capacidad = capacidad
        self.tipo_de_sala = tipo_de_sala
        self.horas = horas
    
    def calcular_costo(self):
        """Calcula el costo total: horas * costo_base"""
        return self.horas * self.costo_base
    
    def mostrar_descripcion(self):
        """Muestra la descripción detallada de la sala"""
        return f"Sala: {self.nombre} - Tipo: {self.tipo_de_sala} - Capacidad: {self.capacidad} personas - {self.descripcion}"
    
    def validar_disponibilidad(self):
        """Valida si la sala está disponible para reservar"""
        return self.disponible

