from pysnmp.entity.rfc3413.oneliner import cmdgen

''' This script obtains basic LSP information from a device via SNMP and displays it in a table. '''

''' class ALIGN is responsible for displaying the information in an ordered table '''
#--------------------------------------------------------------------
class ALIGN:
    LEFT, RIGHT = '-', ''

class Column(list):
    def __init__(self, name, data, align=ALIGN.RIGHT):
        list.__init__(self, data)
        self.name = name
        width = max(len(str(x)) for x in data + [name])
        self.format = ' %%%s%ds ' % (align, width)

class Table:
    def __init__(self, *columns):
        self.columns = columns
        self.length = max(len(x) for x in columns)
    def get_row(self, i=None):
        for x in self.columns:
            if i is None:
                yield x.format % x.name
            else:
                yield x.format % x[i]
    def get_rows(self):
        yield ' '.join(self.get_row(None))
        for i in range(0, self.length):
            yield ' '.join(self.get_row(i))

    def __str__(self):
        return '\n'.join(self.get_rows())   
#--------------------------------------------------------------------

#VARIABLES
lspoidObject=[] 
lspoidString=[] 
mplsLspName=[]
mplsPathType=[]
mplsLspFrom=[]
mplsLspTo=[]
mplsPathExplicitRoute=[]
mplsPathRecordRoute=[]

mplsLspNameOID = '1.3.6.1.4.1.2636.3.2.5.1.1'
mplsLspEntry = '1.3.6.1.4.1.2636.3.2.5.1.'

# Lists with correspondent host names, IPs and communities.
host_names = [ 'host1']
host_ips = [ '1.1.1.1']
host_communities = [ 'comm1' ]

#FUNCIONES
def get_next(oid,comhost,iphost):
    listat = []
    listaoid = []
    cmdGen = cmdgen.CommandGenerator()
    #snmpwalk oid
    errorIndication, errorStatus, errorIndex, varBindTable = cmdGen.nextCmd(
        cmdgen.CommunityData(comhost),
        cmdgen.UdpTransportTarget((iphost, 161)),
        oid  
    )
    # Check and display
    if errorIndication:
        print(errorIndication)
    else:
        if errorStatus:
            print('%s at %s' % (
                errorStatus.prettyPrint(),
                errorIndex and varBindTable[-1][int(errorIndex)-1] or '?'
                )
            )
        else:
            for varBindTableRow in varBindTable:
                for name, val in varBindTableRow:
                    listaoid.append(name)
                    listat.append(val)
    return listat, listaoid

def seleccion_host():
    print 'Select host: '
    counter_temp = 1
    for host in host_names:
        print counter_temp, ') ', host
        counter_temp = counter_temp + 1

    while True:
        seleccion = input('Ingrese #: ')
        if seleccion < 1 or seleccion > len(host_names):
            continue
        else:
            break
    return seleccion

#MAIN

#Obtain lists
mplsLspFromOBJ =[]
mplsLspToOBJ= []

indice_host = seleccion_host() - 1
ip_h = host_ips[indice_host]
com_h = host_communities[indice_host]
print ip_h, com_h
mplsLspName, lspoidObject = get_next(mplsLspNameOID,com_h,ip_h)
mplsLspFromOBJ, pela = get_next(mplsLspEntry + '15',com_h,ip_h)
print mplsLspFromOBJ

for temp in mplsLspFromOBJ:
    temp = str(temp).encode('hex')
    mplsLspFrom.append('.'.join(str(int(i, 16)) for i in ([temp[i:i+2] for i in range(0, len(temp), 2)])))

    
mplsLspToOBJ, pela = get_next(mplsLspEntry + '16',com_h,ip_h)

for temp in mplsLspToOBJ:
    temp = str(temp).encode('hex')
    mplsLspTo.append('.'.join(str(int(i, 16)) for i in ([temp[i:i+2] for i in range(0, len(temp), 2)])))


mplsPathType, pela = get_next(mplsLspEntry + '18',com_h,ip_h)
tipos_path = [ 'other', 'primary', 'standby', 'secondary' ]
indice_temp = 0
for temp in mplsPathType:
    mplsPathType[indice_temp] = tipos_path[temp-1]
    indice_temp = indice_temp + 1
    
mplsPathExplicitRoute, pela = get_next(mplsLspEntry + '19',com_h,ip_h)
mplsPathRecordRoute, pela = get_next(mplsLspEntry + '20',com_h,ip_h)

################ DISPLAY TABLE #################
tabla_info =  Table(
        Column("LspName", mplsLspName,'-'),
        Column("LspFrom", mplsLspFrom,'-'),
        Column("LspTo", mplsLspTo,'-'),
        Column("PathType", mplsPathType,'-'),
        Column("PathExplicitRoute", mplsPathExplicitRoute,'-'),
        Column("PathRecordRoute", mplsPathRecordRoute,'-')
                    )

print tabla_info




