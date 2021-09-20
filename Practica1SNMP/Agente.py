from getSNMP import consultaSNMP
from CreateRRD import crear_rrd
from updateRRD import monitorear
import time
import threading


class Agente:
    def __init__(self, host, snmp_v, comunidad, puerto, id):
        self.host = host
        self.snmp_v = snmp_v
        self.comunidad = comunidad
        self.puerto = puerto
        self.sistema = "linux"
        self.id = id
        self.getSistema()
        if self.sistema != "Ninguno":
            crear_rrd(self.id)
            self.nombre = consultaSNMP(self.comunidad, self.host, "1.3.6.1.2.1.1.5.0", self.snmp_v, self.puerto)
            self.ubicacion = consultaSNMP(self.comunidad, self.host, "1.3.6.1.2.1.1.6.0", self.snmp_v, self.puerto)
            self.tiempo = time.ctime(int(consultaSNMP(self.comunidad, self.host, "1.3.6.1.2.1.1.3.0", self.snmp_v, self.puerto)))
        self.t = threading.Thread(target=self.startMonitoreo)
        self.t.start()


    def getDatos(self):
        print(self.host, self.snmp_v, self.comunidad, self.puerto, self.sistema, self.id)

    def getSistema(self):
        valor = consultaSNMP(self.comunidad, self.host, "1.3.6.1.2.1.1.1.0", self.snmp_v, self.puerto)
        if valor:
            print(str(valor[0]))
        else:
            self.sistema = "Ninguno"
            print("No se puede obtener información del sistema")
            return

        # Se detecta si el sistema ingresado fue windows o linux con una consulta sysDescr con SNMP
        if ("Windows" in str(valor[0])) or ("windows" in str(valor[0])):
            print("Sistema Windows detectado")
            self.sistema = "windows"
        else:
            print("Sistema Linux detectado")

    def intStatus(self, interfacesTotales):
        for i in range(interfacesTotales):
            int_nombre = consultaSNMP(self.comunidad, self.host, "1.3.6.1.2.1.2.2.1.2.{}".format(i+1), self.snmp_v, self.puerto)
            int_admin_estado = consultaSNMP(self.comunidad, self.host, "1.3.6.1.2.1.2.2.1.7.{}".format(i+1), self.snmp_v, self.puerto)
            if int_admin_estado == '1':
                print("Interface", (i+1), int_nombre, "Estado: Up")
            else:
                print("Interface", (i+1), int_nombre[:len(int_nombre)], "Estado: Dowm")

    def startMonitoreo(self):
        t = threading.currentThread()
        monitorear(self.comunidad, self.host, self.sistema, self.id, self.snmp_v, self.puerto)

    def stopMonitoreo(self):
        self.t.runnig = False
