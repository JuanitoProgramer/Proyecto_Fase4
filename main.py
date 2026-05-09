# =============================================================================
# Sistema Integral de Gestión de Clientes, Servicios y Reservas
# Empresa: Software FJ
# =============================================================================

# -------------------------
# Importaciones
# -------------------------
import os
import re
import abc
from datetime import datetime
from pathlib import Path
import tkinter as tk
from tkinter import messagebox, ttk


# -------------------------
# Archivo de logs
# -------------------------
LOG_FILE = Path(__file__).resolve().parent / "logs.txt"


def registrar_log(mensaje):
    try:
        with LOG_FILE.open("a", encoding="utf-8") as archivo:
            fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            archivo.write(f"[{fecha}] {mensaje}\n")
    except Exception as e:
        print(f"Error al escribir en logs: {e}")
        try:
            LOG_FILE.parent.mkdir(parents=True, exist_ok=True)
            with LOG_FILE.open("w", encoding="utf-8") as archivo:
                fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                archivo.write(f"[{fecha}] Archivo de logs creado\n")
                archivo.write(f"[{fecha}] {mensaje}\n")
        except Exception as e2:
            print(f"No se pudo crear logs.txt: {e2}")


# -------------------------
# Excepciones personalizadas
# -------------------------
class ClienteError(Exception):
    """Excepción para errores relacionados con clientes."""
    pass


class ServicioError(Exception):
    """Excepción para errores relacionados con servicios."""
    pass


class ReservaError(Exception):
    """Excepción para errores relacionados con reservas."""
    pass


class PagoError(Exception):
    """Excepción para errores relacionados con pagos."""
    pass

# Nueva excepción específica para disponibilidad
class DisponibilidadError(ServicioError):   
    """Excepción  para indicar cuando un servicio no está disponible. Demuestra jerarquía"""
    pass


class EntidadSistema(abc.ABC):
    """
    clase que obliga a todas las entidades del sistema a 
    implementar mostrar_info() y validar().
    
    """

    @abc.abstractmethod
    def mostrar_info(self):
        """Muestra información general de la entidad."""
        pass

    @abc.abstractmethod
    def validar(self):
        """Valida que la entidad tiene datos correctos."""
        pass

    def tipo_entidad(self):
        """Método concreto disponible para todas las entidades."""
        return f"Entidad: {self.__class__.__name__}"

#

# -------------------------
# Clase Cliente
# -------------------------
class Cliente:

    def __init__(self, nombre, documento, correo, telefono):
        
        # validaciones originales conservadas
        if not isinstance(nombre, str) or not nombre.strip():
            raise ClienteError("El nombre debe ser válido")

        if not isinstance(documento, str) or not re.match(r"^\d{8,10}$", documento):
            raise ClienteError("Documento inválido")

        if not isinstance(correo, str) or not re.match(
            r"^[\w\.-]+@[\w\.-]+\.\w+$", correo
        ):
            raise ClienteError("Correo inválido")

        if not isinstance(telefono, str) or not re.match(r"^\d{10}$", telefono):
            raise ClienteError("Teléfono inválido")

        # Atributos privados con encapsulación
        self.__nombre = nombre
        self.__documento = documento
        self.__correo = correo
        self.__telefono = telefono

    # Propiedades originales conservadas
    @property
    def nombre(self):
        return self.__nombre

    @property
    def documento(self):
        return self.__documento

    @property
    def correo(self):
        return self.__correo

    @property
    def telefono(self):
        return self.__telefono

    def mostrar_info(self):
        return f"Cliente: {self.__nombre} - Documento: {self.__documento}"

    def validar(self):
       #verifica que los datos del cliente sigan siendo correctos 
       
        return bool(self.__nombre and self.__documento and self.__correo and self.__telefono)
 
# -------------------------
# Clase abstracta Servicio
# -------------------------
class Servicio(abc.ABC):

    def __init__(self, nombre, costo_base, disponible, codigo, descripcion):
        # Validaciones originales conservadas
        if not isinstance(nombre, str) or not nombre.strip():
            raise ServicioError("Nombre del servicio inválido")

        if not isinstance(costo_base, (int, float)) or costo_base <= 0:
            raise ServicioError("Costo base inválido")

        if not isinstance(disponible, bool):
            raise ServicioError("Disponible debe ser True o False")

        if not isinstance(codigo, str) or not codigo.strip():
            raise ServicioError("Código inválido")

        if not isinstance(descripcion, str) or not descripcion.strip():
            raise ServicioError("Descripción inválida")
        # Atributos privados
        self.__nombre = nombre
        self.__costo_base = costo_base
        self.__disponible = disponible
        self.__codigo = codigo
        self.__descripcion = descripcion
        
    # Propiedades originales conservadas
    @property
    def nombre(self):
        return self.__nombre

    @property
    def costo_base(self):
        return self.__costo_base

    @property
    def disponible(self):
        return self.__disponible

    @property
    def codigo(self):
        return self.__codigo

    @property
    def descripcion(self):
        return self.__descripcion
    
    # Métodos abstractos originales conservados
    @abc.abstractmethod
    def calcular_costo(self, descuento=0, impuesto=0):
        pass

    @abc.abstractmethod
    def mostrar_descripcion(self):
        pass

    @abc.abstractmethod
    def validar_disponibilidad(self):
        pass
    
    def mostrar_info(self):
        """Implementación de mostrar_info de EntidadSistema."""
        return self.mostrar_descripcion()
    
    def validar(self):
        """
        Implementación del método abstracto validar() de EntidadSistema.
        """
        return self.__disponible and self.__costo_base > 0


# -------------------------
# Reserva de Sala
# -------------------------
class ReservarSala(Servicio):

    def __init__(
        self,
        nombre,
        costo_base,
        disponible,
        codigo,
        descripcion,
        capacidad,
        tipo_sala,
        horas,
    ):

        super().__init__(nombre, costo_base, disponible, codigo, descripcion)

        if not isinstance(capacidad, int) or capacidad <= 0:
            raise ServicioError("Capacidad inválida")

        if not isinstance(tipo_sala, str) or not tipo_sala.strip():
            raise ServicioError("Tipo de sala inválido")

        if not isinstance(horas, (int, float)) or horas <= 0:
            raise ServicioError("Horas inválidas")

        self.capacidad = capacidad
        self.tipo_sala = tipo_sala
        self.horas = horas

    def calcular_costo(self, descuento=0, impuesto=0):
        
        try:
            if not (0 <= descuento <= 1):
                raise ValueError("Descuento debe estar entre 0 y 1")
            if not (0 <= impuesto <= 1):
                raise ValueError("Impuesto debe estar entre 0 y 1")
            costo = self.horas * self.costo_base
            costo -= costo * descuento
            costo += costo * impuesto
        except ValueError as e:
            registrar_log(f"ERROR cálculo sala: {e}")
            raise ServicioError("Parámetros de cálculo inválidos") from e
        else:
            registrar_log(f"Costo de sala calculado: ${costo:.2f}")
        finally:
            pass  
        return round(costo, 2)

    def mostrar_descripcion(self):
        return f"Sala: {self.nombre} - Tipo: {self.tipo_sala} - Capacidad: {self.capacidad}"

    def validar_disponibilidad(self):
      
        if not self.disponible:
            raise DisponibilidadError(f"La sala '{self.nombre}' no está disponible")
        return True


# -------------------------
# Alquiler de Equipo
# -------------------------
class AlquilerEquipo(Servicio):

    def __init__(
        self,
        nombre,
        costo_base,
        disponible,
        codigo,
        descripcion,
        tipo_equipo,
        dias,
        garantia,
    ):

        super().__init__(nombre, costo_base, disponible, codigo, descripcion)

        if not isinstance(tipo_equipo, str) or not tipo_equipo.strip():
            raise ServicioError("Tipo de equipo inválido")

        if not isinstance(dias, (int, float)) or dias <= 0:
            raise ServicioError("Días inválidos")

        if not isinstance(garantia, bool):
            raise ServicioError("Garantía inválida")

        self.tipo_equipo = tipo_equipo
        self.dias = dias
        self.garantia = garantia

    def calcular_costo(self, descuento=0, impuesto=0):
        
        try:
            if not (0 <= descuento <= 1):
                raise ValueError("Descuento debe estar entre 0 y 1")
            if not (0 <= impuesto <= 1):
                raise ValueError("Impuesto debe estar entre 0 y 1")
            costo = self.dias * self.costo_base
            if self.garantia:
                costo += costo * 0.05
            costo -= costo * descuento
            costo += costo * impuesto
        except ValueError as e:
            registrar_log(f"ERROR cálculo equipo: {e}")
            raise ServicioError("Parámetros de cálculo inválidos") from e
        else:
            registrar_log(f"Costo de equipo calculado: ${costo:.2f}")
        finally:
            pass
        return round(costo, 2) 

    def mostrar_descripcion(self):
        garantia_str = "Con garantía" if self.garantia else "Sin garantía"
        return f"Equipo: {self.nombre} - Tipo: {self.tipo_equipo} - {garantia_str}"

    def validar_disponibilidad(self):
        if not self.disponible:
            raise DisponibilidadError(f"El equipo '{self.nombre}' no está disponible")
        return True

# -------------------------
# Asesoría
# -------------------------
class Asesoria(Servicio):

    def __init__(
        self,
        nombre,
        costo_base,
        disponible,
        codigo,
        descripcion,
        especialista,
        tema,
        horas,
    ):

        super().__init__(nombre, costo_base, disponible, codigo, descripcion)

        if not isinstance(especialista, str) or not especialista.strip():
            raise ServicioError("Especialista inválido")

        if not isinstance(tema, str) or not tema.strip():
            raise ServicioError("Tema inválido")

        if not isinstance(horas, (int, float)) or horas <= 0:
            raise ServicioError("Horas inválidas")

        self.especialista = especialista
        self.tema = tema
        self.horas = horas

    def calcular_costo(self, descuento=0, impuesto=0):
        
        try:
            if not (0 <= descuento <= 1):
                raise ValueError("Descuento debe estar entre 0 y 1")
            if not (0 <= impuesto <= 1):
                raise ValueError("Impuesto debe estar entre 0 y 1")
            costo = self.horas * self.costo_base
            costo -= costo * descuento
            costo += costo * impuesto
        except ValueError as e:
            registrar_log(f"ERROR cálculo asesoría: {e}")
            raise ServicioError("Parámetros de cálculo inválidos") from e
        else:
            registrar_log(f"Costo de asesoría calculado: ${costo:.2f}")
        finally:
            pass
        return round(costo, 2)

    def mostrar_descripcion(self):
        return f"Asesoría: {self.nombre} - Tema: {self.tema} - Especialista: {self.especialista}"

    def validar_disponibilidad(self): 
    # Lanza DisponibilidadError si no está disponible.
        if not self.disponible:
            raise DisponibilidadError(f"La asesoría '{self.nombre}' no está disponible")
        return True


# -------------------------
# Clase Reserva
# -------------------------
class Reserva:

    def __init__(self, cliente, servicio, fecha, duracion, estado="activo"):

        if not isinstance(cliente, Cliente):
            raise ReservaError("Cliente inválido")

        if not isinstance(servicio, Servicio):
            raise ReservaError("Servicio inválido")

        try:
            self.fecha = datetime.strptime(fecha, "%Y-%m-%d")
        except ValueError as e:
            raise ReservaError("Formato de fecha incorrecto (use YYYY-MM-DD)") from e

        if not isinstance(duracion, (int, float)) or duracion <= 0:
            raise ReservaError("Duración inválida (debe ser mayor a 0)")

        self.cliente = cliente
        self.servicio = servicio
        self.duracion = duracion
        self.estado = estado

    def confirmar(self):
    
        try:
            self.servicio.validar_disponibilidad()
        except DisponibilidadError as e:
            raise ReservaError(f"No se puede confirmar: {e}") from e

        self.estado = "confirmado"
        registrar_log(f"Reserva confirmada para {self.cliente.nombre}")
        return "Reserva confirmada"

    def cancelar(self):

        if self.estado == "cancelado":
            raise ReservaError("La reserva ya está cancelada")

        self.estado = "cancelado"
        registrar_log(f"Reserva cancelada para {self.cliente.nombre}")
        return "Reserva cancelada"

    def obtener_costo_total(self, descuento=0, impuesto=0):
        return self.servicio.calcular_costo(descuento=descuento, impuesto=impuesto)

    def mostrar_detalles(self):

        return (
            f"Cliente: {self.cliente.nombre}\n"
            f"Servicio: {self.servicio.nombre}\n"
            f"Fecha: {self.fecha.strftime('%Y-%m-%d')}\n"
            f"Duración: {self.duracion} horas\n"
            f"Estado: {self.estado}"
        )

    def procesar_pago(self, descuento=0, impuesto=0):
        if self.estado == "cancelado":
            raise PagoError("No se puede pagar una reserva cancelada")

        if self.estado != "confirmado":
            raise PagoError("La reserva debe estar confirmada antes de pagar")

        total = self.obtener_costo_total(descuento=descuento, impuesto=impuesto)
        registrar_log(f"Pago procesado: ${total} para {self.cliente.nombre}")
        return f"Pago procesado correctamente. Total: ${total:.2f}"


# -------------------------
# Simulación del sistema
# -------------------------
clientes = []
servicios = []
reservas = []

# -------------------------
# Operaciones de prueba
# -------------------------
try:
    sala1 = ReservarSala("Sala VIP", 50000, True, "SV01", "Sala premium", 20, "VIP", 2)
    sala2 = ReservarSala("Sala Conferencias", 30000, True, "SC01", "Sala para conferencias", 50, "Conferencia", 3)
    sala3 = ReservarSala("Sala No Disponible", 20000, False, "SN01", "Fuera de servicio", 10, "Básica", 1)
    servicios.extend([sala1, sala2, sala3])
    registrar_log("Servicios de sala cargados correctamente")
except ServicioError as e:
    registrar_log(f"ERROR cargando salas: {e}")

# Equipos
try:
    equipo1 = AlquilerEquipo("Laptop HP", 15000, True, "EL01", "Laptop de alto rendimiento", "Computador", 3, True)
    equipo2 = AlquilerEquipo("Proyector 4K", 20000, True, "EP01", "Proyector profesional", "Proyector", 2, False)
    servicios.extend([equipo1, equipo2])
    registrar_log("Servicios de equipo cargados correctamente")
except ServicioError as e:
    registrar_log(f"ERROR cargando equipos: {e}")

# Asesorías
try:
    asesoria1 = Asesoria("Asesoría Legal", 80000, True, "AL01", "Consulta legal empresarial", "Dr. García", "Contratos", 2)
    asesoria2 = Asesoria("Asesoría Tech", 60000, True, "AT01", "Consultoría tecnológica", "Ing. López", "Arquitectura Software", 3)
    servicios.extend([asesoria1, asesoria2])
    registrar_log("Servicios de asesoría cargados correctamente")
except ServicioError as e:
    registrar_log(f"ERROR cargando asesorías: {e}")



print("\n" + "="*60)
print("   SIMULACIÓN DE OPERACIONES - Software FJ")
print("="*60)

# =============================================================================
# SIMULACIÓN DE 10 OPERACIONES COMPLETAS
# Este bloque se ejecuta automáticamente al arrancar el programa.
# Su propósito es demostrar que el sistema funciona correctamente
# tanto con datos válidos como con datos inválidos, sin que el
# programa se detenga ante los errores.
# =============================================================================

# -----------------------------------------------------------------------
# OPERACIÓN 1: Cliente válido
# -----------------------------------------------------------------------

print("\n[OP 1] Registrar cliente válido")
try:
    cliente1 = Cliente("Juan Miguel", "12345678", "juan@gmail.com", "3001234567")
    clientes.append(cliente1)
    registrar_log("OP1 - Cliente Juan Miguel registrado correctamente")
except ClienteError as e:
    registrar_log(f"OP1 - ERROR CLIENTE: {e}")
else:
    # AGREGADO: bloque else - se ejecuta solo si no hubo excepción
    print(f"  ✓ {cliente1.mostrar_info()}")
finally:
    print("  → OP1 finalizada")

# -----------------------------------------------------------------------
# OPERACIÓN 2: Cliente inválido (error intencional)
# -----------------------------------------------------------------------

print("\n[OP 2] Intentar registrar cliente con datos inválidos")
try:
    cliente_error = Cliente("", "12", "correo_malo", "123")
    clientes.append(cliente_error)
except ClienteError as e:
    print(f"  ✗ Error esperado: {e}")
    registrar_log(f"OP2 - ERROR INTENCIONAL CLIENTE: {e}")
finally:
    print("  → OP2 finalizada")

# -----------------------------------------------------------------------
# OPERACIÓN 3: Cliente con correo inválido
# -----------------------------------------------------------------------
print("\n[OP 3] Cliente con correo inválido")
try:
    cliente_correo_mal = Cliente("Ana Torres", "98765432", "no_es_correo", "3109876543")
    clientes.append(cliente_correo_mal)
except ClienteError as e:
    print(f"  ✗ Error esperado: {e}")
    registrar_log(f"OP3 - ERROR CLIENTE CORREO: {e}")
else:
    print("  ✓ Cliente registrado")
finally:
    print("  → OP3 finalizada")

# -----------------------------------------------------------------------
# OPERACIÓN 4: Segundo cliente válido
# -----------------------------------------------------------------------
print("\n[OP 4] Registrar segundo cliente válido")
try:
    cliente2 = Cliente("María Pérez", "87654321", "maria@empresa.com", "3157654321")
    clientes.append(cliente2)
    registrar_log("OP4 - Cliente María Pérez registrado")
except ClienteError as e:
    registrar_log(f"OP4 - ERROR: {e}")
else:
    print(f"  ✓ {cliente2.mostrar_info()}")
finally:
    print("  → OP4 finalizada")

# -----------------------------------------------------------------------
# OPERACIÓN 5: Servicio con costo base inválido
# -----------------------------------------------------------------------
print("\n[OP 5] Crear servicio con costo negativo (inválido)")
try:
    sala_invalida = ReservarSala("Sala Error", -5000, True, "SE01", "Sala inválida", 10, "Básica", 2)
    servicios.append(sala_invalida)
except ServicioError as e:
    print(f"  ✗ Error esperado: {e}")
    registrar_log(f"OP5 - ERROR SERVICIO COSTO: {e}")
else:
    print("  ✓ Servicio creado")
finally:
    print("  → OP5 finalizada")

# -----------------------------------------------------------------------
# OPERACIÓN 6: Reserva exitosa con confirmación y pago
# -----------------------------------------------------------------------
print("\n[OP 6] Crear reserva exitosa y procesar pago")
try:
    reserva1 = Reserva(cliente1, sala1, "2026-05-20", 2)
    reservas.append(reserva1)
    confirmacion = reserva1.confirmar()
    # AGREGADO: calcular con impuesto del 19%
    costo_con_iva = reserva1.obtener_costo_total(impuesto=0.19)
    pago = reserva1.procesar_pago(impuesto=0.19)
    registrar_log("OP6 - Reserva creada y pagada correctamente")
except (ReservaError, PagoError) as e:
    registrar_log(f"OP6 - ERROR RESERVA: {e}")
else:
    print(f"  ✓ {confirmacion}")
    print(f"  ✓ Costo con IVA 19%: ${costo_con_iva}")
    print(f"  ✓ {pago}")
finally:
    print("  → OP6 finalizada")

# -----------------------------------------------------------------------
# OPERACIÓN 7: Intentar reservar servicio NO disponible
# -----------------------------------------------------------------------
print("\n[OP 7] Reservar sala no disponible (error encadenado)")
try:
    reserva_imposible = Reserva(cliente1, sala3, "2026-06-01", 1)
    reserva_imposible.confirmar()
except ReservaError as e:
    print(f"  ✗ Error esperado: {e}")
    # Verificar que tiene causa encadenada
    if e.__cause__:
        print(f"    Causa original: {e.__cause__}")
    registrar_log(f"OP7 - ERROR RESERVA NO DISPONIBLE: {e}")
finally:
    print("  → OP7 finalizada")

# -----------------------------------------------------------------------
# OPERACIÓN 8: Cancelar una reserva y luego intentar pagarla
# -----------------------------------------------------------------------
print("\n[OP 8] Cancelar reserva y luego intentar pagar")
try:
    reserva2 = Reserva(cliente2, equipo1, "2026-05-25", 3)
    reservas.append(reserva2)
    reserva2.confirmar()
    reserva2.cancelar()
    registrar_log("OP8 - Reserva cancelada")
    # Intentar pagar después de cancelar
    reserva2.procesar_pago()
except ReservaError as e:
    print(f"  ✗ {e}")
    registrar_log(f"OP8 - ERROR reserva: {e}")
except PagoError as e:
    print(f"  ✗ Error de pago esperado: {e}")
    registrar_log(f"OP8 - ERROR PAGO CANCELADA: {e}")
else:
    print("  ✓ Operación completada")
finally:
    print("  → OP8 finalizada")

# -----------------------------------------------------------------------
# OPERACIÓN 9: Reserva con fecha en formato incorrecto
# -----------------------------------------------------------------------
print("\n[OP 9] Crear reserva con fecha inválida")
try:
    reserva_fecha_mal = Reserva(cliente1, asesoria1, "20-05-2026", 2)
except ReservaError as e:
    print(f"  ✗ Error esperado: {e}")
    if e.__cause__:
        print(f"    Causa (ValueError): {type(e.__cause__).__name__}")
    registrar_log(f"OP9 - ERROR FECHA RESERVA: {e}")
finally:
    print("  → OP9 finalizada")

# -----------------------------------------------------------------------
# OPERACIÓN 10: Reserva de asesoría con descuento del 10%
# -----------------------------------------------------------------------
print("\n[OP 10] Reservar asesoría con descuento del 10%")
try:
    reserva3 = Reserva(cliente2, asesoria1, "2026-06-10", 2)
    reservas.append(reserva3)
    reserva3.confirmar()
    # Calcular con descuento del 10% e impuesto del 19%
    costo_final = reserva3.obtener_costo_total(descuento=0.10, impuesto=0.19)
    registrar_log(f"OP10 - Asesoría reservada con descuento. Costo: ${costo_final}")
except (ReservaError, ServicioError) as e:
    registrar_log(f"OP10 - ERROR: {e}")
else:
    print(f"  ✓ Asesoría reservada exitosamente")
    print(f"  ✓ Costo con 10% descuento + 19% IVA: ${costo_final}")
finally:
    print("  → OP10 finalizada")

print("\n" + "="*60)
print("   SIMULACIÓN COMPLETADA")
print("="*60 + "\n")


# =============================================================================
# INTERFAZ GRÁFICA (TKINTER)
# =============================================================================

# -------------------------
# Variable ventanas globales
# -------------------------
ventana_cliente = None
ventana_sala = None
ventana_equipo = None      # variable para ventana de equipo
ventana_asesoria = None    # variable para ventana de asesoría
ventana_reservas = None    # variable para ventana ver reservas


# =============================================================================
# FUNCIÓN: ABRIR VENTANA CLIENTES
# =============================================================================

def abrir_clientes():
    """[SIN CAMBIOS] Abre la ventana de registro de clientes."""
    global ventana_cliente

    if ventana_cliente is not None:
        ventana_cliente.lift()
        return

    ventana_cliente = tk.Toplevel()
    ventana_cliente.title("Añadir Cliente")
    ventana_cliente.geometry("500x500")
    ventana_cliente.config(bg="#1f1f1f")

    def cerrar_ventana():
        global ventana_cliente
        ventana_cliente.destroy()
        ventana_cliente = None

    ventana_cliente.protocol("WM_DELETE_WINDOW", cerrar_ventana)

    titulo = tk.Label(
        ventana_cliente,
        text="Registro de Clientes",
        font=("Arial", 22, "bold"),
        bg="#1f1f1f",
        fg="white"
    )
    titulo.pack(pady=20)

    frame = tk.Frame(ventana_cliente, bg="#2f2f2f", padx=20, pady=20)
    frame.pack(pady=10)

    # Nombre
    tk.Label(frame, text="Nombre", font=("Arial", 12), bg="#2f2f2f", fg="white").pack(anchor="w")
    entry_nombre = tk.Entry(frame, width=35, font=("Arial", 12))
    entry_nombre.pack(pady=5)

    # Documento
    tk.Label(frame, text="Documento", font=("Arial", 12), bg="#2f2f2f", fg="white").pack(anchor="w")
    entry_documento = tk.Entry(frame, width=35, font=("Arial", 12))
    entry_documento.pack(pady=5)

    # Correo
    tk.Label(frame, text="Correo", font=("Arial", 12), bg="#2f2f2f", fg="white").pack(anchor="w")
    entry_correo = tk.Entry(frame, width=35, font=("Arial", 12))
    entry_correo.pack(pady=5)

    # Teléfono
    tk.Label(frame, text="Teléfono", font=("Arial", 12), bg="#2f2f2f", fg="white").pack(anchor="w")
    entry_telefono = tk.Entry(frame, width=35, font=("Arial", 12))
    entry_telefono.pack(pady=5)

    def guardar_cliente():
        nombre = entry_nombre.get()
        documento = entry_documento.get()
        correo = entry_correo.get()
        telefono = entry_telefono.get()

        try:
            cliente = Cliente(nombre, documento, correo, telefono)
            clientes.append(cliente)
            registrar_log(f"GUI - Cliente registrado: {nombre}")
            messagebox.showinfo("Éxito", "Cliente registrado correctamente")
            entry_nombre.delete(0, tk.END)
            entry_documento.delete(0, tk.END)
            entry_correo.delete(0, tk.END)
            entry_telefono.delete(0, tk.END)
        except ClienteError as e:
            messagebox.showerror("Error", str(e))
            registrar_log(f"GUI - ERROR CLIENTE: {e}")

    tk.Button(
        ventana_cliente,
        text="Guardar Cliente",
        font=("Arial", 12, "bold"),
        bg="#8ec5e8",
        fg="black",
        width=20,
        height=2,
        bd=0,
        cursor="hand2",
        command=guardar_cliente
    ).pack(pady=20)


# =============================================================================
# FUNCIÓN: RESERVAR SALA
# =============================================================================

def reservar_sala():
    """[SIN CAMBIOS] Abre la ventana de reserva de salas."""
    global ventana_sala

    if ventana_sala is not None:
        ventana_sala.lift()
        return

    ventana_sala = tk.Toplevel()
    ventana_sala.title("Reservar Sala")
    ventana_sala.geometry("550x700")
    ventana_sala.config(bg="#1f1f1f")

    def cerrar_ventana():
        global ventana_sala
        ventana_sala.destroy()
        ventana_sala = None

    ventana_sala.protocol("WM_DELETE_WINDOW", cerrar_ventana)

    tk.Label(
        ventana_sala,
        text="Reservar Sala",
        font=("Arial", 24, "bold"),
        bg="#1f1f1f",
        fg="white"
    ).pack(pady=20)

    frame = tk.Frame(ventana_sala, bg="#2f2f2f", padx=20, pady=20)
    frame.pack(pady=10)

    # Cliente
    tk.Label(frame, text="Cliente", font=("Arial", 12), bg="#2f2f2f", fg="white").pack(anchor="w")
    nombres_clientes = [c.nombre for c in clientes] if clientes else ["No hay clientes"]
    cliente_var = tk.StringVar(value=nombres_clientes[0])
    menu_clientes = tk.OptionMenu(frame, cliente_var, *nombres_clientes)
    menu_clientes.config(width=30, bg="#8ec5e8")
    menu_clientes.pack(pady=5)

    # Sala
    tk.Label(frame, text="Sala Disponible", font=("Arial", 12), bg="#2f2f2f", fg="white").pack(anchor="w", pady=(15, 0))
    salas_disponibles = [
        f"{s.nombre} - {s.tipo_sala}"
        for s in servicios
        if isinstance(s, ReservarSala) and s.disponible
    ]
    if not salas_disponibles:
        salas_disponibles = ["No hay salas disponibles"]
    sala_var = tk.StringVar(value=salas_disponibles[0])
    menu_sala = tk.OptionMenu(frame, sala_var, *salas_disponibles)
    menu_sala.config(width=30, bg="#8ec5e8")
    menu_sala.pack(pady=5)

    # Fecha
    tk.Label(frame, text="Fecha (YYYY-MM-DD)", font=("Arial", 12), bg="#2f2f2f", fg="white").pack(anchor="w", pady=(15, 0))
    entry_fecha = tk.Entry(frame, width=35, font=("Arial", 12))
    entry_fecha.pack(pady=5)

    # Duración
    tk.Label(frame, text="Duración (horas)", font=("Arial", 12), bg="#2f2f2f", fg="white").pack(anchor="w", pady=(15, 0))
    entry_duracion = tk.Entry(frame, width=35, font=("Arial", 12))
    entry_duracion.pack(pady=5)

    resultado = tk.Text(ventana_sala, width=55, height=10, bg="#111111", fg="lime", font=("Consolas", 10))
    resultado.pack(pady=20)

    def crear_reserva_sala():
        try:
            if not clientes:
                raise ReservaError("No hay clientes registrados")

            nombre_cliente = cliente_var.get()
            cliente_seleccionado = next((c for c in clientes if c.nombre == nombre_cliente), None)
            if cliente_seleccionado is None:
                raise ReservaError("Cliente no encontrado")

            sala_str = sala_var.get()
            servicio_seleccionado = next(
                (s for s in servicios if isinstance(s, ReservarSala) and f"{s.nombre} - {s.tipo_sala}" == sala_str),
                None
            )
            if servicio_seleccionado is None:
                raise ReservaError("Sala no encontrada")

            fecha_str = entry_fecha.get().strip()
            duracion_str = entry_duracion.get().strip()

            if not fecha_str:
                raise ReservaError("Ingrese una fecha")
            if not duracion_str:
                raise ReservaError("Ingrese la duración")

            try:
                duracion = float(duracion_str)
            except ValueError:
                raise ReservaError("Duración debe ser un número")

            if duracion <= 0:
                raise ReservaError("La duración debe ser mayor a 0")

            reserva = Reserva(cliente_seleccionado, servicio_seleccionado, fecha_str, duracion)
            reserva.confirmar()
            reservas.append(reserva)
            registrar_log(f"GUI - Reserva de sala creada para {cliente_seleccionado.nombre}")

            costo_total = reserva.obtener_costo_total()
            resultado.delete("1.0", tk.END)
            resultado.insert(tk.END,
                f"RESERVA CONFIRMADA\n\n"
                f"Cliente: {reserva.cliente.nombre}\n"
                f"Sala: {reserva.servicio.nombre} - {reserva.servicio.tipo_sala}\n"
                f"Fecha: {reserva.fecha.strftime('%Y-%m-%d')}\n"
                f"Duración: {reserva.duracion} horas\n"
                f"Costo Total: ${costo_total:.2f}\n"
                f"Estado: {reserva.estado}"
            )
            messagebox.showinfo("Éxito", "Reserva creada y confirmada correctamente")
            entry_fecha.delete(0, tk.END)
            entry_duracion.delete(0, tk.END)

        except ReservaError as e:
            messagebox.showerror("Error", str(e))
            registrar_log(f"GUI - ERROR RESERVA SALA: {e}")
        except Exception as e:
            messagebox.showerror("Error", f"Error inesperado: {str(e)}")
            registrar_log(f"GUI - ERROR INESPERADO SALA: {e}")

    tk.Button(
        ventana_sala,
        text="Crear Reserva",
        font=("Arial", 12, "bold"),
        bg="#8ec5e8",
        fg="black",
        width=20,
        height=2,
        bd=0,
        cursor="hand2",
        command=crear_reserva_sala
    ).pack(pady=10)


# =============================================================================
# FUNCIÓN: ALQUILAR EQUIPO
# =============================================================================

def alquilar_equipo():
    """
    AGREGADO: Ventana completa para alquiler de equipos.
    Antes esta función solo mostraba un messagebox con 'Aquí irá el sistema...'.
    Ahora implementa el flujo completo: selección de cliente, equipo,
    fecha, duración y creación de la reserva con manejo de excepciones.
    """
    global ventana_equipo

    if ventana_equipo is not None:
        ventana_equipo.lift()
        return

    ventana_equipo = tk.Toplevel()
    ventana_equipo.title("Alquilar Equipo")
    ventana_equipo.geometry("550x700")
    ventana_equipo.config(bg="#1f1f1f")

    def cerrar_ventana():
        global ventana_equipo
        ventana_equipo.destroy()
        ventana_equipo = None

    ventana_equipo.protocol("WM_DELETE_WINDOW", cerrar_ventana)

    tk.Label(
        ventana_equipo,
        text="Alquilar Equipo",
        font=("Arial", 24, "bold"),
        bg="#1f1f1f",
        fg="white"
    ).pack(pady=20)

    frame = tk.Frame(ventana_equipo, bg="#2f2f2f", padx=20, pady=20)
    frame.pack(pady=10)

    # Cliente
    tk.Label(frame, text="Cliente", font=("Arial", 12), bg="#2f2f2f", fg="white").pack(anchor="w")
    nombres_clientes = [c.nombre for c in clientes] if clientes else ["No hay clientes"]
    cliente_var = tk.StringVar(value=nombres_clientes[0])
    menu_clientes = tk.OptionMenu(frame, cliente_var, *nombres_clientes)
    menu_clientes.config(width=30, bg="#8ec5e8")
    menu_clientes.pack(pady=5)

    # Equipo
    tk.Label(frame, text="Equipo Disponible", font=("Arial", 12), bg="#2f2f2f", fg="white").pack(anchor="w", pady=(15, 0))
    equipos_disponibles = [
        f"{s.nombre} - {s.tipo_equipo}"
        for s in servicios
        if isinstance(s, AlquilerEquipo) and s.disponible
    ]
    if not equipos_disponibles:
        equipos_disponibles = ["No hay equipos disponibles"]
    equipo_var = tk.StringVar(value=equipos_disponibles[0])
    menu_equipo = tk.OptionMenu(frame, equipo_var, *equipos_disponibles)
    menu_equipo.config(width=30, bg="#8ec5e8")
    menu_equipo.pack(pady=5)

    # Fecha
    tk.Label(frame, text="Fecha (YYYY-MM-DD)", font=("Arial", 12), bg="#2f2f2f", fg="white").pack(anchor="w", pady=(15, 0))
    entry_fecha = tk.Entry(frame, width=35, font=("Arial", 12))
    entry_fecha.pack(pady=5)

    # Días de alquiler
    tk.Label(frame, text="Días de alquiler", font=("Arial", 12), bg="#2f2f2f", fg="white").pack(anchor="w", pady=(15, 0))
    entry_dias = tk.Entry(frame, width=35, font=("Arial", 12))
    entry_dias.pack(pady=5)

    resultado = tk.Text(ventana_equipo, width=55, height=10, bg="#111111", fg="lime", font=("Consolas", 10))
    resultado.pack(pady=20)

    def crear_reserva_equipo():
        try:
            if not clientes:
                raise ReservaError("No hay clientes registrados")

            nombre_cliente = cliente_var.get()
            cliente_seleccionado = next((c for c in clientes if c.nombre == nombre_cliente), None)
            if cliente_seleccionado is None:
                raise ReservaError("Cliente no encontrado")

            equipo_str = equipo_var.get()
            servicio_seleccionado = next(
                (s for s in servicios if isinstance(s, AlquilerEquipo) and f"{s.nombre} - {s.tipo_equipo}" == equipo_str),
                None
            )
            if servicio_seleccionado is None:
                raise ReservaError("Equipo no encontrado")

            fecha_str = entry_fecha.get().strip()
            dias_str = entry_dias.get().strip()

            if not fecha_str:
                raise ReservaError("Ingrese una fecha")
            if not dias_str:
                raise ReservaError("Ingrese los días de alquiler")

            try:
                dias = float(dias_str)
            except ValueError:
                raise ReservaError("Los días deben ser un número")

            if dias <= 0:
                raise ReservaError("Los días deben ser mayores a 0")

            reserva = Reserva(cliente_seleccionado, servicio_seleccionado, fecha_str, dias)
            reserva.confirmar()
            reservas.append(reserva)
            registrar_log(f"GUI - Reserva de equipo creada para {cliente_seleccionado.nombre}")

            costo_total = reserva.obtener_costo_total()
            garantia_txt = "Sí" if servicio_seleccionado.garantia else "No"
            resultado.delete("1.0", tk.END)
            resultado.insert(tk.END,
                f"ALQUILER CONFIRMADO\n\n"
                f"Cliente: {reserva.cliente.nombre}\n"
                f"Equipo: {servicio_seleccionado.nombre} ({servicio_seleccionado.tipo_equipo})\n"
                f"Garantía incluida: {garantia_txt}\n"
                f"Fecha: {reserva.fecha.strftime('%Y-%m-%d')}\n"
                f"Días: {reserva.duracion}\n"
                f"Costo Total: ${costo_total:.2f}\n"
                f"Estado: {reserva.estado}"
            )
            messagebox.showinfo("Éxito", "Alquiler creado y confirmado correctamente")
            entry_fecha.delete(0, tk.END)
            entry_dias.delete(0, tk.END)

        except ReservaError as e:
            messagebox.showerror("Error", str(e))
            registrar_log(f"GUI - ERROR RESERVA EQUIPO: {e}")
        except Exception as e:
            messagebox.showerror("Error", f"Error inesperado: {str(e)}")
            registrar_log(f"GUI - ERROR INESPERADO EQUIPO: {e}")

    tk.Button(
        ventana_equipo,
        text="Confirmar Alquiler",
        font=("Arial", 12, "bold"),
        bg="#8ec5e8",
        fg="black",
        width=20,
        height=2,
        bd=0,
        cursor="hand2",
        command=crear_reserva_equipo
    ).pack(pady=10)


# =============================================================================
# FUNCIÓN: RESERVAR ASESORÍA
# =============================================================================

def reservar_asesoria():
    """
    AGREGADO: Ventana completa para reserva de asesorías.
    Antes esta función solo mostraba 'Aquí irá el sistema de asesorías'.
    Ahora implementa flujo completo con selección de cliente, asesoría,
    fecha, duración, descuento e impuesto opcionales.
    """
    global ventana_asesoria

    if ventana_asesoria is not None:
        ventana_asesoria.lift()
        return

    ventana_asesoria = tk.Toplevel()
    ventana_asesoria.title("Reservar Asesoría")
    ventana_asesoria.geometry("560x750")
    ventana_asesoria.config(bg="#1f1f1f")

    def cerrar_ventana():
        global ventana_asesoria
        ventana_asesoria.destroy()
        ventana_asesoria = None

    ventana_asesoria.protocol("WM_DELETE_WINDOW", cerrar_ventana)

    tk.Label(
        ventana_asesoria,
        text="Reservar Asesoría",
        font=("Arial", 24, "bold"),
        bg="#1f1f1f",
        fg="white"
    ).pack(pady=20)

    frame = tk.Frame(ventana_asesoria, bg="#2f2f2f", padx=20, pady=20)
    frame.pack(pady=10)

    # Cliente
    tk.Label(frame, text="Cliente", font=("Arial", 12), bg="#2f2f2f", fg="white").pack(anchor="w")
    nombres_clientes = [c.nombre for c in clientes] if clientes else ["No hay clientes"]
    cliente_var = tk.StringVar(value=nombres_clientes[0])
    menu_clientes = tk.OptionMenu(frame, cliente_var, *nombres_clientes)
    menu_clientes.config(width=30, bg="#8ec5e8")
    menu_clientes.pack(pady=5)

    # Asesoría
    tk.Label(frame, text="Asesoría Disponible", font=("Arial", 12), bg="#2f2f2f", fg="white").pack(anchor="w", pady=(15, 0))
    asesorias_disponibles = [
        f"{s.nombre} - {s.tema}"
        for s in servicios
        if isinstance(s, Asesoria) and s.disponible
    ]
    if not asesorias_disponibles:
        asesorias_disponibles = ["No hay asesorías disponibles"]
    asesoria_var = tk.StringVar(value=asesorias_disponibles[0])
    menu_asesoria = tk.OptionMenu(frame, asesoria_var, *asesorias_disponibles)
    menu_asesoria.config(width=30, bg="#8ec5e8")
    menu_asesoria.pack(pady=5)

    # Fecha
    tk.Label(frame, text="Fecha (YYYY-MM-DD)", font=("Arial", 12), bg="#2f2f2f", fg="white").pack(anchor="w", pady=(15, 0))
    entry_fecha = tk.Entry(frame, width=35, font=("Arial", 12))
    entry_fecha.pack(pady=5)

    # Horas
    tk.Label(frame, text="Horas de asesoría", font=("Arial", 12), bg="#2f2f2f", fg="white").pack(anchor="w", pady=(15, 0))
    entry_horas = tk.Entry(frame, width=35, font=("Arial", 12))
    entry_horas.pack(pady=5)

    # Descuento (0 a 1) 
    tk.Label(frame, text="Descuento (0.0 - 1.0, ej: 0.10 = 10%)", font=("Arial", 11), bg="#2f2f2f", fg="#aaaaaa").pack(anchor="w", pady=(15, 0))
    entry_descuento = tk.Entry(frame, width=35, font=("Arial", 12))
    entry_descuento.insert(0, "0")
    entry_descuento.pack(pady=5)

    resultado = tk.Text(ventana_asesoria, width=55, height=10, bg="#111111", fg="lime", font=("Consolas", 10))
    resultado.pack(pady=20)

    def crear_reserva_asesoria():
        try:
            if not clientes:
                raise ReservaError("No hay clientes registrados")

            nombre_cliente = cliente_var.get()
            cliente_seleccionado = next((c for c in clientes if c.nombre == nombre_cliente), None)
            if cliente_seleccionado is None:
                raise ReservaError("Cliente no encontrado")

            asesoria_str = asesoria_var.get()
            servicio_seleccionado = next(
                (s for s in servicios if isinstance(s, Asesoria) and f"{s.nombre} - {s.tema}" == asesoria_str),
                None
            )
            if servicio_seleccionado is None:
                raise ReservaError("Asesoría no encontrada")

            fecha_str = entry_fecha.get().strip()
            horas_str = entry_horas.get().strip()
            descuento_str = entry_descuento.get().strip()

            if not fecha_str:
                raise ReservaError("Ingrese una fecha")
            if not horas_str:
                raise ReservaError("Ingrese las horas")

            try:
                horas = float(horas_str)
            except ValueError:
                raise ReservaError("Las horas deben ser un número")

            try:
                descuento = float(descuento_str) if descuento_str else 0.0
                if not (0 <= descuento <= 1):
                    raise ValueError("Descuento fuera de rango")
            except ValueError:
                raise ReservaError("Descuento inválido (use valor entre 0.0 y 1.0)")

            if horas <= 0:
                raise ReservaError("Las horas deben ser mayores a 0")

            reserva = Reserva(cliente_seleccionado, servicio_seleccionado, fecha_str, horas)
            reserva.confirmar()
            reservas.append(reserva)

            # Calcular con descuento e IVA 19% 
            costo_sin_desc = reserva.obtener_costo_total()
            costo_con_desc = reserva.obtener_costo_total(descuento=descuento, impuesto=0.19)
            registrar_log(f"GUI - Asesoría reservada para {cliente_seleccionado.nombre}. Costo: ${costo_con_desc}")

            resultado.delete("1.0", tk.END)
            resultado.insert(tk.END,
                f"ASESORÍA CONFIRMADA\n\n"
                f"Cliente: {reserva.cliente.nombre}\n"
                f"Asesoría: {servicio_seleccionado.nombre}\n"
                f"Especialista: {servicio_seleccionado.especialista}\n"
                f"Tema: {servicio_seleccionado.tema}\n"
                f"Fecha: {reserva.fecha.strftime('%Y-%m-%d')}\n"
                f"Horas: {reserva.duracion}\n"
                f"Costo base: ${costo_sin_desc:.2f}\n"
                f"Descuento: {int(descuento*100)}% | IVA: 19%\n"
                f"Costo final: ${costo_con_desc:.2f}\n"
                f"Estado: {reserva.estado}"
            )
            messagebox.showinfo("Éxito", "Asesoría reservada y confirmada correctamente")
            entry_fecha.delete(0, tk.END)
            entry_horas.delete(0, tk.END)

        except ReservaError as e:
            messagebox.showerror("Error", str(e))
            registrar_log(f"GUI - ERROR RESERVA ASESORIA: {e}")
        except Exception as e:
            messagebox.showerror("Error", f"Error inesperado: {str(e)}")
            registrar_log(f"GUI - ERROR INESPERADO ASESORIA: {e}")

    tk.Button(
        ventana_asesoria,
        text="Confirmar Asesoría",
        font=("Arial", 12, "bold"),
        bg="#8ec5e8",
        fg="black",
        width=20,
        height=2,
        bd=0,
        cursor="hand2",
        command=crear_reserva_asesoria
    ).pack(pady=10)


# =============================================================================
# FUNCIÓN: VER RESERVAS
# =============================================================================

def ver_reservas():
    """
    AGREGADO: Ventana para ver todas las reservas del sistema y cancelarlas.
    Muestra una tabla con cliente, servicio, fecha, costo y estado.
    Permite seleccionar una reserva y cancelarla desde la interfaz.
    """
    global ventana_reservas

    if ventana_reservas is not None:
        ventana_reservas.lift()
        return

    ventana_reservas = tk.Toplevel()
    ventana_reservas.title("Ver Reservas")
    ventana_reservas.geometry("750x500")
    ventana_reservas.config(bg="#1f1f1f")

    def cerrar_ventana():
        global ventana_reservas
        ventana_reservas.destroy()
        ventana_reservas = None

    ventana_reservas.protocol("WM_DELETE_WINDOW", cerrar_ventana)

    tk.Label(
        ventana_reservas,
        text="Reservas del Sistema",
        font=("Arial", 20, "bold"),
        bg="#1f1f1f",
        fg="white"
    ).pack(pady=15)

    # Tabla de reservas con Treeview
    columnas = ("Cliente", "Servicio", "Fecha", "Duración", "Costo", "Estado")
    tree = ttk.Treeview(ventana_reservas, columns=columnas, show="headings", height=12)

    for col in columnas:
        tree.heading(col, text=col)
        tree.column(col, width=110, anchor="center")

    tree.pack(padx=20, pady=10, fill="both", expand=True)

    def cargar_reservas():
        """Recarga la tabla con las reservas actuales."""
        tree.delete(*tree.get_children())
        if not reservas:
            tree.insert("", "end", values=("Sin reservas", "-", "-", "-", "-", "-"))
            return
        for r in reservas:
            try:
                costo = r.obtener_costo_total()
                tree.insert("", "end", values=(
                    r.cliente.nombre,
                    r.servicio.nombre,
                    r.fecha.strftime("%Y-%m-%d"),
                    f"{r.duracion}h",
                    f"${costo:.2f}",
                    r.estado
                ))
            except Exception as e:
                registrar_log(f"GUI - ERROR mostrando reserva: {e}")

    cargar_reservas()

    def cancelar_seleccionada():
        """Cancela la reserva seleccionada en la tabla."""
        seleccion = tree.selection()
        if not seleccion:
            messagebox.showwarning("Advertencia", "Seleccione una reserva para cancelar")
            return

        idx = tree.index(seleccion[0])
        try:
            reserva = reservas[idx]
            mensaje = reserva.cancelar()
            messagebox.showinfo("Éxito", mensaje)
            registrar_log(f"GUI - Reserva cancelada para {reserva.cliente.nombre}")
            cargar_reservas()
        except ReservaError as e:
            messagebox.showerror("Error", str(e))
            registrar_log(f"GUI - ERROR CANCELAR RESERVA: {e}")

    frame_botones = tk.Frame(ventana_reservas, bg="#1f1f1f")
    frame_botones.pack(pady=10)

    tk.Button(
        frame_botones,
        text="Cancelar Reserva Seleccionada",
        font=("Arial", 11, "bold"),
        bg="#e87b8e",
        fg="black",
        width=25,
        height=2,
        bd=0,
        cursor="hand2",
        command=cancelar_seleccionada
    ).pack(side="left", padx=10)

    tk.Button(
        frame_botones,
        text="Actualizar Lista",
        font=("Arial", 11),
        bg="#8ec5e8",
        fg="black",
        width=15,
        height=2,
        bd=0,
        cursor="hand2",
        command=cargar_reservas
    ).pack(side="left", padx=10)


# =============================================================================
# VENTANA PRINCIPAL
# =============================================================================

ventana = tk.Tk()
ventana.title("Sistema de Reservas - Software FJ")
ventana.geometry("820x780")
ventana.config(bg="#1f1f1f")

# Título
tk.Label(
    ventana,
    text="Sistema de Reservas - Software FJ",
    font=("Arial", 30, "bold"),
    bg="#1f1f1f",
    fg="white"
).pack(pady=20)

# Frame principal
frame_menu = tk.Frame(ventana, bg="#505050", width=520, height=520)
frame_menu.pack(pady=10)
frame_menu.pack_propagate(False)

# Texto menú
tk.Label(
    frame_menu,
    text="Menu",
    font=("Arial", 28),
    bg="#505050",
    fg="white"
).pack(pady=20)

# Estilo botones 
estilo_boton = {
    "font": ("Arial", 14),
    "bg": "#63c3fa",
    "fg": "black",
    "width": 18,
    "height": 2,
    "bd": 0,
    "cursor": "hand2"
}

# Botón añadir cliente 
tk.Button(frame_menu, text="Añadir Cliente", command=abrir_clientes, **estilo_boton).pack(pady=10)

# Botón reservar sala 
tk.Button(frame_menu, text="Reservar Sala", command=reservar_sala, **estilo_boton).pack(pady=10)

# Botón alquilar equipo 
tk.Button(frame_menu, text="Alquilar Equipo", command=alquilar_equipo, **estilo_boton).pack(pady=10)

# Botón asesoría 
tk.Button(frame_menu, text="Reservar Asesoría", command=reservar_asesoria, **estilo_boton).pack(pady=10)

# Botón ver reservas 
tk.Button(
    frame_menu,
    text="Ver Reservas",
    command=ver_reservas,
    font=("Arial", 14),
    bg="#a3e4a0",
    fg="black",
    width=18,
    height=2,
    bd=0,
    cursor="hand2"
).pack(pady=10)

# Footer 
tk.Label(
    ventana,
    text="Creado por: Juan Miguel Salcedo Fulanoito perez",
    font=("Arial", 14),
    bg="#1f1f1f",
    fg="white"
).pack(pady=30)

# Ejecutar 
ventana.mainloop()
