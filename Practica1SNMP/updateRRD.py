import time
import rrdtool
from getSNMP import consultaSNMP
total_multpack_traffic = 0
total_ippack_traffic = 0
total_icmpmsgs_traffic = 0
total_tcpsegs_traffic = 0
total_udpdata_traffic = 0


def monitorear(comunidad, host, sistema, id, snmp_v, puerto):

    global total_multpack_traffic
    global total_ippack_traffic
    global total_icmpmsgs_traffic
    global total_tcpsegs_traffic
    global total_udpdata_traffic

    while 1:
        if sistema == "windows":
            total_multpack_traffic = int(
                consultaSNMP(comunidad, host,
                             '1.3.6.1.2.1.2.2.1.18.9', snmp_v, puerto))
        else:
            total_multpack_traffic = int(
                consultaSNMP(comunidad, host,
                             '1.3.6.1.2.1.2.2.1.18.2', snmp_v, puerto))

        total_ippack_traffic = int(
            consultaSNMP(comunidad,host,
                         '1.3.6.1.2.1.4.10.0', snmp_v, puerto))

        total_icmpmsgs_traffic = int(
            consultaSNMP(comunidad, host,
                         '1.3.6.1.2.1.5.1.0', snmp_v, puerto))

        total_tcpsegs_traffic = int(
            consultaSNMP(comunidad, host,
                         '1.3.6.1.2.1.6.12.0', snmp_v, puerto))

        total_udpdata_traffic = int(
            consultaSNMP(comunidad, host,
                         '1.3.6.1.2.1.7.4.0', snmp_v, puerto))

        valor = "N:" + str(total_multpack_traffic) + ':' + str(total_ippack_traffic) + ':' + str(total_icmpmsgs_traffic) + ':' + str(total_tcpsegs_traffic) + ':' + str(total_udpdata_traffic)

        rrdtool.update('traficoRED{}.rrd'.format(id), valor)
        rrdtool.dump('traficoRED{}.rrd'.format(id),'traficoRED{}.xml'.format(id))
        time.sleep(1)

    if ret:
        print (rrdtool.error())
        time.sleep(300)