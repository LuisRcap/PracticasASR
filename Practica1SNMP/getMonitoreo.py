from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from graphRRD import graficarTrafico
from Agente import *
import time
import os

archivoExiste = False

if os.path.exists("agentes.txt"):
    archivoExiste = True

listaAgentes = []
contId = 1


def add_agente(host, snmp_v, comunidad, puerto):
    global contId
    f = open("agentes.txt", "a")
    if len(listaAgentes) > 0:
        existe = False

        for agente in listaAgentes:
            if agente.host == host and agente.comunidad == comunidad:
                existe = True
                break

        if not existe:

            f.write("\n{} {} {} {}".format(host, snmp_v, comunidad, puerto))
            f.close()

            listaAgentes.append(Agente(host, snmp_v, comunidad, puerto, contId))
            contId += 1
            print("El agente fue agregado con exito")
            listaAgentes[len(listaAgentes) - 1].getDatos()

        else:
            print("El agente ya existe")
            return
    else:
        f.write("{} {} {} {}".format(host, snmp_v, comunidad, puerto))
        f.close()
        listaAgentes.append(Agente(host, snmp_v, comunidad, puerto, contId))
        contId += 1
        print("El agente fue agregado con exito")
        listaAgentes[0].getDatos()


def remove_agente(host, comunidad):
    global contId
    f = open("agentes.txt", "r")
    contenido = f.read().split("\n")
    f.close()

    existe = False
    for agente in listaAgentes:
        if agente.host == host and agente.comunidad == comunidad:
            agenteToRemove = "{} {} {} {}".format(agente.host, agente.snmp_v, agente.comunidad, agente.puerto)

            if os.path.exists("traficoRED{}.rrd".format(agente.id)):
                os.remove("traficoRED{}.rrd".format(agente.id))

            if os.path.exists("traficoRED{}.xml".format(agente.id)):
                os.remove("traficoRED{}.xml".format(agente.id))

            listaAgentes.remove(agente)
            print("El agente fue eliminado con exito")
            existe = True
            break
    if not existe:
        print("No se encontró el agente")
    else:
        f = open("agentes.txt", "w")
        if agenteToRemove in contenido:
            contenido.remove(agenteToRemove)

        for i in range(len(contenido)):
            if i == 0:
                f.write(contenido[i])
            else:
                f.write("\n" + contenido[i])
            listaAgentes[i].id = i+1
            contId = i+1


def getReporte(agente, tiempo_inicio, tiempo_fin):

    graficarTrafico(agente.id, tiempo_inicio, tiempo_fin)
    time.sleep(5)
    w, h = A4

    # Esta variable manejará el archivo PDF pra mostrar aquí las gráficas
    c = canvas.Canvas("Reporte{}.pdf".format(agente.id), pagesize=A4)
    if agente.sistema == "linux":
        c.drawImage("Debian_logo.png", 20, h-80, width=60, height=60)
    else:
        c.drawImage("logo-windows.png", 20, h - 80, width=60, height=60)


    txt = c.beginText(100, h-50)
    txt.setFont("Helvetica", 12)
    txt.textLines("Nombre: " + str(agente.nombre) + "\n" +
                  "Version SNMP: " + str(agente.snmp_v) + "\n" +
                  "Sistema Operativo: " + agente.sistema + "\n" +
                  "Ubicacion: " + str(agente.ubicacion) + "\n" +
                  "Puerto: " + agente.puerto + "\n" +
                  "Tiempo activo: " + str(agente.tiempo) + "\n" +
                  "Comunidad: " + agente.comunidad + "\n" +
                  "IP: " + agente.host + "\n")

    c.drawText(txt)
    c.drawImage("traficoRED{}-1.png".format(agente.id), 90, h - 400, width=400, height=200)
    c.drawImage("traficoRED{}-2.png".format(agente.id), 90, h - 620, width=400, height=200)
    c.showPage()
    c.drawImage("traficoRED{}-3.png".format(agente.id), 90, h - 300, width=400, height=200)
    c.drawImage("traficoRED{}-4.png".format(agente.id), 90, h - 520, width=400, height=200)
    c.drawImage("traficoRED{}-5.png".format(agente.id), 90, h - 740, width=400, height=200)
    c.save()
    print("El archivo fue creado con éxito")
    


if archivoExiste:
    f = open("agentes.txt", "r")
    contenido = f.read().split("\n")
    f.close()
    print(contenido)
    for i in range(len(contenido)):
        [host, snmp_v, comunidad, puerto] = contenido[i].split()
        listaAgentes.append(Agente(host, snmp_v, comunidad, puerto, (i + 1)))
        contId = i + 1
    for agente in listaAgentes:
        if agente.sistema != "Ninguno":
            print(agente.id, "Host: " + agente.host + " Estado: Up")
            if agente.sistema == "windows":
                print("Total de interfaces de red: 62")
                agente.intStatus(62)
            else:
                print("Total de interfaces de red: 2")
                agente.intStatus(2)
        else:
            print(agente.id, "Host: " + agente.host + " Estado: Up")

else:
    print("Aún no existen agentes")

while True:
    opcion = int(input(
        "Indique la acción que quiere hacer:\n1. Agregar agente\n2. Eliminar agente\n3. Enlistar agentes activos\n4. Obtener reporte \nPresione cualquier otro para cerrar el programa\n"))

    if opcion == 1:
        host = input("Indique el nombre del host o ip del dispositivo: ")
        snmp_v = input("Indique la versión de snmp a utilizar:\n1. v1\n2. v2c\n")
        comunidad = input("Indique la comunidad a la que pertenece el agente: ")
        puerto = input("Indique el puerto de snmp del agente: ")

        add_agente(host, snmp_v, comunidad, puerto)

    elif opcion == 2:
        host = input("Indique el nombre del host o ip del dispositivo a eliminar: ")
        comunidad = input("Indique la comunidad a la que pertenece el agente a eliminar: ")

        remove_agente(host, comunidad)

    elif opcion == 3:
        for i in range(0, len(listaAgentes)):
            print("agente", (i + 1), ":")
            listaAgentes[i].getDatos()
    elif opcion == 4:
        print("seleccione un agente:")
        for i in range(0, len(listaAgentes)):
            print("agente", (i + 1), ":")
            listaAgentes[i].getDatos()
        op = int(input())
        tiempo_ini = input("Indique el tiempo iniical con formato dd-mm-yyyy HH:MM: ")
        tiempo_final = input("Indique el tiempo final con formato dd-mm-yyyy HH:MM: ")

        getReporte(listaAgentes[op - 1], tiempo_ini, tiempo_final)


    else:
        for i in range(len(listaAgentes)):
            listaAgentes[i].stopMonitoreo()

        for i in range(contId):
            if os.path.exists("traficoRED{}.rrd".format(i+1)):
                os.remove("traficoRED{}.rrd".format(i+1))

            if os.path.exists("traficoRED{}.xml".format(i + 1)):
                os.remove("traficoRED{}.xml".format(i + 1))

        break
