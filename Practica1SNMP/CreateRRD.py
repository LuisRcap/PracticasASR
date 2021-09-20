#!/usr/bin/env python

import rrdtool


def crear_rrd(id):
    ret = rrdtool.create("traficoRED{}.rrd".format(id),
                         "--start",'N',
                         "--step",'60',
                         "DS:multpack:COUNTER:300:U:U",
                         "DS:ippack:COUNTER:300:U:U",
                         "DS:icmpmsgs:COUNTER:300:U:U",
                         "DS:tcpsegs:COUNTER:300:U:U",
                         "DS:udpdata:COUNTER:300:U:U",
                         "RRA:AVERAGE:0.5:6:5",
                         "RRA:AVERAGE:0.5:1:20",
                         "RRA:AVERAGE:0.5:1:20",
                         "RRA:AVERAGE:0.5:1:20",
                         "RRA:AVERAGE:0.5:6:5")


    if ret:
        print(rrdtool.error())
