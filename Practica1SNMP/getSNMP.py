from pysnmp.hlapi import *


def consultaSNMP(comunidad, host, oid, snmp_v, puerto):
    if snmp_v == "2":
        errorIndication, errorStatus, errorIndex, varBinds = next(
            getCmd(SnmpEngine(),
                   CommunityData(comunidad),
                   UdpTransportTarget((host, puerto)),
                   ContextData(),
                   ObjectType(ObjectIdentity(oid))))
    else:
        errorIndication, errorStatus, errorIndex, varBinds = next(
            getCmd(SnmpEngine(),
                   CommunityData(comunidad, mpModel=0),
                   UdpTransportTarget((host, puerto)),
                   ContextData(),
                   ObjectType(ObjectIdentity(oid))))

    if errorIndication:
        print(errorIndication)
    elif errorStatus:
        print('%s at %s' % (errorStatus.prettyPrint(), errorIndex and varBinds[int(errorIndex) - 1][0] or '?'))
    else:
        if oid == "1.3.6.1.2.1.1.1.0":
            return varBinds

        elif 18 < len(oid) <= 22:
            for varBind in varBinds:
                varB = (' = '.join([x.prettyPrint() for x in varBind]))
            val = varB.split('= ')[1]
            if len(val) > 2:
                try:
                    resultado = bytes.fromhex(val[2:]).decode(encoding='latin1')
                except:
                    resultado = val
            else:
                resultado = val
            return resultado

        else:
            for varBind in varBinds:
                varB = (' = '.join([x.prettyPrint() for x in varBind]))
                resultado = varB.split()[2]
            return resultado
