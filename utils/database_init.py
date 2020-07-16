import sys
import openstack
import sqlite3

#Create DB Connection
dbconn = sqlite3.connect('./utils/database.db', check_same_thread=False)



#Helpers

def getUserProject(user, conn):
    lroles = conn.list_role_assignments()
    res = set()
    for i in range(len(lroles)):
        if lroles[i]['user'] == user.id:
            try :
                res.add(conn.get_project(lroles[i]['project']).name)
            except:
                ()
    return res

def getProject(item, conn):
    global dbconn
    nid = item.project_id
    if nid != "":
        try:
            return dbconn.execute("SELECT NAME FROM PROJECTS WHERE ID=?", (nid,)).fetchone()[0]
        except:
            return ""

def getUser(item, conn):
    global dbconn
    nid = item.user_id
    if nid != "":
        try:
            return dbconn.execute("SELECT NAME FROM USERS WHERE ID=?", (nid,)).fetchone()[0]
        except:
            return ""

def getImageName(server):
    global dbconn
    try :
        return dbconn.execute("SELECT NAME FROM IMAGES WHERE ID=?", (server.image['id'],)).fetchone()[0]
    except:
        ()

def serverSecGroupName(server):
    try:
        return server.security_groups[0]['name']
    except:
        return ""

def getNetworkSubnetsNames(network, conn):
    global dbconn
    lt = network.subnet_ids
    res = []
    for x in lt:
        name = dbconn.execute("SELECT NAME FROM SUBNETS WHERE ID=?", (x,)).fetchone()[0]
        res.append(name)
    return res

def getNetworkName(item, conn):
    global dbconn
    nid = item.network_id
    return dbconn.execute("SELECT NAME FROM NETWORKS WHERE ID=?", (nid,)).fetchone()[0]

def getRoutersNetworkName(router, conn):
    global dbconn
    try :
        return dbconn.execute("SELECT NAME FROM NETWORKS WHERE ID=?", (router.external_gateway_info['network_id'],)).fetchone()[0]
    except:
        ()

def getPortFixedIPs(port):
    lt = port.fixed_ips
    res = []
    for i in range(len(lt)):
        res.append(lt[i]['ip_address'])
    return res

def getPortSubnetsName(port):
    global dbconn
    lt = port.fixed_ips
    res = []
    for i in range(len(lt)):
        cursor = dbconn.execute("SELECT NAME FROM SUBNETS WHERE ID=?", (lt[i]['subnet_id'],))
        for row in cursor:
            res.append(row[0])
    return res

def getServerNameFloatingIP(fip, conn):
    global dbconn
    cursor = dbconn.execute("SELECT PRIVATE_IP, NAME FROM SERVERS")
    res = ""
    for row in cursor:
        if  row[0] != None and row[0] == fip.fixed_ip_address:
            res = row[1]
    return res

def getFloatingNetworkName(fip, conn):
    global dbconn
    nid = fip.floating_network_id
    return dbconn.execute("SELECT NAME FROM NETWORKS WHERE ID=?", (nid,)).fetchone()[0]

def getRouter(item):
    global dbconn
    iid = item.router_id
    if iid != None and iid != "":
        return dbconn.execute("SELECT NAME FROM ROUTERS WHERE ID=?", (iid,)).fetchone()[0]




def initDatabase(conn):
    global dbconn
    
    dbconn.execute('''CREATE TABLE IF NOT EXISTS PROJECTS(ID TEXT PRIMARY KEY NOT NULL, NAME TEXT NOT NULL, DESCRIPTION TEXT);''')
    dbconn.execute('''CREATE TABLE IF NOT EXISTS USERS(ID TEXT PRIMARY KEY NOT NULL, NAME TEXT NOT NULL, DESCRIPTION TEXT, PROJECT TEXT);''')
    dbconn.execute('''CREATE TABLE IF NOT EXISTS NETWORKS(ID TEXT PRIMARY KEY NOT NULL, CREATED_AT TEXT, NAME TEXT NOT NULL, PROJECT TEXT, NETWORK_TYPE TEXT,
    SUBNETS TEXT, IS_ROUTER_EXTERNAL TEXT, MTU TEXT, IS_VLAN_TRANSPARENT TEXT, STATUS TEXT);''')
    dbconn.execute('''CREATE TABLE IF NOT EXISTS SUBNETS(ID TEXT PRIMARY KEY NOT NULL, CREATED_AT TEXT, NAME TEXT NOT NULL, PROJECT TEXT, NETWORK TEXT,
    IP_VERSION TEXT, IPV6_ADDR TEXT, IPV6_RA TEXT, DHCP_ENABLED TEXT, CIDR TEXT, ALLOCATIONPOOLSTART TEXT, ALLOCATIONPOOLEND TEXT, DNS TEXT, GATEWAY TEXT);''')
    dbconn.execute('''CREATE TABLE IF NOT EXISTS PORTS(ID TEXT PRIMARY KEY NOT NULL, CREATED_AT TEXT, NAME TEXT NOT NULL, PROJECT TEXT, NETWORK TEXT,
    FIXED_IP TEXT, SUBNETS TEXT, DEVICE_OWNER TEXT, MAC_ADDR TEXT, STATUS TEXT);''')
    dbconn.execute('''CREATE TABLE IF NOT EXISTS SECURITY_GROUPS(ID TEXT PRIMARY KEY NOT NULL, CREATED_AT TEXT, NAME TEXT NOT NULL, PROJECT TEXT);''')
    dbconn.execute('''CREATE TABLE IF NOT EXISTS SECURITY_GROUP_RULES(ID TEXT PRIMARY KEY NOT NULL, SECURITY_GROUP_ID TEXT NOT NULL, CREATED_AT TEXT, PROJECT TEXT, DIRECTION TEXT, 
    PORT_RANGE_MIN TEXT, PORT_RANGE_MAX TEXT, PROTOCOL TEXT, REMOTE_IP_PREFIX TEXT);''')
    dbconn.execute('''CREATE TABLE IF NOT EXISTS ROUTERS(ID TEXT PRIMARY KEY NOT NULL, CREATED_AT TEXT, NAME TEXT NOT NULL, PROJECT TEXT, NETWORK TEXT, IS_ADMIN_STATE_UP TEXT,
    IS_DISTRIBUTED TEXT, STATUS TEXT);''')
    dbconn.execute('''CREATE TABLE IF NOT EXISTS NETWORK_AGENTS(ID TEXT PRIMARY KEY NOT NULL, CREATED_AT TEXT, STARTED_AT TEXT, AGENT_TYPE TEXT NOT NULL, HOST TEXT, IS_ALIVE TEXT,
    DESCRIPTION TEXT, LAST_HEARTBEAT_AT TEXT);''')
    dbconn.execute('''CREATE TABLE IF NOT EXISTS FLOATING_IPS(ID TEXT PRIMARY KEY NOT NULL, CREATED_AT TEXT, PROJECT TEXT, SERVER TEXT, FLOATING_IP_ADDR TEXT, FIXED_IP_ADDR TEXT,
    NETWORK TEXT, ROUTER TEXT, STATUS TEXT, PORT_ID TEXT);''')
    dbconn.execute('''CREATE TABLE IF NOT EXISTS SERVERS(ID TEXT PRIMARY KEY NOT NULL, CREATED_AT TEXT, LAUNCHED_AT TEXT, TERMINATED_AT TEXT, NAME TEXT NOT NULL, PROJECT TEXT, USER TEXT,
    IMAGE TEXT, HOSTNAME TEXT, HYPERVISOR_HOSTNAME TEXT, INSTANCE_NAME TEXT, PRIVATE_IP TEXT, PUBLIC_IP TEXT, SECURITY_GROUP_NAME TEXT, PROGRESS TEXT, VM_STATE TEXT, STATUS TEXT);''')
    dbconn.execute('''CREATE TABLE IF NOT EXISTS IMAGES(ID TEXT PRIMARY KEY NOT NULL, CREATED_AT TEXT, NAME TEXT NOT NULL, SIZE TEXT, MIN_DISK TEXT, MIN_RAM TEXT,
    PROGRESS TEXT, STATUS TEXT);''')
    dbconn.execute('''CREATE TABLE IF NOT EXISTS KEYPAIRS(ID TEXT PRIMARY KEY NOT NULL, CREATED_AT TEXT, NAME TEXT NOT NULL, USER TEXT, IS_DELETED TEXT, TYPE TEXT);''')
    dbconn.execute('''CREATE TABLE IF NOT EXISTS STACKS(ID TEXT PRIMARY KEY NOT NULL, CREATED_AT TEXT, NAME TEXT NOT NULL, STATUS TEXT);''')
    
    for project in conn.identity.projects():
        dbconn.execute(''' INSERT INTO PROJECTS(ID,NAME,DESCRIPTION) VALUES(?,?,?) ''', (project.id, project.name, project.description))
        dbconn.commit()
    for image in conn.compute.images():
        dbconn.execute(''' INSERT INTO IMAGES(ID,CREATED_AT,NAME,SIZE,MIN_DISK,MIN_RAM,PROGRESS,STATUS) VALUES(?,?,?,?,?,?,?,?) ''', (image.id, image.created_at, 
        image.name, image.size, image.min_disk, image.min_ram, image.progress, image.status))
        dbconn.commit()
    for agent in conn.network.agents():
        dbconn.execute(''' INSERT INTO NETWORK_AGENTS(ID,CREATED_AT,STARTED_AT,AGENT_TYPE,HOST,IS_ALIVE,DESCRIPTION,LAST_HEARTBEAT_AT) VALUES(?,?,?,?,?,?,?,?) ''', 
        (agent.id, agent.created_at, agent.started_at, agent.agent_type, agent.host, agent.is_alive, agent.description, agent.last_heartbeat_at))
        dbconn.commit()
    for user in conn.identity.users():
        dbconn.execute(''' INSERT INTO USERS(ID,NAME,DESCRIPTION,PROJECT) VALUES(?,?,?,?) ''', (user.id, user.name, user.description, "    ".join(getUserProject(user, conn))))
        dbconn.commit()
    for port in conn.network.security_groups():
        dbconn.execute(''' INSERT INTO SECURITY_GROUPS(ID,CREATED_AT,NAME,PROJECT) VALUES(?,?,?,?) ''', 
        (port.id, port.created_at, port.name, getProject(port, conn)))
        dbconn.commit()
    for rule in conn.network.security_group_rules():
        dbconn.execute(''' INSERT INTO SECURITY_GROUP_RULES(ID,SECURITY_GROUP_ID,CREATED_AT,PROJECT,DIRECTION,PORT_RANGE_MIN,PORT_RANGE_MAX,PROTOCOL,REMOTE_IP_PREFIX) VALUES(?,?,?,?,?,?,?,?,?) ''', 
        (rule.id, rule.security_group_id, rule.created_at, getProject(rule, conn), rule.direction, rule.port_range_min, rule.port_range_max, rule.protocol, rule.remote_ip_prefix))
        dbconn.commit()
    for keypair in conn.compute.keypairs():
        dbconn.execute(''' INSERT INTO KEYPAIRS(ID,CREATED_AT,NAME,USER,IS_DELETED,TYPE) VALUES(?,?,?,?,?,?) ''', 
        (keypair.created_at, keypair.name, dbconn.execute("SELECT NAME FROM USERS WHERE ID=?", (keypair.user_id,)).fetchone()[0], keypair.is_deleted, keypair.type))
        dbconn.commit()
    for server in conn.list_servers(all_projects=True):
        if server.status != "BUILD":
            dbconn.execute(''' INSERT INTO SERVERS(ID,CREATED_AT,LAUNCHED_AT,TERMINATED_AT,NAME,PROJECT,USER,IMAGE,HOSTNAME,HYPERVISOR_HOSTNAME,INSTANCE_NAME,PRIVATE_IP,PUBLIC_IP,
            SECURITY_GROUP_NAME,PROGRESS,VM_STATE,STATUS) VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?) ''', 
            (server.id, server.created_at, server.launched_at, server.terminated_at, server.name, getProject(server, conn), getUser(server, conn), getImageName(server),
            server.hostname, server.hypervisor_hostname, server.instance_name, conn.get_server_private_ip(server), conn.get_server_public_ip(server), serverSecGroupName(server), 
            server.progress, server.vm_state, server.status))
            dbconn.commit()
    for network in conn.network.networks():
        dbconn.execute(''' INSERT INTO NETWORKS(ID,CREATED_AT,NAME,PROJECT,NETWORK_TYPE,SUBNETS,IS_ROUTER_EXTERNAL,MTU,IS_VLAN_TRANSPARENT,STATUS) VALUES(?,?,?,?,?,?,?,?,?,?) ''', 
        (network.id, network.created_at, network.name, getProject(network,conn), network.provider_network_type, "", network.is_router_external, network.mtu, 
        network.is_vlan_transparent, network.status))
        dbconn.commit()
    for subnet in conn.network.subnets():
        dbconn.execute(''' INSERT INTO SUBNETS(ID,CREATED_AT,NAME,PROJECT,NETWORK,IP_VERSION,IPV6_ADDR,IPV6_RA,DHCP_ENABLED,CIDR,ALLOCATIONPOOLSTART,
        ALLOCATIONPOOLEND,DNS,GATEWAY) VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?) ''', 
        (subnet.id, subnet.created_at, subnet.name, getProject(subnet, conn), getNetworkName(subnet, conn), subnet.ip_version, subnet.ipv6_address_mode, subnet.ipv6_ra_mode, 
        subnet.is_dhcp_enabled, subnet.cidr, subnet.allocation_pools[0]["start"], subnet.allocation_pools[0]["end"], "    ".join(subnet.dns_nameservers), subnet.gateway_ip))
        dbconn.commit()
    cursorUpdateNetwork = dbconn.execute("SELECT ID FROM NETWORKS")
    for network in conn.network.networks():
        for row in cursorUpdateNetwork:
            if network.id == row[0]:
                dbconn.execute("UPDATE NETWORKS SET SUBNETS=? WHERE ID=?", ("    ".join(getNetworkSubnetsNames(network, conn)), row[0]))
                dbconn.commit()
    for router in conn.network.routers():
        dbconn.execute(''' INSERT INTO ROUTERS(ID,CREATED_AT,NAME,PROJECT,NETWORK,IS_ADMIN_STATE_UP,IS_DISTRIBUTED, STATUS) VALUES(?,?,?,?,?,?,?,?) ''', 
        (router.id, router.created_at, router.name, getProject(router, conn), getRoutersNetworkName(router, conn), router.is_admin_state_up, router.is_distributed, router.status))
        dbconn.commit()
    for port in conn.list_ports():
        dbconn.execute(''' INSERT INTO PORTS(ID,CREATED_AT,NAME,PROJECT,NETWORK,FIXED_IP,SUBNETS,DEVICE_OWNER,MAC_ADDR,STATUS) VALUES(?,?,?,?,?,?,?,?,?,?) ''', 
        (port.id, port.created_at, port.name, getProject(port, conn), getNetworkName(port, conn), "    ".join(getPortFixedIPs(port)), 
        "    ".join(getPortSubnetsName(port)), port.device_owner, port.mac_address, port.status))
        dbconn.commit()
    for ip in conn.list_floating_ips():
        dbconn.execute(''' INSERT INTO FLOATING_IPS(ID,CREATED_AT,PROJECT,SERVER,FLOATING_IP_ADDR,FIXED_IP_ADDR,NETWORK,ROUTER,STATUS,PORT_ID) VALUES(?,?,?,?,?,?,?,?,?,?) ''', 
        (ip.id, ip.created_at, getProject(ip, conn), getServerNameFloatingIP(ip, conn), ip.floating_ip_address, ip.fixed_ip_address, getFloatingNetworkName(ip, conn), 
        getRouter(ip), ip.status, ip.port_id))
        dbconn.commit()
    for stack in conn.list_stacks():
        dbconn.execute(''' INSERT INTO STACKS(ID,CREATED_AT,NAME,STATUS) VALUES(?,?,?,?) ''', (stack.id, stack.created_at, stack.stack_name, stack.status))
        dbconn.commit()
        