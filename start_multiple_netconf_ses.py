import sys
import time
import xml.dom.minidom
from xml.dom import minidom
from ncclient import manager
from xml.dom.minidom import parse, parseString
from thread import start_new_thread
import sys, os, string, thread


global swMgr

swMgr = None
def writeToFile(fileName, data):

                f = open(fileName,'w')
                f.write(data)
                f.close()

def prettify(xmlstr):

        """Used for prettify the XML output from switch.
        Arguments: 
           xmlstr       : any xml string
        """

        reparsed = minidom.parseString(xmlstr)
        return reparsed.toprettyxml(indent=" ")


### get product information
def connect_switch(host, port, userName, password, timeout,cmd):
    global swMgr
    #print "Connecting to  switch <IP:Port = %s:%s>\n" % (host,port)
    print "%s" % cmd
    swMgr = manager.connect_ssh(host=host, port=port, username=userName, password=password,timeout=timeout, hostkey_verify=False)

def get_product_info(cmd):

    global swMgr

    #product_information_Str="""<opsw:product-information xmlns:opsw="http://www.polatis.com/yang/optical-switch"><opsw:model-name/></opsw:product-information>"""
    product_information_Str="""<opsw:product-information xmlns:opsw="http://www.polatis.com/yang/optical-switch"/>"""
    try:
        print "%sget model name..\n" % cmd
        print "product_information_Str : %s\n\n" % product_information_Str
        time.sleep(5)
        xmlout = swMgr.get(filter=('subtree',product_information_Str)).data_xml
        time.sleep(5)
            
        xmlout = prettify(xmlout)
        print "xmlout : %s\n\n" % xmlout
        print "%sget model name : output received\n" % cmd
        time.sleep(5)
    except Exception as err:
        print "%sget model name : not getting output\n" % cmd



### main
def main(cmd):
    connect_switch('10.99.99.225','830','admin','root',60, cmd)
    time.sleep(5)
    get_product_info(cmd)
#main('Establish multiple netconf session')

for ses in range(1, 11):
    time.sleep(10)
    start_new_thread(main,('Establish netconf session %s : ' % ses,))
#    time.sleep(3600000000)


while True:
    pass
