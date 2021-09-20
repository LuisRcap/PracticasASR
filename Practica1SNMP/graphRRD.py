import sys
import rrdtool
import time
#Grafica desde el tiempo actual menos diez minutos


def graficarTrafico(id, tiempo_inicial, tiempo_final):
    tiempo_inicial = time.strptime(tiempo_inicial, "%d-%m-%Y %H:%M")
    tiempo_inicial = int(time.mktime(tiempo_inicial))

    tiempo_final = time.strptime(tiempo_final, "%d-%m-%Y %H:%M")
    tiempo_final = int(time.mktime(tiempo_final))

    ret = rrdtool.graph("traficoRED{}-1.png".format(id),
                        "--start",str(tiempo_inicial),
                        "--end",str(tiempo_final),
                        "--vertical-label=Bytes/s",
                        "--title=Tráfico de Red de un agente \n Usando SNMP y RRDtools",
                        "DEF:multpack=traficoRED{}.rrd:multpack:AVERAGE".format(id),
                        "LINE3:multpack#00FF00:Paquetes multicast")

    ret = rrdtool.graph("traficoRED{}-2.png".format(id),
                        "--start", str(tiempo_inicial),
                        "--end", str(tiempo_final),
                        "--vertical-label=Bytes/s",
                        "--title=Tráfico de Red de un agente \n Usando SNMP y RRDtools",
                        "DEF:ippack=traficoRED{}.rrd:ippack:AVERAGE".format(id),
                        "AREA:ippack#0000FF:Paquetes IPv4")

    ret = rrdtool.graph("traficoRED{}-3.png".format(id),
                        "--start", str(tiempo_inicial),
                        "--end", str(tiempo_final),
                        "--vertical-label=Bytes/s",
                        "--title=Tráfico de Red de un agente \n Usando SNMP y RRDtools",
                        "DEF:icmpmsgs=traficoRED{}.rrd:icmpmsgs:AVERAGE".format(id),
                        "LINE3:icmpmsgs#FF0000:Mensajes ICMP")

    ret = rrdtool.graph("traficoRED{}-4.png".format(id),
                        "--start", str(tiempo_inicial),
                        "--end", str(tiempo_final),
                        "--vertical-label=Bytes/s",
                        "--title=Tráfico de Red de un agente \n Usando SNMP y RRDtools",
                        "DEF:tcpsegs=traficoRED{}.rrd:tcpsegs:AVERAGE".format(id),
                        "AREA:tcpsegs#078670:Segmentos TCP")

    ret = rrdtool.graph("traficoRED{}-5.png".format(id),
                        "--start", str(tiempo_inicial),
                        "--end", str(tiempo_final),
                        "--vertical-label=Bytes/s",
                        "--title=Tráfico de Red de un agente \n Usando SNMP y RRDtools",
                        "DEF:udpdata=traficoRED{}.rrd:udpdata:AVERAGE".format(id),
                        "AREA:udpdata#930B3F:Datos UDP")
