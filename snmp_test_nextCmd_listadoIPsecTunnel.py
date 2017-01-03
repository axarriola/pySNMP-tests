#walk of jnxJsIpSecTunnelEntry

from pysnmp.entity.rfc3413.oneliner import cmdgen

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
# Constant OIDs
jnxJsIpSecTunPolicyName = '1.3.6.1.4.1.2636.3.39.1.5.1.2.1.1.1'
jnxJsIpSecTunnelEntry = '1.3.6.1.4.1.2636.3.39.1.5.1.2.1.1'
jnxJsIpSecVpnTunType = '1.3.6.1.4.1.2636.3.39.1.5.1.2.1.1.2'
jnxJsIpSecTunCfgMonState = '1.3.6.1.4.1.2636.3.39.1.5.1.2.1.1.3'
jnxJsIpSecTunState = '1.3.6.1.4.1.2636.3.39.1.5.1.2.1.1.4'
jnxIpSecTunMonLocalGwAddr = '1.3.6.1.4.1.2636.3.52.1.2.2.1.5'
jnxIpSecTunMonLocalProxyId = '1.3.6.1.4.1.2636.3.52.1.2.2.1.6'
jnxIpSecTunMonRemoteProxyId = '1.3.6.1.4.1.2636.3.52.1.2.2.1.7'

#Lists
IpSecTunnelNamesOID = []
IpsecTunnelName = []
IpSecTunnelType = []
IpSecTunnelState = []
IpSecTunnelLocalGwAdd = []
IpSecTunnelLocalProxyId = []
IpSecTunnelRemoteProxyId = []

#FUNCTIONS
def get_next(oid):
    global lista_valores
    global lista_oid
    lista_valores = []
    lista_oid = []
    cmdGen = cmdgen.CommandGenerator()
    #snmpwalk
    errorIndication, errorStatus, errorIndex, varBindTable = cmdGen.nextCmd(
        cmdgen.CommunityData('Community'),
        cmdgen.UdpTransportTarget(('1.1.1.1', 161)),
        oid  
    )

    # Check for errors
    if errorIndication:
        print(errorIndication)
    else:
        if errorStatus:
            print('%s at %s' % (
                errorStatus.prettyPrint(),
                errorIndex and varBindTable[-1][int(errorIndex)-1] or '?'
                )
            )
        else: #Obtain values
            for varBindTableRow in varBindTable:
                for name, val in varBindTableRow:
                    lista_oid.append(name)
                    lista_valores.append(val)
    return lista_valores, lista_oid

# Obtain the last part of the OID that corresponds to each tunnel
# This will be used to add at the end of the distinct OIDs
# Example: jnxJsIpSecTunState + IpSecTunnelNamesOID[2] 
def listado_oids_tuneles():
    for temp in IpSecTunnelNamesOID:
        indice_temp = IpSecTunnelNamesOID.index(temp)
        IpSecTunnelNamesOID[indice_temp] = str(temp)
        IpSecTunnelNamesOID[indice_temp] = IpSecTunnelNamesOID[indice_temp].replace(jnxJsIpSecTunPolicyName,'')

#MAIN
IpSecTunnelName, IpSecTunnelNamesOID = get_next(jnxJsIpSecTunPolicyName)
IpSecTunnelType = get_next(jnxJsIpSecVpnTunType)[0] #returns a tuple, hence [0]
IpSecTunnelState = get_next(jnxJsIpSecTunState)[0]
IpSecTunnelLocalGwAdd = get_next(jnxIpSecTunMonLocalGwAddr)[0]
IpSecTunnelLocalProxyId = get_next(jnxIpSecTunMonLocalProxyId)[0]
IpSecTunnelRemoteProxyId = get_next(jnxIpSecTunMonRemoteProxyId)[0]

print "IPSec Info"
############TABLE
print Table(
        Column("Policy Name", IpSecTunnelName,'-'),
        Column("Type", IpSecTunnelType,'-'),
        Column("State", IpSecTunnelState,'-'),
        Column("Local GW Address", IpSecTunnelLocalGwAdd,'-'),
        Column("Local Proxy ID", IpSecTunnelLocalProxyId,'-'),
        Column("Remote Proxy ID", IpSecTunnelRemoteProxyId,'-')
    )





