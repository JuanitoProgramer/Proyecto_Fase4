# Sistema Integral de Gestión de Clientes, Servicios y Reservas

# -------------------------
# Importaciones
# -------------------------
import tkinter as tk
from tkinter import messagebox

import os
import re
import abc
from datetime import datetime
from pathlib import Path


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
    pass


class ServicioError(Exception):
    pass


class ReservaError(Exception):
    pass


class PagoError(Exception):
    pass


# -------------------------
# Clase Cliente
# -------------------------
class Cliente:
    def __init__(self, nombre, documento, correo, telefono):

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

        self.__nombre = nombre
        self.__documento = documento
        self.__correo = correo
        self.__telefono = telefono

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


# -------------------------
# Clase abstracta Servicio
# -------------------------
class Servicio(abc.ABC):

    def __init__(self, nombre, costo_base, disponible, codigo, descripcion):

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

        self.__nombre = nombre
        self.__costo_base = costo_base
        self.__disponible = disponible
        self.__codigo = codigo
        self.__descripcion = descripcion

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

    @abc.abstractmethod
    def calcular_costo(self, descuento=0, impuesto=0):
        pass

    @abc.abstractmethod
    def mostrar_descripcion(self):
        pass

    @abc.abstractmethod
    def validar_disponibilidad(self):
        pass


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

        costo = self.horas * self.costo_base

        costo -= costo * descuento
        costo += costo * impuesto

        return costo

    def mostrar_descripcion(self):
        return f"Sala: {self.nombre} - Tipo: {self.tipo_sala}"

    def validar_disponibilidad(self):
        return self.disponible


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

        costo = self.dias * self.costo_base

        costo -= costo * descuento
        costo += costo * impuesto

        return costo

    def mostrar_descripcion(self):
        return f"Equipo: {self.nombre} - Tipo: {self.tipo_equipo}"

    def validar_disponibilidad(self):
        return self.disponible


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

        costo = self.horas * self.costo_base

        costo -= costo * descuento
        costo += costo * impuesto

        return costo

    def mostrar_descripcion(self):
        return f"Asesoría: {self.nombre} - Tema: {self.tema}"

    def validar_disponibilidad(self):
        return self.disponible


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
            raise ReservaError("Formato de fecha incorrecto") from e

        if not isinstance(duracion, (int, float)) or duracion <= 0:
            raise ReservaError("Duración inválida")

        self.cliente = cliente
        self.servicio = servicio
        self.duracion = duracion
        self.estado = estado

    def confirmar(self):

        if not self.servicio.validar_disponibilidad():
            raise ReservaError("Servicio no disponible")

        self.estado = "activo"

        return "Reserva confirmada"

    def cancelar(self):

        if self.estado == "cancelado":
            raise ReservaError("La reserva ya está cancelada")

        self.estado = "cancelado"

        return "Reserva cancelada"

    def obtener_costo_total(self):
        return self.servicio.calcular_costo()

    def mostrar_detalles(self):

        return (
            f"Cliente: {self.cliente.nombre}\n"
            f"Servicio: {self.servicio.nombre}\n"
            f"Fecha: {self.fecha.strftime('%Y-%m-%d')}\n"
            f"Estado: {self.estado}"
        )

    def procesar_pago(self):

        if self.estado == "cancelado":
            raise PagoError("No se puede pagar una reserva cancelada")

        total = self.obtener_costo_total()

        return f"Pago procesado correctamente. Total: ${total}"


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

    cliente1 = Cliente("Juan Miguel", "12345678", "juan@gmail.com", "3001234567")

    clientes.append(cliente1)

    registrar_log("Cliente registrado correctamente")

except Exception as e:

    registrar_log(f"ERROR CLIENTE: {e}")

finally:

    print("Proceso cliente finalizado")

try:

    sala1 = ReservarSala("Sala VIP", 50000, True, "SV01", "Sala premium", 20, "VIP", 2)

    servicios.append(sala1)

    registrar_log("Servicio Sala registrado")

except Exception as e:

    registrar_log(f"ERROR SERVICIO: {e}")

finally:

    print("Proceso servicio finalizado")

try:

    reserva1 = Reserva(cliente1, sala1, "2026-05-20", 2)

    reservas.append(reserva1)

    print(reserva1.confirmar())

    print(reserva1.mostrar_detalles())

    print(reserva1.procesar_pago())

    registrar_log("Reserva creada correctamente")

except Exception as e:

    registrar_log(f"ERROR RESERVA: {e}")

finally:

    print("Proceso reserva finalizado")

# -------------------------
# Error intencional
# -------------------------
try:

    cliente_error = Cliente("", "12", "correo_malo", "123")

except Exception as e:
    print(f"ERROR Intencional: {e}")
    registrar_log(f"ERROR INTENCIONAL: {e}")

finally:

    print("Prueba de error finalizada")


# Tkinter

import tkinter as tk
from tkinter import messagebox

# -------------------------
# Funciones botones
# -------------------------

# -------------------------
# Variable ventana
# -------------------------

ventana_cliente = None

# -------------------------
# Función abrir ventana
# -------------------------

def abrir_clientes():

    global ventana_cliente

    # Si ya existe
    if ventana_cliente is not None:
        ventana_cliente.lift()
        return

    # Crear ventana
    ventana_cliente = tk.Toplevel()

    ventana_cliente.title("Añadir Cliente")
    ventana_cliente.geometry("500x500")
    ventana_cliente.config(bg="#1f1f1f")

    # -------------------------
    # Función cerrar ventana
    # -------------------------

    def cerrar_ventana():
        global ventana_cliente
        ventana_cliente.destroy()
        ventana_cliente = None

    ventana_cliente.protocol(
        "WM_DELETE_WINDOW",
        cerrar_ventana
    )

    # -------------------------
    # Título
    # -------------------------

    titulo = tk.Label(
        ventana_cliente,
        text="Registro de Clientes",
        font=("Arial", 22, "bold"),
        bg="#1f1f1f",
        fg="white"
    )

    titulo.pack(pady=20)

    # -------------------------
    # Frame formulario
    # -------------------------

    frame = tk.Frame(
        ventana_cliente,
        bg="#2f2f2f",
        padx=20,
        pady=20
    )

    frame.pack(pady=10)

    # -------------------------
    # Nombre
    # -------------------------

    label_nombre = tk.Label(
        frame,
        text="Nombre",
        font=("Arial", 12),
        bg="#2f2f2f",
        fg="white"
    )

    label_nombre.pack(anchor="w")

    entry_nombre = tk.Entry(
        frame,
        width=35,
        font=("Arial", 12)
    )

    entry_nombre.pack(pady=5)

    # -------------------------
    # Documento
    # -------------------------

    label_documento = tk.Label(
        frame,
        text="Documento",
        font=("Arial", 12),
        bg="#2f2f2f",
        fg="white"
    )

    label_documento.pack(anchor="w")

    entry_documento = tk.Entry(
        frame,
        width=35,
        font=("Arial", 12)
    )

    entry_documento.pack(pady=5)

    # -------------------------
    # Correo
    # -------------------------

    label_correo = tk.Label(
        frame,
        text="Correo",
        font=("Arial", 12),
        bg="#2f2f2f",
        fg="white"
    )

    label_correo.pack(anchor="w")

    entry_correo = tk.Entry(
        frame,
        width=35,
        font=("Arial", 12)
    )

    entry_correo.pack(pady=5)

    # -------------------------
    # Teléfono
    # -------------------------

    label_telefono = tk.Label(
        frame,
        text="Teléfono",
        font=("Arial", 12),
        bg="#2f2f2f",
        fg="white"
    )

    label_telefono.pack(anchor="w")

    entry_telefono = tk.Entry(
        frame,
        width=35,
        font=("Arial", 12)
    )

    entry_telefono.pack(pady=5)

    # -------------------------
    # Función guardar
    # -------------------------

    def guardar_cliente():

        nombre = entry_nombre.get()
        documento = entry_documento.get()
        correo = entry_correo.get()
        telefono = entry_telefono.get()

        try:
            cliente = Cliente(nombre, documento, correo, telefono)
            clientes.append(cliente)
            registrar_log("Cliente registrado correctamente")
            messagebox.showinfo(
                "Éxito",
                "Cliente registrado correctamente"
            )
            # Limpiar campos
            entry_nombre.delete(0, tk.END)
            entry_documento.delete(0, tk.END)
            entry_correo.delete(0, tk.END)
            entry_telefono.delete(0, tk.END)
        except ClienteError as e:
            messagebox.showerror("Error", str(e))
            registrar_log(f"ERROR CLIENTE: {e}")
            return

    # -------------------------
    # Botón guardar
    # -------------------------

    boton_guardar = tk.Button(
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
    )

    boton_guardar.pack(pady=20)

# -------------------------
# Variable ventana sala
# -------------------------

ventana_sala = None

# -------------------------
# Función reservar sala
# -------------------------

def reservar_sala():

    global ventana_sala

    # Evitar múltiples ventanas
    if ventana_sala is not None:
        ventana_sala.lift()
        return

    # -------------------------
    # Crear ventana
    # -------------------------

    ventana_sala = tk.Toplevel()

    ventana_sala.title("Reservar Sala")
    ventana_sala.geometry("550x650")
    ventana_sala.config(bg="#1f1f1f")

    # -------------------------
    # Cerrar ventana
    # -------------------------

    def cerrar_ventana():

        global ventana_sala

        ventana_sala.destroy()
        ventana_sala = None

    ventana_sala.protocol(
        "WM_DELETE_WINDOW",
        cerrar_ventana
    )

    # -------------------------
    # Título
    # -------------------------

    titulo = tk.Label(
        ventana_sala,
        text="Reservar Sala",
        font=("Arial", 24, "bold"),
        bg="#1f1f1f",
        fg="white"
    )

    titulo.pack(pady=20)

    # -------------------------
    # Frame formulario
    # -------------------------

    frame = tk.Frame(
        ventana_sala,
        bg="#2f2f2f",
        padx=20,
        pady=20
    )

    frame.pack(pady=10)

    # -------------------------
    # Seleccionar cliente
    # -------------------------

    label_cliente = tk.Label(
        frame,
        text="Cliente",
        font=("Arial", 12),
        bg="#2f2f2f",
        fg="white"
    )

    label_cliente.pack(anchor="w")

    # Lista nombres clientes
    nombres_clientes = []

    for cliente in clientes:
        nombres_clientes.append(cliente.nombre)

    # Si no hay clientes
    if len(nombres_clientes) == 0:
        nombres_clientes.append("No hay clientes")

    cliente_var = tk.StringVar()
    cliente_var.set(nombres_clientes[0])

    menu_clientes = tk.OptionMenu(
        frame,
        cliente_var,
        *nombres_clientes
    )

    menu_clientes.config(
        width=30,
        bg="#8ec5e8"
    )

    menu_clientes.pack(pady=5)

    # -------------------------
    # Seleccionar sala
    # -------------------------

    label_sala = tk.Label(
        frame,
        text="Sala Disponible",
        font=("Arial", 12),
        bg="#2f2f2f",
        fg="white"
    )

    label_sala.pack(anchor="w", pady=(15, 0))

    salas_disponibles = []

    for servicio in servicios:
        if isinstance(servicio, ReservarSala) and servicio.disponible:
            salas_disponibles.append(f"{servicio.nombre} - {servicio.tipo_sala}")

    if len(salas_disponibles) == 0:
        salas_disponibles.append("No hay salas disponibles")

    sala_var = tk.StringVar()
    sala_var.set(salas_disponibles[0])

    menu_sala = tk.OptionMenu(
        frame,
        sala_var,
        *salas_disponibles
    )

    menu_sala.config(
        width=30,
        bg="#8ec5e8"
    )

    menu_sala.pack(pady=5)

    # -------------------------
    # Fecha
    # -------------------------

    label_fecha = tk.Label(
        frame,
        text="Fecha (YYYY-MM-DD)",
        font=("Arial", 12),
        bg="#2f2f2f",
        fg="white"
    )

    label_fecha.pack(anchor="w", pady=(15, 0))

    entry_fecha = tk.Entry(
        frame,
        width=35,
        font=("Arial", 12)
    )

    entry_fecha.pack(pady=5)

    # -------------------------
    # Duración (horas)
    # -------------------------

    label_duracion = tk.Label(
        frame,
        text="Duración (horas)",
        font=("Arial", 12),
        bg="#2f2f2f",
        fg="white"
    )

    label_duracion.pack(anchor="w", pady=(15, 0))

    entry_duracion = tk.Entry(
        frame,
        width=35,
        font=("Arial", 12)
    )

    entry_duracion.pack(pady=5)

    # -------------------------
    # Resultado
    # -------------------------

    resultado = tk.Text(
        ventana_sala,
        width=55,
        height=10,
        bg="#111111",
        fg="lime",
        font=("Consolas", 10)
    )

    resultado.pack(pady=20)

    # -------------------------
    # Función crear reserva
    # -------------------------

    def crear_reserva_sala():

        try:

            if len(clientes) == 0:
                raise ReservaError("No hay clientes registrados")

            nombre_cliente = cliente_var.get()

            cliente_seleccionado = None

            for cliente in clientes:
                if cliente.nombre == nombre_cliente:
                    cliente_seleccionado = cliente
                    break

            if cliente_seleccionado is None:
                raise ReservaError("Cliente no encontrado")

            sala_seleccionada_str = sala_var.get()

            servicio_seleccionado = None

            for servicio in servicios:
                if isinstance(servicio, ReservarSala) and f"{servicio.nombre} - {servicio.tipo_sala}" == sala_seleccionada_str:
                    servicio_seleccionado = servicio
                    break

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

            # Crear reserva
            reserva = Reserva(cliente_seleccionado, servicio_seleccionado, fecha_str, duracion)

            # Confirmar reserva
            reserva.confirmar()

            reservas.append(reserva)

            registrar_log("Reserva de sala creada correctamente")

            # Mostrar resultado
            resultado.delete("1.0", tk.END)

            costo_total = reserva.obtener_costo_total()

            resultado.insert(
                tk.END,
                f"RESERVA CONFIRMADA\n\n"
                f"Cliente: {reserva.cliente.nombre}\n"
                f"Sala: {reserva.servicio.nombre} - {reserva.servicio.tipo_sala}\n"
                f"Fecha: {reserva.fecha.strftime('%Y-%m-%d')}\n"
                f"Duración: {reserva.duracion} horas\n"
                f"Costo Total: ${costo_total}\n"
                f"Estado: {reserva.estado}"
            )

            messagebox.showinfo(
                "Éxito",
                "Reserva creada y confirmada correctamente"
            )

            # Limpiar campos
            entry_fecha.delete(0, tk.END)
            entry_duracion.delete(0, tk.END)

        except ReservaError as e:
            messagebox.showerror("Error", str(e))
            registrar_log(f"ERROR RESERVA SALA: {e}")
        except Exception as e:
            messagebox.showerror("Error", f"Error inesperado: {str(e)}")
            registrar_log(f"ERROR RESERVA SALA: {e}")
            print("ERROR:", e)

    # -------------------------
    # Botón reservar
    # -------------------------

    boton_reservar = tk.Button(
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
    )

    boton_reservar.pack(pady=10)

def alquilar_equipo():
    messagebox.showinfo(
        "Alquiler",
        "Aquí irá el sistema de alquiler de equipos"
    )

def reservar_asesoria():
    messagebox.showinfo(
        "Asesoría",
        "Aquí irá el sistema de asesorías"
    )

# -------------------------
# Ventana principal
# -------------------------

ventana = tk.Tk()
ventana.title("Sistema de Reservas - Software FJ")
ventana.geometry("820x720")
ventana.config(bg="#1f1f1f")

# -------------------------
# Título
# -------------------------

titulo = tk.Label(
    ventana,
    text="Sistema de Reservas - Software FJ",
    font=("Arial", 30, "bold"),
    bg="#1f1f1f",
    fg="white"
)

titulo.pack(pady=20)

# -------------------------
# Frame principal
# -------------------------

frame_menu = tk.Frame(
    ventana,
    bg="#505050",
    width=520,
    height=450
)

frame_menu.pack(pady=10)

# Mantener tamaño fijo
frame_menu.pack_propagate(False)

# -------------------------
# Texto menu
# -------------------------

texto_menu = tk.Label(
    frame_menu,
    text="Menu",
    font=("Arial", 28),
    bg="#505050",
    fg="white"
)

texto_menu.pack(pady=20)

# -------------------------
# Estilo botones
# -------------------------

estilo_boton = {
    "font": ("Arial", 14),
    "bg": "#63c3fa",
    "fg": "black",
    "width": 18,
    "height": 2,
    "bd": 0,
    "cursor": "hand2"
}

# -------------------------
# Botón añadir cliente
# -------------------------

btn_cliente = tk.Button(
    frame_menu,
    text="Añadir Cliente",
    command=abrir_clientes,
    **estilo_boton
)

btn_cliente.pack(pady=14)

# -------------------------
# Botón reservar sala
# -------------------------

btn_sala = tk.Button(
    frame_menu,
    text="Reservar sala",
    command=reservar_sala,
    **estilo_boton
)

btn_sala.pack(pady=14)

# -------------------------
# Botón alquilar equipo
# -------------------------

btn_equipo = tk.Button(
    frame_menu,
    text="Alquilar Equipo",
    command=alquilar_equipo,
    **estilo_boton
)

btn_equipo.pack(pady=14)

# -------------------------
# Botón asesoría
# -------------------------

btn_asesoria = tk.Button(
    frame_menu,
    text="Reservar Asesoria",
    command=reservar_asesoria,
    **estilo_boton
)

btn_asesoria.pack(pady=14)

# -------------------------
# Footer
# -------------------------

footer = tk.Label(
    ventana,
    text="Creado por: Juan Miguel Salcedo Fulanoito perez",
    font=("Arial", 14),
    bg="#1f1f1f",
    fg="white"
)

footer.pack(pady=30)

# -------------------------
# Ejecutar
# -------------------------

ventana.mainloop()