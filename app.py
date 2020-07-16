
import tkinter as tk
from tkinter import ttk
from tkinter import *
from tkinter.ttk import Treeview
from tkinter.messagebox import *
from tkinter.filedialog import *
from utils import osconn
from utils import osdata
from utils import thread
from utils import database_init
import sqlite3
import os
import sys
import openstack
from threading import Thread
import webbrowser

        

#Global var OS connection
conn = None


#Root UI
window = Tk()
window.title("OSupervisor")
window.geometry('600x750')
#window.resizable(width=0, height=0)

#Monitoring checkbutton
addButton=None
deleteButton=None
createRuleButton=None
deleteRuleButton=None
monitor = BooleanVar(value=False)
check = Checkbutton(window, text="Monitoring Only", fg='red', variable=monitor, onvalue=False, offvalue=True, command= lambda: monitoringMode(monitor))


def monitoringMode(monitor):
    global addButton, deleteButton, createRuleButton, deleteRuleButton
    if monitor.get():
        showinfo('WARNING', 'Please be aware of what you may modify !')
        if (addButton, deleteButton, createRuleButton, deleteRuleButton) != (None, None, None, None):
            try:
                createRuleButton.config(state=ACTIVE)
            except:
                ()
            try:
                deleteRuleButton.config(state=ACTIVE)
            except:
                ()
            try:
                addButton.config(state=ACTIVE)
            except:
                ()
            try:
                deleteButton.config(state=ACTIVE)
            except:
                ()
    else:
        if (addButton, deleteButton, createRuleButton, deleteRuleButton) != (None, None, None, None):
            try:
                createRuleButton.config(state=DISABLED)
            except:
                ()
            try:
                deleteRuleButton.config(state=DISABLED)
            except:
                ()
            try:
                addButton.config(state=DISABLED)
            except:
                ()
            try:
                deleteButton.config(state=DISABLED)
            except:
                ()

def setButtons(monitor):
    if monitor.get():
        try:
            createRuleButton.pack(padx = 10, pady = 10, side = 'left')
            createRuleButton.config(state=ACTIVE)
        except:
            ()
        try:
            deleteRuleButton.pack(padx = 10, pady = 10, side = 'left')
            deleteRuleButton.config(state=ACTIVE)
        except:
            ()
        try:
            addButton.pack(padx = 10, pady = 10, side = 'left')
            addButton.config(state=ACTIVE)
        except:
            ()
        try:
            deleteButton.pack(padx = 10, pady = 10, side = 'left')
            deleteButton.config(state=ACTIVE)
        except:
            ()
    else:
        try:
            createRuleButton.pack(padx = 10, pady = 10, side = 'left')
            createRuleButton.config(state=DISABLED)
        except:
            ()
        try:
            deleteRuleButton.pack(padx = 10, pady = 10, side = 'left')
            deleteRuleButton.config(state=DISABLED)
        except:
            ()
        try:
            addButton.pack(padx = 10, pady = 10, side = 'left')
            addButton.config(state=DISABLED)
        except:
            ()
        try:
            deleteButton.pack(padx = 10, pady = 10, side = 'left')
            deleteButton.config(state=DISABLED)
        except:
            ()
    

#MainFrame
mainFrame = LabelFrame(window, text="OpenStack Supervisor")


#Menubar
menubar = Menu(window)

menu1 = Menu(menubar, tearoff=0)
menubar.add_cascade(label="Main", menu=menu1)
menu1.add_command(label="Quick View", command= lambda: displayMain(mainFrame))
menu1.add_command(label="Quit", command= lambda: on_closing())


menu2 = Menu(menubar, tearoff=0)
menubar.add_cascade(label="Identity", menu=menu2)
menu2.add_command(label="Projects", command= lambda: displayProjects(mainFrame))
menu2.add_command(label="Users", command=lambda: displayUsers(mainFrame))

menu3 = Menu(menubar, tearoff=0)
menubar.add_cascade(label="Compute", menu=menu3)
menu3.add_command(label="Images", command=lambda: displayImages(mainFrame))
menu3.add_command(label="Servers", command=lambda: displayServers(mainFrame))
menu3.add_command(label="KeyPairs", command=lambda: displayKeyPairs(mainFrame))

menu4 = Menu(menubar, tearoff=0)
menubar.add_cascade(label="Network", menu=menu4)
menu4.add_command(label="Networks", command=lambda: displayNetworks(mainFrame))
menu4.add_command(label="Subnets", command=lambda: displaySubnets(mainFrame))
menu4.add_command(label="Routers", command=lambda: displayRouters(mainFrame))
menu4.add_command(label="Floating IPs", command=lambda: displayFloatingIPs(mainFrame))
menu4.add_command(label="Ports", command=lambda: displayPorts(mainFrame))
menu4.add_command(label="Network Agents", command=lambda: displayNetworkAgents(mainFrame))
menu4.add_command(label="Security Groups", command=lambda: displaySecurityGroups(mainFrame))

menu5 = Menu(menubar, tearoff=0)
menubar.add_cascade(label="Orchestration", menu=menu5)
menu5.add_command(label="Stacks", command= lambda: displayStacks(mainFrame))




#  ***Connection***


#Connection Frame
lf = LabelFrame(window, text="Connection Form", bd=3)
lf.pack(fill="both", expand="yes",padx=5, pady=5)


#Auth_URL input
labelAuthURL = Label(lf, text="Auth_URL", bg="grey")
labelAuthURL.pack(pady=10)
valueAuthURL = StringVar()
valueAuthURL.set("http://172.17.8.3:5000/v3")
entryAuthURL = Entry(lf, textvariable=valueAuthURL, width=30,fg="red",bd=5)
entryAuthURL.pack()

#Username input
labelUser = Label(lf, text="Username", bg="grey")
labelUser.pack(pady=10)
valueUser = StringVar()
valueUser.set("admin")
entryUser = Entry(lf, textvariable=valueUser, width=20,fg="red",bd=5)
entryUser.pack()

#Password input
labelPass = Label(lf, text="Password", bg="grey")
labelPass.pack(pady=10)
valuePass = StringVar()
valuePass.set("4793ae9444c44505")
entryPass = Entry(lf, textvariable=valuePass, width=20,fg="red",bd=5,show="*")
entryPass.pack()

#Project_Name input
labelProjectName = Label(lf, text="Project Name", bg="grey")
labelProjectName.pack(pady=10)
valueProjectName = StringVar()
valueProjectName.set("admin")
entryProjectName = Entry(lf, textvariable=valueProjectName, width=20,fg="red",bd=5)
entryProjectName.pack()

#Region_Name input
labelRegionName = Label(lf, text="Region Name", bg="grey")
labelRegionName.pack(pady=10)
valueRegionName = StringVar()
valueRegionName.set("RegionOne")
entryRegionName = Entry(lf, textvariable=valueRegionName, width=20,fg="red",bd=5)
entryRegionName.pack()

#User Domain Name input
labelUserDomain = Label(lf, text="User Domain Name", bg="grey")
labelUserDomain.pack(pady=10)
valueUserDomain = StringVar()
valueUserDomain.set("Default")
entryUserDomain = Entry(lf, textvariable=valueUserDomain, width=20,fg="red",bd=5)
entryUserDomain.pack()

#Project Domain Name input
labelProjectDomain = Label(lf, text="Project Domain Name", bg="grey")
labelProjectDomain.pack(pady=10)
valueProjectDomain = StringVar()
valueProjectDomain.set("Default")
entryProjectDomain = Entry(lf, textvariable=valueProjectDomain, width=20,fg="red",bd=5)
entryProjectDomain.pack()

def importKeystone():
    global conn
    filename = askopenfilename(title="Ouvrir votre document",filetypes=[('txt files','.txt'),('all files','.*')])
    fichier = open(filename, "r")
    lignes = fichier.readlines()
    username=""
    password=""
    region=""
    auth=""
    project_name=""
    user_domain_name=""
    project_domain_name=""
    for ligne in lignes:
        if "USERNAME" in ligne:
            username = ligne.split("USERNAME=",1)[1][:-1]
        elif "PASSWORD" in ligne:
            password = (ligne.split("PASSWORD='",1)[1])[:-2]
        elif "REGION_NAME" in ligne:
            region = ligne.split("REGION_NAME=",1)[1][:-1]
        elif "AUTH_URL" in ligne:
            auth = ligne.split("AUTH_URL=",1)[1][:-1]
        elif "PROJECT_NAME" in ligne:
            project_name = ligne.split("PROJECT_NAME=",1)[1][:-1]
        elif "USER_DOMAIN_NAME" in ligne:
            user_domain_name = ligne.split("USER_DOMAIN_NAME=",1)[1][:-1]
        elif "PROJECT_DOMAIN_NAME" in ligne:
            project_domain_name = ligne.split("PROJECT_DOMAIN_NAME=",1)[1][:-1]
    OSConnection(auth,region,project_name,username,password,user_domain_name,project_domain_name)
    

#DBinit  
dbInit = BooleanVar(value=False)  
checkDB = Checkbutton(lf, text="First Launch ? Please check the box to initialize the database before connecting", fg='red', 
variable=dbInit, onvalue=True, offvalue=False)
checkDB.pack(padx=10, pady=5)

#Connection buttons
connButton=Button(lf,text="Connect", command=lambda: OSConnection(valueAuthURL.get(),valueRegionName.get(),
valueProjectName.get(),valueUser.get(),valuePass.get(),valueUserDomain.get(),valueProjectDomain.get())) 
connButton.pack(padx=20,pady=10, side=RIGHT)
importButton=Button(lf,text="Import keystonerc_admin", command=lambda:importKeystone()) 
importButton.pack(padx=20,pady=10, side=LEFT)




    
def OSConnection(auth_url, region, project_name, username, password,
                      user_domain, project_domain):
    global conn, dbInit
    conn = osconn.createConnection(
        auth_url,
        region,
        project_name,
        username,
        password,
        user_domain,
        project_domain)

    lf.destroy()
    #w, h = window.winfo_screenwidth(), window.winfo_screenheight()
    #window.geometry("%dx%d+0+0" % (w, h))
    window.geometry('1920x1080')
    #window.attributes("-fullscreen", 1)
    window.resizable(True, True)
    window.config(menu=menubar)
    check.pack(anchor="e")
    mainFrame.pack(fill="both", expand=True ,padx=5, pady=5)
    if dbInit.get():
        showinfo(title="Database initialization", message="Please Wait During Database Initialization")
        database_init.initDatabase(conn)
    displayMain(mainFrame)



#Clear MainFrame   
def clearMainFrame(mainFrame):
    for widget in mainFrame.winfo_children():
        widget.destroy()
    for widget in window.winfo_children():
        if isinstance(widget, OptionMenu) or isinstance(widget, Label) or isinstance(widget, Button):
            widget.destroy()
    
#Stop Thread
def stopThread():
    thread.stop_thread = True

#***DISPLAY***


#Display DATA


def displayMain(mainFrame, project=""):
    clearMainFrame(mainFrame)

    
    #Thread
    thread.stop_thread = False
    thread_1 = thread.CollectData1(conn)
    thread_2 = thread.CollectData2(conn)
    thread_1.start()
    thread_2.start()



    #Projects
    mainFrame.columnconfigure(0, weight=1)
    #mainFrame.rowconfigure(0, weight=1)
    listProjects = []
    projectCursor=osdata.dbconn.execute("SELECT NAME FROM PROJECTS")
    for row in projectCursor:
        listProjects.append(row[0])
    projectLabel = Label(window, text="SELECT PROJECT", fg='red')
    projectVar = StringVar()
    if project == "":
        projectVar.set(listProjects[0])
    else:
        projectVar.set(project)
    projectSelector = OptionMenu(window, projectVar, listProjects[0], *listProjects[1:len(listProjects)])
    projectLabel.pack(side='left', padx=5)
    projectSelector.pack(side='left', padx=5)
    goButton=Button(window, text="Go", command=lambda: displayMain(mainFrame, projectVar.get()))
    goButton.pack(padx = 5, side = 'left')
    
    

    #User
    mainFrame.columnconfigure(1, weight=1) 
    #mainFrame.rowconfigure(0, weight=1)
    userFrame = Frame(mainFrame, width=200, height=200)
    userFrame.grid(column=1, row=0, padx=5, pady=5)
    #window.rowconfigure(0, weight=1)
    userLabel = Label(userFrame, text="USERS")
    usertab = Treeview(userFrame, selectmode="extended", columns=('Name'))
    usertab.heading('Name', text='Name')
    usertab['show'] = 'headings'
    userLabel.pack()
    #usertab.grid(column=10, row=3, padx = 5, pady = 5)
    usertab.pack(expand=YES, fill=BOTH, padx = 5, pady = 5)
    userCursor = osdata.dbconn.execute("SELECT NAME FROM USERS WHERE PROJECT=?", (projectVar.get(),))
    userid=0
    for row in userCursor:
        usertab.insert('', 'end', iid=userid, values=(row[0]))
        userid +=1

    #Server
    mainFrame.columnconfigure(2, weight=1)
    #mainFrame.rowconfigure(0, weight=1)
    serverFrame = Frame(mainFrame, width=200, height=200)
    serverFrame.grid(column=2, row=0, padx=5, pady=5)
    serverLabel = Label(serverFrame, text="SERVERS")
    servertab = Treeview(serverFrame, selectmode="extended", columns=('Name', 'User_id', 'Image', 'ip_private', 'ip_public', 'Status'))
    servertab.heading('Name', text='Name')
    servertab.heading('User_id', text='Owner')
    servertab.heading('Image', text='Image')
    servertab.heading('ip_private', text='Private IP')
    servertab.heading('ip_public', text='Floating IP')
    servertab.heading('Status', text='Status')
    servertab['show'] = 'headings'
    serverLabel.pack()
    servertab.pack(expand=YES, fill=BOTH, padx = 5, pady = 5)
    serverCursor = osdata.dbconn.execute("SELECT NAME,USER,IMAGE,PRIVATE_IP,PUBLIC_IP,STATUS FROM SERVERS WHERE PROJECT=?", (projectVar.get(),))
    serverid=0
    for row in serverCursor:
        servertab.insert('', 'end', iid=serverid, values=(row[0], row[1], row[2], row[3], row[4], row[5]))
        serverid +=1
    
    #Network
    #mainFrame.rowconfigure(1, weight=1)
    #mainFrame.columnconfigure(1, weight=1)
    netFrame = Frame(mainFrame, width=200, height=200)
    netFrame.grid(column=1, row=1, padx=5, pady=5)
    netLabel = Label(netFrame, text="NETWORKS")
    nettab = Treeview(netFrame, selectmode="extended", columns=('Name', 'Network_type', 'Status'))
    nettab.heading('Name', text='Name')
    nettab.heading('Network_type', text='Network Type')
    nettab.heading('Status', text='Status')
    nettab['show'] = 'headings'
    netLabel.pack()
    nettab.pack(expand=YES, fill=BOTH, padx = 5, pady = 5)
    netCursor = osdata.dbconn.execute("SELECT NAME,NETWORK_TYPE,STATUS FROM NETWORKS WHERE PROJECT=?", (projectVar.get(),))
    netid=0
    for row in netCursor:
        nettab.insert('', 'end', iid=netid, values=(row[0], row[1], row[2]))
        netid +=1

    #Subnet
    subFrame = Frame(mainFrame, width=200, height=200)
    subFrame.grid(column=2, row=1, padx=5, pady=5)
    subLabel = Label(subFrame, text="SUBNETS")
    subtab = Treeview(subFrame, selectmode="extended", columns=('Name', 'Network_id', 'ipv6_address_mode', 'ipv6_ra_mode', 'CIDR', 'Gateway'))
    subtab.heading('Name', text='Name')
    subtab.heading('Network_id', text='Network')
    subtab.heading('ipv6_address_mode', text='IPv6 Addr Mode')
    subtab.heading('ipv6_ra_mode', text='IPv6 Router Advert Mode')
    subtab.heading('CIDR', text='CIDR')
    subtab.heading('Gateway', text='Gateway IP')
    subtab['show'] = 'headings'
    subLabel.pack()
    subtab.pack(expand=YES, fill=BOTH, padx = 5, pady = 5)
    subCursor = osdata.dbconn.execute("SELECT NAME,NETWORK,IPV6_ADDR,IPV6_RA,CIDR,GATEWAY FROM SUBNETS WHERE PROJECT=?", (projectVar.get(),))
    subid=0
    for row in subCursor:
        subtab.insert('', 'end', iid=subid, values=(row[0], row[1], row[2], row[3], row[4], row[5]))
        subid +=1

    #Router
    #mainFrame.rowconfigure(2, weight=1)
    #mainFrame.columnconfigure(0, weight=1)
    routerFrame = Frame(mainFrame, width=200, height=200)
    routerFrame.grid(column=1, row=3, padx=5, pady=5)
    routerLabel = Label(routerFrame, text="ROUTERS")
    routertab = Treeview(routerFrame, selectmode="extended", columns=('Name', 'External_gateway', 'Status'))
    routertab.heading('Name', text='Name')
    routertab.heading('External_gateway', text='External Gateway')
    routertab.heading('Status', text='Status')
    routertab['show'] = 'headings'
    routerLabel.pack()
    routertab.pack(expand=YES, fill=BOTH, padx = 5, pady = 5)
    routerCursor = osdata.dbconn.execute("SELECT NAME,NETWORK,STATUS FROM ROUTERS WHERE PROJECT=?", (projectVar.get(),))
    routerid=0
    for row in routerCursor:
        routertab.insert('', 'end', iid=routerid, values=(row[0], row[1], row[2]))
        routerid +=1

    #Floating IP
    ipFrame = Frame(mainFrame, width=200, height=200)
    ipFrame.grid(column=2, row=3, padx=5, pady=5)
    ipLabel = Label(ipFrame, text="FLOATING IPS")
    iptab = Treeview(ipFrame, selectmode="extended", columns=('Server', 'floating_ip_address', 'fixed_ip_address', 'floating_network_id', 'router_id', 'status'))
    iptab.heading('Server', text='Server')
    iptab.heading('floating_ip_address', text='Floating IP')
    iptab.heading('fixed_ip_address', text='Fixed IP')
    iptab.heading('floating_network_id', text='Network')
    iptab.heading('router_id', text='Router')
    iptab.heading('status', text='Status')
    iptab['show'] = 'headings'
    ipLabel.pack()
    iptab.pack(expand=YES, fill=BOTH, padx = 5, pady = 5)
    ipCursor = osdata.dbconn.execute("SELECT SERVER,FLOATING_IP_ADDR,FIXED_IP_ADDR,NETWORK,ROUTER,STATUS FROM FLOATING_IPS WHERE PROJECT=?", (projectVar.get(),))
    ipid=0
    for row in ipCursor:
        iptab.insert('', 'end', iid=ipid, values=(row[0], row[1], row[2], row[3], row[4], row[5]))
        ipid +=1



def displayProjects(mainFrame):
    global conn, addButton, deleteButton, monitor
    clearMainFrame(mainFrame)
    if osdata.getProjectsData:
        osdata.listProjects(conn)
        osdata.setProjectData(False)
    tab = Treeview(mainFrame, selectmode="extended", columns=('Name', 'Description'))
    scroll = Scrollbar(tab, orient="vertical", command=tab.yview)
    scroll.pack(side='right', fill='y')
    tab.configure(yscrollcommand=scroll.set)
    hscroll = Scrollbar(tab, orient="horizontal", command=tab.xview)
    hscroll.pack(side='bottom', fill='x')
    tab.configure(xscrollcommand=hscroll.set)
    tab.heading('Name', text='Name')
    tab.heading('Description', text='Description')
    tab['show'] = 'headings'
    tab.pack(expand=YES, fill=BOTH, padx = 5, pady = 5)
    id = 0
    lselect = []
    cursor = osdata.dbconn.execute("SELECT * from PROJECTS")
    for row in cursor:
        tab.insert('', 'end', iid=id, values=(row[1], row[2]))
        lselect.append(row[1])
        id += 1
    controlVar = StringVar(mainFrame)
    controlVar.set(lselect[0])
    selector = OptionMenu(mainFrame, controlVar, lselect[0], *lselect[1:len(lselect)])
    selector.pack(padx = 10, pady = 10, side = 'left')
    addButton=Button(mainFrame, text="Add", command= lambda : addProject())
    deleteButton=Button(mainFrame, text="Delete", command=lambda: deleteProject(osdata.dbconn.execute("SELECT ID from PROJECTS WHERE NAME=?", (controlVar.get(),)).fetchone()[0]))
    setButtons(monitor)
    refreshButton=Button(mainFrame, text="Refresh", command=lambda:[osdata.setProjectData(True), displayProjects(mainFrame)])
    refreshButton.pack(padx = 10, pady = 10, side = 'right')  


    
def displayUsers(mainFrame):
    global conn, addButton, deleteButton, monitor
    clearMainFrame(mainFrame)
    if osdata.getUsersData:
        osdata.listUsers(conn)
        osdata.setUserData(False)
    tab = Treeview(mainFrame, selectmode="extended", columns=('Name', 'Description', 'Project'))
    scroll = Scrollbar(tab, orient="vertical", command=tab.yview)
    scroll.pack(side='right', fill='y')
    tab.configure(yscrollcommand=scroll.set)
    hscroll = Scrollbar(tab, orient="horizontal", command=tab.xview)
    hscroll.pack(side='bottom', fill='x')
    tab.configure(xscrollcommand=hscroll.set)
    tab.heading('Name', text='Name')
    tab.heading('Description', text='Description')
    tab.heading('Project', text='Project')
    tab['show'] = 'headings'
    tab.pack(expand=YES, fill=BOTH, padx = 5, pady = 5)
    id = 0
    lselect = []
    cursor = osdata.dbconn.execute("SELECT * from USERS")
    for row in cursor:
        tab.insert('', 'end', iid=id, values=(row[1], row[2], row[3]))
        lselect.append(row[1])
        id += 1
    controlVar = StringVar(mainFrame)
    controlVar.set(lselect[0])
    selector = OptionMenu(mainFrame, controlVar, lselect[0], *lselect[1:len(lselect)])
    selector.pack(padx = 10, pady = 10, side = 'left')
    addButton=Button(mainFrame, text="Add", command=lambda: addUser())
    deleteButton=Button(mainFrame, text="Delete", command=lambda: deleteUser(osdata.dbconn.execute("SELECT ID from USERS WHERE NAME=?", (controlVar.get(),)).fetchone()[0]))
    setButtons(monitor)
    refreshButton=Button(mainFrame, text="Refresh", command=lambda: [osdata.setUserData(True), displayUsers(mainFrame)])
    refreshButton.pack(padx = 10, pady = 10, side = 'right')



def displayNetworks(mainFrame):
    global conn, addButton, deleteButton, monitor
    clearMainFrame(mainFrame)
    if osdata.getNetworksData:
        osdata.listNetworks(conn)
        osdata.setNetworkData(False)
    tab = Treeview(mainFrame, selectmode="extended", columns=('Created_at', 'Name', 'Project', 'Network_type', 'Subnets', 'is_router_external','mtu','is_vlan_transparent', 'Status'))
    scroll = Scrollbar(tab, orient="vertical", command=tab.yview)
    scroll.pack(side='right', fill='y')
    tab.configure(yscrollcommand=scroll.set)
    hscroll = Scrollbar(tab, orient="horizontal", command=tab.xview)
    hscroll.pack(side='bottom', fill='x')
    tab.configure(xscrollcommand=hscroll.set)
    tab.heading('Created_at', text='Created at')
    tab.heading('Name', text='Name')
    tab.heading('Project', text='Project')
    tab.heading('Network_type', text='Network Type')
    tab.heading('Subnets', text='Subnets')
    tab.heading('is_router_external', text='Is Router External')
    tab.heading('mtu', text='MTU')
    tab.heading('is_vlan_transparent', text='Is VLAN Transparent')
    tab.heading('Status', text='Status')
    tab['show'] = 'headings'
    tab.pack(expand=YES, fill=BOTH, padx = 5, pady = 5)
    id = 0
    lselect = []
    cursor = osdata.dbconn.execute("SELECT * from NETWORKS")
    for row in cursor:
        tab.insert('', 'end', iid=id, values=(row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9]))
        lselect.append(row[2])
        id += 1
    controlVar = StringVar(mainFrame)
    controlVar.set(lselect[0])
    selector = OptionMenu(mainFrame, controlVar, lselect[0], *lselect[1:len(lselect)])
    selector.pack(padx = 10, pady = 10, side = 'left')
    subnetsButton=Button(mainFrame, text="Subnets Details", command=lambda: subnetsDetails(osdata.getNetworkSubnetsIDs(osdata.dbconn.execute("SELECT ID from NETWORKS WHERE NAME=?", 
    (controlVar.get(),)).fetchone()[0], conn)))
    subnetsButton.pack(padx = 10, pady = 10, side = 'left')
    addButton=Button(mainFrame, text="Add", command=lambda: addNetwork())
    deleteButton=Button(mainFrame, text="Delete", command=lambda: deleteNetwork(osdata.dbconn.execute("SELECT ID from NETWORKS WHERE NAME=?", (controlVar.get(),)).fetchone()[0]))
    setButtons(monitor)
    refreshButton=Button(mainFrame, text="Refresh", command=lambda: [osdata.setNetworkData(True), displayNetworks(mainFrame)])
    refreshButton.pack(padx = 10, pady = 10, side = 'right')    



def displayFloatingIPs(mainFrame):
    global conn, addButton, deleteButton, monitor
    clearMainFrame(mainFrame)
    if osdata.getFloatingIPsData:
        osdata.listFloatingIPs(conn)
        osdata.setFloatingIPData(False)
    tab = Treeview(mainFrame, selectmode="extended", columns=('Created_at', 'project_id','Server', 'floating_ip_address', 'fixed_ip_address', 'floating_network_id', 'router_id', 'status'))
    scroll = Scrollbar(tab, orient="vertical", command=tab.yview)
    scroll.pack(side='right', fill='y')
    tab.configure(yscrollcommand=scroll.set)
    hscroll = Scrollbar(tab, orient="horizontal", command=tab.xview)
    hscroll.pack(side='bottom', fill='x')
    tab.configure(xscrollcommand=hscroll.set)
    tab.heading('Created_at', text='Created at')
    tab.heading('project_id', text='Project')
    tab.heading('Server', text='Server')
    tab.heading('floating_ip_address', text='Floating IP')
    tab.heading('fixed_ip_address', text='Fixed IP')
    tab.heading('floating_network_id', text='Network')
    tab.heading('router_id', text='Router')
    tab.heading('status', text='Status')
    tab['show'] = 'headings'
    tab.pack(expand=YES, fill=BOTH, padx = 5, pady = 5)
    id = 0
    lselect = []
    cursor = osdata.dbconn.execute("SELECT * from FLOATING_IPS")
    for row in cursor:
        tab.insert('', 'end', iid=id, values=(row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8]))
        lselect.append(row[4])
        id += 1
    controlVar = StringVar(mainFrame)
    controlVar.set(lselect[0])
    selector = OptionMenu(mainFrame, controlVar, lselect[0], *lselect[1:len(lselect)])
    selector.pack(padx = 10, pady = 10, side = 'left')
    serverButton=Button(mainFrame, text="Server Details", command=lambda: floatingIPServerDetails(controlVar.get()))
    serverButton.pack(padx = 10, pady = 10, side = 'left')
    networkButton=Button(mainFrame, text="Network Details", command=lambda: networkDetails(osdata.dbconn.execute("SELECT ID FROM NETWORKS WHERE NAME=(SELECT NETWORK FROM FLOATING_IPS WHERE FLOATING_IP_ADDR=?)", 
    (controlVar.get(),)).fetchone()[0]))
    networkButton.pack(padx = 10, pady = 10, side = 'left')
    routerButton=Button(mainFrame, text="Router Details", command=lambda: floatingIPRouterDetails(osdata.dbconn.execute("SELECT ID FROM ROUTERS WHERE NAME=(SELECT ROUTER FROM FLOATING_IPS WHERE FLOATING_IP_ADDR=?)",
    (controlVar.get(),)).fetchone()[0]))
    routerButton.pack(padx = 10, pady = 10, side = 'left')
    portButton=Button(mainFrame, text="Port Details", command=lambda: floatingIPPortDetails(osdata.dbconn.execute("SELECT PORT_ID FROM FLOATING_IPS WHERE FLOATING_IP_ADDR=?",
    (controlVar.get(),)).fetchone()[0]))
    portButton.pack(padx = 10, pady = 10, side = 'left')
    deleteButton=Button(mainFrame, text="Delete", command=lambda: deleteFloatingIP(osdata.dbconn.execute("SELECT ID from FLOATING_IPS WHERE FLOATING_IP_ADDR=?", 
    (controlVar.get(),)).fetchone()[0]))
    setButtons(monitor)
    refreshButton=Button(mainFrame, text="Refresh", command=lambda: [osdata.setFloatingIPData(True), displayFloatingIPs(mainFrame)])
    refreshButton.pack(padx = 10, pady = 10, side = 'right')
    


def displaySubnets(mainFrame):
    global conn, addButton, deleteButton, monitor
    clearMainFrame(mainFrame)
    if osdata.getSubnetsData:
        osdata.listSubnets(conn)
        osdata.setSubnetData(False)
    tab = Treeview(mainFrame, selectmode="extended", columns=('Created_at', 'Name', 'Project_id', 'Network_id', 'ip_version', 'ipv6_address_mode', 'ipv6_ra_mode', 'is_dhcp_enabled', 
    'CIDR', 'AllocationPool_Start', 'AllocationPool_End', 'DNS', 'Gateway'))
    scroll = Scrollbar(tab, orient="vertical", command=tab.yview)
    scroll.pack(side='right', fill='y')
    tab.configure(yscrollcommand=scroll.set)
    hscroll = Scrollbar(tab, orient="horizontal", command=tab.xview)
    hscroll.pack(side='bottom', fill='x')
    tab.configure(xscrollcommand=hscroll.set)
    tab.heading('Created_at', text='Created at')
    tab.heading('Name', text='Name')
    tab.heading('Project_id', text='Project')
    tab.heading('Network_id', text='Network')
    tab.heading('ip_version', text='IP Version')
    tab.heading('ipv6_address_mode', text='IPv6 Addr Mode')
    tab.heading('ipv6_ra_mode', text='IPv6 Router Advert Mode')
    tab.heading('is_dhcp_enabled', text='Is DHCP Enabled')
    tab.heading('CIDR', text='CIDR')
    tab.heading('AllocationPool_Start', text='Allocation Pool Start')
    tab.heading('AllocationPool_End', text='Allocation Pool End')
    tab.heading('DNS', text='DNS')
    tab.heading('Gateway', text='Gateway IP')
    tab['show'] = 'headings'
    tab.pack(expand=YES, fill=BOTH, padx = 5, pady = 5)
    id = 0
    lselect = []
    cursor = osdata.dbconn.execute("SELECT * from SUBNETS")
    for row in cursor:
        tab.insert('', 'end', iid=id, values=(row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9], row[10], row[11], row[12], row[13]))
        lselect.append(row[2])
        id += 1
    controlVar = StringVar(mainFrame)
    controlVar.set(lselect[0])
    selector = OptionMenu(mainFrame, controlVar, lselect[0], *lselect[1:len(lselect)])
    selector.pack(padx = 10, pady = 10, side = 'left')
    networkButton=Button(mainFrame, text="Network Details", command=lambda: networkDetails(conn.get_subnet_by_id(osdata.dbconn.execute("SELECT ID from SUBNETS WHERE NAME=?", 
    (controlVar.get(),)).fetchone()[0]).network_id))
    networkButton.pack(padx = 10, pady = 10, side = 'left')
    addButton=Button(mainFrame, text="Add", command=lambda: addSubnet())
    deleteButton=Button(mainFrame, text="Delete", command=lambda: deleteSubnet(osdata.dbconn.execute("SELECT ID from SUBNETS WHERE NAME=?", (controlVar.get(),)).fetchone()[0]))
    setButtons(monitor)
    refreshButton=Button(mainFrame, text="Refresh", command=lambda: [osdata.setSubnetData(True), displaySubnets(mainFrame)])
    refreshButton.pack(padx = 10, pady = 10, side = 'right')



def displayRouters(mainFrame):
    global conn, addButton, deleteButton, monitor
    clearMainFrame(mainFrame)
    if osdata.getRoutersData:
        osdata.listRouters(conn)
        osdata.setRouterData(False)
    tab = Treeview(mainFrame, selectmode="extended", columns=('Created_at', 'Name', 'Project_id', 'External_gateway', 'is_admin_state_up', 'is_distributed', 'Status'))
    scroll = Scrollbar(tab, orient="vertical", command=tab.yview)
    scroll.pack(side='right', fill='y')
    tab.configure(yscrollcommand=scroll.set)
    hscroll = Scrollbar(tab, orient="horizontal", command=tab.xview)
    hscroll.pack(side='bottom', fill='x')
    tab.configure(xscrollcommand=hscroll.set)
    tab.heading('Created_at', text='Created at')
    tab.heading('Name', text='Name')
    tab.heading('Project_id', text='Project')
    tab.heading('External_gateway', text='External Gateway')
    tab.heading('is_admin_state_up', text='Is Admin State Up')
    tab.heading('is_distributed', text='Is Distributed')
    tab.heading('Status', text='Status')
    tab['show'] = 'headings'
    tab.pack(expand=YES, fill=BOTH, padx = 5, pady = 5)
    id = 0
    lselect = []
    cursor = osdata.dbconn.execute("SELECT * from ROUTERS")
    for row in cursor:
            tab.insert('', 'end', iid=id, values=(row[1], row[2], row[3], row[4], row[5], row[6], row[7]))
            lselect.append(row[2])
            id += 1
    controlVar = StringVar(mainFrame)
    controlVar.set(lselect[0])
    selector = OptionMenu(mainFrame, controlVar, lselect[0], *lselect[1:len(lselect)])
    selector.pack(padx = 10, pady = 10, side = 'left')
    networkButton=Button(mainFrame, text="Network Details", command=lambda: networkDetails(osdata.dbconn.execute("SELECT ID FROM NETWORKS WHERE NAME=(SELECT NETWORK FROM ROUTERS WHERE NAME=?)",
    (controlVar.get(),)).fetchone()[0]))
    networkButton.pack(padx = 10, pady = 10, side = 'left')
    addButton=Button(mainFrame, text="Add", command=lambda: addRouter())
    deleteButton=Button(mainFrame, text="Delete", command=lambda: deleteRouter(osdata.dbconn.execute("SELECT ID from ROUTERS WHERE NAME=?", (controlVar.get(),)).fetchone()[0]))
    setButtons(monitor)
    refreshButton=Button(mainFrame, text="Refresh", command=lambda: [osdata.setRouterData(True), displayRouters(mainFrame)])
    refreshButton.pack(padx = 10, pady = 10, side = 'right')



def displayPorts(mainFrame):
    global conn, addButton, deleteButton, monitor
    clearMainFrame(mainFrame)
    if osdata.getPortsData:
        osdata.listPorts(conn)
        osdata.setPortData(False)
    tab = Treeview(mainFrame, selectmode="extended", columns=('Created_at', 'ID', 'Name', 'Project', 'Network_id', 'Fixed_ip', 'Subnets', 'device_owner', 'Mac_addr', 'Status'))
    scroll = Scrollbar(tab, orient="vertical", command=tab.yview)
    scroll.pack(side='right', fill='y')
    tab.configure(yscrollcommand=scroll.set)
    hscroll = Scrollbar(tab, orient="horizontal", command=tab.xview)
    hscroll.pack(side='bottom', fill='x')
    tab.configure(xscrollcommand=hscroll.set)
    tab.heading('Created_at', text='Created at')
    tab.heading('ID', text='ID')
    tab.heading('Name', text='Name')
    tab.heading('Project', text='Project')
    tab.heading('Network_id', text='Network')
    tab.heading('Fixed_ip', text='Fixed IPs')
    tab.heading('Subnets', text='Subnets')
    tab.heading('device_owner', text='Device Owner')
    tab.heading('Mac_addr', text='MAC')
    tab.heading('Status', text='Status')
    tab['show'] = 'headings'
    tab.pack(expand=YES, fill=BOTH, padx = 5, pady = 5)
    id = 0
    lselect = []
    cursor = osdata.dbconn.execute("SELECT * from PORTS")
    for row in cursor:
        tab.insert('', 'end', iid=id, values=(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9]))
        lselect.append(row[0])
        id += 1
    controlVar = StringVar(mainFrame)
    controlVar.set(lselect[0])
    selector = OptionMenu(mainFrame, controlVar, lselect[0], *lselect[1:len(lselect)])
    selector.pack(padx = 10, pady = 10, side = 'left')
    networkButton=Button(mainFrame, text="Network Details", command=lambda: networkDetails(osdata.dbconn.execute("SELECT ID FROM NETWORKS WHERE NAME=(SELECT NETWORK FROM PORTS WHERE ID=?)",
    (controlVar.get(),)).fetchone()[0]))
    networkButton.pack(padx = 10, pady = 10, side = 'left')
    subnetsButton=Button(mainFrame, text="Subnets Details", command=lambda: subnetsDetails(osdata.getPortSubnetsIDs(conn.get_port_by_id(controlVar.get()), conn)))
    subnetsButton.pack(padx = 10, pady = 10, side = 'left')
    addButton=Button(mainFrame, text="Add", command=lambda: addPort())
    deleteButton=Button(mainFrame, text="Delete", command=lambda: deletePort(controlVar.get()))
    setButtons(monitor)
    refreshButton=Button(mainFrame, text="Refresh", command=lambda:[osdata.setPortData(True), displayPorts(mainFrame)])
    refreshButton.pack(padx = 10, pady = 10, side = 'right')



def displayNetworkAgents(mainFrame):
    global conn
    clearMainFrame(mainFrame)
    if osdata.getNetworkAgentsData:
        osdata.listNetworkAgents(conn)
        osdata.setNetworkAgentData(False)
    tab = Treeview(mainFrame, selectmode="extended", columns=('Created_at', 'started_at', 'Agent_type', 'Host', 'is_alive', 'description',  'last_heartbeat_at'))
    scroll = Scrollbar(tab, orient="vertical", command=tab.yview)
    scroll.pack(side='right', fill='y')
    tab.configure(yscrollcommand=scroll.set)
    hscroll = Scrollbar(tab, orient="horizontal", command=tab.xview)
    hscroll.pack(side='bottom', fill='x')
    tab.configure(xscrollcommand=hscroll.set)
    tab.heading('Created_at', text='Created at')
    tab.heading('started_at', text='Started at')
    tab.heading('Agent_type', text='Agent Type')
    tab.heading('Host', text='Host')
    tab.heading('is_alive', text='Is Alive')
    tab.heading('description', text='Description')
    tab.heading('last_heartbeat_at', text='Last Heartbeat at')
    tab['show'] = 'headings'
    tab.pack(expand=YES, fill=BOTH, padx = 5, pady = 5)
    id = 0
    cursor = osdata.dbconn.execute("SELECT * from NETWORK_AGENTS")
    for row in cursor:
            tab.insert('', 'end', iid=id, values=(row[1], row[2], row[3], row[4], row[5], row[6], row[7]))
            id += 1
    refreshButton=Button(mainFrame, text="Refresh", command=lambda: [osdata.setNetworkAgentData(True), displayNetworkAgents(mainFrame)])
    refreshButton.pack(padx = 10, pady = 10, side = 'right')



def displayImages(mainFrame):
    global conn, deleteButton, monitor
    clearMainFrame(mainFrame)
    if osdata.getImagesData:
        osdata.listImages(conn)
        osdata.setImageData(False)
    tab = Treeview(mainFrame, selectmode="extended", columns=('Created_at', 'Name', 'Size', 'min_disk', 'min_ram', 'progress', 'Status'))
    scroll = Scrollbar(tab, orient="vertical", command=tab.yview)
    scroll.pack(side='right', fill='y')
    tab.configure(yscrollcommand=scroll.set)
    hscroll = Scrollbar(tab, orient="horizontal", command=tab.xview)
    hscroll.pack(side='bottom', fill='x')
    tab.configure(xscrollcommand=hscroll.set)
    tab.heading('Created_at', text='Created at')
    tab.heading('Name', text='Name')
    tab.heading('Size', text='Size')
    tab.heading('min_disk', text='Min Disk (Gio)')
    tab.heading('min_ram', text='Min Ram (Mio)')
    tab.heading('progress', text='Progress %')
    tab.heading('Status', text='Status')
    tab['show'] = 'headings'
    tab.pack(expand=YES, fill=BOTH, padx = 5, pady = 5)
    id = 0
    lselect = []
    cursor = osdata.dbconn.execute("SELECT * from IMAGES")
    for row in cursor:
            tab.insert('', 'end', iid=id, values=(row[1], row[2], row[3], row[4], row[5], row[6], row[7]))
            lselect.append(row[1])
            id += 1
    controlVar = StringVar(mainFrame)
    controlVar.set(lselect[0])
    selector = OptionMenu(mainFrame, controlVar, lselect[0], *lselect[1:len(lselect)])
    selector.pack(padx = 10, pady = 10, side = 'left')
    deleteButton=Button(mainFrame, text="Delete", command=lambda: deleteImage(osdata.dbconn.execute("SELECT ID FROM IMAGES WHERE NAME=?",
    (controlVar.get(),)).fetchone()[0]))
    setButtons(monitor)
    refreshButton=Button(mainFrame, text="Refresh", command=lambda: [osdata.setImageData(True), displayImages(mainFrame)])
    refreshButton.pack(padx = 10, pady = 10, side = 'right')



def displayServers(mainFrame):
    global conn, addButton, deleteButton, monitor
    clearMainFrame(mainFrame)
    if osdata.getServersData:
        osdata.listServers(conn)
        osdata.setServerData(False)
    tab = Treeview(mainFrame, selectmode="extended", columns=('ID', 'Created_at', 'launched_at', 'terminated_at', 'Name', 'Project_id', 'User_id', 'Image', 'hostname', 
    'hypervisor_hostname', 'instance_name', 'ip_private', 'ip_public', 'security_groups', 'progress', 'vm_state', 'Status'))
    scroll = Scrollbar(tab, orient="vertical", command=tab.yview)
    scroll.pack(side='right', fill='y')
    tab.configure(yscrollcommand=scroll.set)
    hscroll = Scrollbar(tab, orient="horizontal", command=tab.xview)
    hscroll.pack(side='bottom', fill='x')
    tab.configure(xscrollcommand=hscroll.set)
    tab.heading('ID', text='ID')
    tab.heading('Created_at', text='Created at')
    tab.heading('launched_at', text='Launched at')
    tab.heading('terminated_at', text='Terminated at')
    tab.heading('Name', text='Name')
    tab.heading('Project_id', text='Project')
    tab.heading('User_id', text='Owner')
    tab.heading('Image', text='Image')
    tab.heading('hostname', text='Hostname')
    tab.heading('hypervisor_hostname', text='Hypervisor Hostname')
    tab.heading('instance_name', text='Instance Name')
    tab.heading('ip_private', text='Private IP')
    tab.heading('ip_public', text='Floating IP')
    tab.heading('security_groups', text='Security Groups')
    tab.heading('progress', text='Progress %')
    tab.heading('vm_state', text='VM State')
    tab.heading('Status', text='Status')
    tab['show'] = 'headings'
    tab.pack(expand=YES, fill=BOTH, padx = 5, pady = 5)
    id = 0
    lselect = []
    cursor = osdata.dbconn.execute("SELECT * from SERVERS")
    for row in cursor:
        tab.insert('', 'end', iid=id, values=(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9], row[10], row[11], row[12], row[13], row[14], row[15], row[16]))
        lselect.append(row[0])
        id += 1
    controlVar = StringVar(mainFrame)
    controlVar.set(lselect[0])
    selector = OptionMenu(mainFrame, controlVar, lselect[0], *lselect[1:len(lselect)])
    selector.pack(padx = 10, pady = 10, side = 'left')
    imageButton=Button(mainFrame, text="Image Details", command=lambda: serverImageDetails(osdata.dbconn.execute("SELECT ID FROM IMAGES WHERE NAME=(SELECT IMAGE FROM SERVERS WHERE ID=?)",
    (controlVar.get(),)).fetchone()[0]))
    imageButton.pack(padx = 10, pady = 10, side = 'left')
    addButton=Button(mainFrame, text="Add", command=lambda: addServer())
    deleteButton=Button(mainFrame, text="Delete", command=lambda: deleteServer(controlVar.get()))
    setButtons(monitor)
    refreshButton=Button(mainFrame, text="Refresh", command=lambda: [osdata.setServerData(True), displayServers(mainFrame)])
    refreshButton.pack(padx = 10, pady = 10, side = 'right')
    


def displaySecurityGroups(mainFrame):
    global conn, addButton, deleteButton, monitor
    clearMainFrame(mainFrame)
    if osdata.getSecGroupsData:
        osdata.listSecGroup(conn)
        osdata.setSecGroupData(False)
    tab = Treeview(mainFrame, selectmode="extended", columns=('ID', 'Created_at', 'Name', 'Project'))
    scroll = Scrollbar(tab, orient="vertical", command=tab.yview)
    scroll.pack(side='right', fill='y')
    tab.configure(yscrollcommand=scroll.set)
    hscroll = Scrollbar(tab, orient="horizontal", command=tab.xview)
    hscroll.pack(side='bottom', fill='x')
    tab.configure(xscrollcommand=hscroll.set)
    tab.heading('ID', text='ID')
    tab.heading('Created_at', text='Created at')
    tab.heading('Name', text='Name')
    tab.heading('Project', text='Project')
    tab['show'] = 'headings'
    tab.pack(expand=YES, fill=BOTH, padx = 5, pady = 5)
    id = 0
    lselect = []
    cursor = osdata.dbconn.execute("SELECT * from SECURITY_GROUPS")
    for row in cursor:
        tab.insert('', 'end', iid=id, values=(row[0], row[1], row[2], row[3]))
        lselect.append(row[0])
        id += 1
    controlVar = StringVar(mainFrame)
    controlVar.set(lselect[0])
    selector = OptionMenu(mainFrame, controlVar, lselect[0], *lselect[1:len(lselect)])
    selector.pack(padx = 10, pady = 10, side = 'left')
    viewRulesButton=Button(mainFrame, text="View Security Group Rules", command=lambda: secGroupRules(controlVar.get()))
    viewRulesButton.pack(padx = 10, pady = 10, side = 'left')
    addButton=Button(mainFrame, text="Add", command=lambda: addSecGroup())
    deleteButton=Button(mainFrame, text="Delete", command=lambda: deleteSecGroup(controlVar.get()))
    setButtons(monitor)
    refreshButton=Button(mainFrame, text="Refresh", command=lambda: [osdata.setSecGroupData(True), displaySecurityGroups(mainFrame)])
    refreshButton.pack(padx = 10, pady = 10, side = 'right')



def displayKeyPairs(mainFrame):
    global conn
    clearMainFrame(mainFrame)
    if osdata.getKeyPairsData:
        osdata.listKeyPairs(conn)
        osdata.setKeyPairData(False)
    tab = Treeview(mainFrame, selectmode="extended", columns=('Created_at', 'Name', 'user_id', 'is_deleted', 'type'))
    scroll = Scrollbar(tab, orient="vertical", command=tab.yview)
    scroll.pack(side='right', fill='y')
    tab.configure(yscrollcommand=scroll.set)
    hscroll = Scrollbar(tab, orient="horizontal", command=tab.xview)
    hscroll.pack(side='bottom', fill='x')
    tab.configure(xscrollcommand=hscroll.set)
    tab.heading('Created_at', text='Created at')
    tab.heading('Name', text='Name')
    tab.heading('user_id', text='User')
    tab.heading('is_deleted', text='Is Deleted')
    tab.heading('type', text='Type')
    tab['show'] = 'headings'
    tab.pack(expand=YES, fill=BOTH, padx = 5, pady = 5)
    id = 0
    cursor = osdata.dbconn.execute("SELECT * from KEYPAIRS")
    for row in cursor:
            tab.insert('', 'end', iid=id, values=(row[1], row[2], row[3], row[4], row[5]))
            id += 1
    refreshButton=Button(mainFrame, text="Refresh", command=lambda: [osdata.setKeyPairData(True),displayKeyPairs(mainFrame)])
    refreshButton.pack(padx = 10, pady = 10, side = 'right')



def displayStacks(mainFrame):
    global conn
    clearMainFrame(mainFrame)
    if osdata.getStacksData:
        osdata.listStacks(conn)
        osdata.setStackData(False)
    tab = Treeview(mainFrame, selectmode="extended", columns=('Created_at', 'Name', 'Status'))
    scroll = Scrollbar(tab, orient="vertical", command=tab.yview)
    scroll.pack(side='right', fill='y')
    tab.configure(yscrollcommand=scroll.set)
    hscroll = Scrollbar(tab, orient="horizontal", command=tab.xview)
    hscroll.pack(side='bottom', fill='x')
    tab.configure(xscrollcommand=hscroll.set)
    tab.heading('Created_at', text='Created at')
    tab.heading('Name', text='Name')
    tab.heading('Status', text='Status')
    tab['show'] = 'headings'
    tab.pack(expand=YES, fill=BOTH, padx = 5, pady = 5)
    id = 0
    cursor = osdata.dbconn.execute("SELECT * from STACKS")
    for row in cursor:
            tab.insert('', 'end', iid=id, values=(row[1], row[2], row[3]))
            id += 1
    linkButton=Button(mainFrame, text="More Details with Horizon", command=lambda: webbrowser.open(valueAuthURL.get()))
    linkButton.pack(padx = 10, pady = 10, side = 'left')
    refreshButton=Button(mainFrame, text="Refresh", command=lambda: [osdata.setStackData(True),displayStacks(mainFrame)])
    refreshButton.pack(padx = 10, pady = 10, side = 'right')



#Display Details       


def floatingIPServerDetails(floating_ip):
    global conn
    windowDetail = Tk()
    windowDetail.title("OSupervisor")
    windowDetail.geometry('800x200')
    windowDetail.resizable(True, True)
    DetailFrame = LabelFrame(windowDetail, text="Server Details")
    DetailFrame.pack(fill="both", expand="yes",padx=10, pady=10)
    tab2 = Treeview(DetailFrame, selectmode="extended", columns=('Created_at', 'launched_at', 'terminated_at', 'Name', 'Project_id', 'User_id', 'Image', 'hostname', 
    'hypervisor_hostname', 'instance_name', 'ip_private', 'ip_public', 'security_groups', 'progress', 'vm_state', 'Status'))
    scroll = Scrollbar(tab2, orient="vertical", command=tab2.yview)
    scroll.pack(side='right', fill='y')
    tab2.configure(yscrollcommand=scroll.set)
    hscroll = Scrollbar(tab2, orient="horizontal", command=tab2.xview)
    hscroll.pack(side='bottom', fill='x')
    tab2.configure(xscrollcommand=hscroll.set)
    tab2.heading('Created_at', text='Created at')
    tab2.heading('launched_at', text='Launched at')
    tab2.heading('terminated_at', text='Terminated at')
    tab2.heading('Name', text='Name')
    tab2.heading('Project_id', text='Project')
    tab2.heading('User_id', text='Owner')
    tab2.heading('Image', text='Image')
    tab2.heading('hostname', text='Hostname')
    tab2.heading('hypervisor_hostname', text='Hypervisor Hostname')
    tab2.heading('instance_name', text='Instance Name')
    tab2.heading('ip_private', text='Private IP')
    tab2.heading('ip_public', text='Floating IP')
    tab2.heading('security_groups', text='Security Groups')
    tab2.heading('progress', text='Progress %')
    tab2.heading('vm_state', text='VM State')
    tab2.heading('Status', text='Status')
    tab2['show'] = 'headings'
    tab2.pack(expand=YES, fill=BOTH, padx = 5, pady = 5)
    row = osdata.dbconn.execute("SELECT * from SERVERS WHERE PUBLIC_IP=?", (floating_ip,)).fetchone()
    tab2.insert('', 'end', iid=0, values=(row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9], row[10], row[11], row[12], row[13], row[14], row[15], row[16]))
    windowDetail.mainloop()


def floatingIPRouterDetails(routerid):
    global conn
    windowDetail = Tk()
    windowDetail.title("OSupervisor")
    windowDetail.geometry('800x200')
    windowDetail.resizable(True, True)
    DetailFrame = LabelFrame(windowDetail, text="Network Details")
    DetailFrame.pack(fill="both", expand="yes",padx=10, pady=10)
    tab2 = Treeview(DetailFrame, selectmode="extended", columns=('Created_at', 'Name', 'Project_id', 'External_gateway', 'is_admin_state_up', 'is_distributed', 'Status'))
    scroll = Scrollbar(tab2, orient="vertical", command=tab2.yview)
    scroll.pack(side='right', fill='y')
    tab2.configure(yscrollcommand=scroll.set)
    hscroll = Scrollbar(tab2, orient="horizontal", command=tab2.xview)
    hscroll.pack(side='bottom', fill='x')
    tab2.configure(xscrollcommand=hscroll.set)
    tab2.heading('Created_at', text='Created at')
    tab2.heading('Name', text='Name')
    tab2.heading('Project_id', text='Project')
    tab2.heading('External_gateway', text='External Gateway')
    tab2.heading('is_admin_state_up', text='Is Admin State Up')
    tab2.heading('is_distributed', text='Is Distributed')
    tab2.heading('Status', text='Status')
    tab2['show'] = 'headings'
    tab2.pack(expand=YES, fill=BOTH, padx = 5, pady = 5)
    row = osdata.dbconn.execute("SELECT * from ROUTERS WHERE ID=?", (routerid,)).fetchone()
    tab2.insert('', 'end', iid=0, values=(row[1], row[2], row[3], row[4], row[5], row[6], row[7]))
    windowDetail.mainloop()

    
def floatingIPPortDetails(port_id):
    global conn
    windowDetail = Tk()
    windowDetail.title("OSupervisor")
    windowDetail.geometry('800x200')
    windowDetail.resizable(True, True)
    DetailFrame = LabelFrame(windowDetail, text="Network Details")
    DetailFrame.pack(fill="both", expand="yes",padx=10, pady=10)
    tab2 = Treeview(DetailFrame, selectmode="extended", columns=('Created_at', 'ID', 'Name', 'Project', 'Network_id', 'Fixed_ip', 'Subnets', 'device_owner', 'Mac_addr', 'Status'))
    scroll = Scrollbar(tab2, orient="vertical", command=tab2.yview)
    scroll.pack(side='right', fill='y')
    tab2.configure(yscrollcommand=scroll.set)
    hscroll = Scrollbar(tab2, orient="horizontal", command=tab2.xview)
    hscroll.pack(side='bottom', fill='x')
    tab2.configure(xscrollcommand=hscroll.set)
    tab2.heading('Created_at', text='Created at')
    tab2.heading('ID', text='ID')
    tab2.heading('Name', text='Name')
    tab2.heading('Project', text='Project')
    tab2.heading('Network_id', text='Network')
    tab2.heading('Fixed_ip', text='Fixed IPs')
    tab2.heading('Subnets', text='Subnets')
    tab2.heading('device_owner', text='Device Owner')
    tab2.heading('Mac_addr', text='MAC')
    tab2.heading('Status', text='Status')
    tab2['show'] = 'headings'
    tab2.pack(expand=YES, fill=BOTH, padx = 5, pady = 5)
    row = osdata.dbconn.execute("SELECT * from PORTS WHERE ID=?", (port_id,)).fetchone()
    tab2.insert('', 'end', iid=0, values=(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9]))
    windowDetail.mainloop()


def subnetsDetails(subnetids):
    global conn
    windowDetail = Tk()
    windowDetail.title("OSupervisor")
    windowDetail.geometry('800x200')
    windowDetail.resizable(True, True)
    DetailFrame = LabelFrame(windowDetail, text="Subnets Details")
    DetailFrame.pack(fill="both", expand="yes",padx=10, pady=10)
    tab2 = Treeview(DetailFrame, selectmode="extended", columns=('Created_at', 'Name', 'Project_id', 'Network_id', 'ip_version', 'ipv6_address_mode', 'ipv6_ra_mode', 
    'CIDR', 'AllocationPool', 'DNS', 'Gateway'))
    scroll = Scrollbar(tab2, orient="vertical", command=tab2.yview)
    scroll.pack(side='right', fill='y')
    tab2.configure(yscrollcommand=scroll.set)
    hscroll = Scrollbar(tab2, orient="horizontal", command=tab2.xview)
    hscroll.pack(side='bottom', fill='x')
    tab2.configure(xscrollcommand=hscroll.set)
    tab2.heading('Created_at', text='Created at')
    tab2.heading('Name', text='Name')
    tab2.heading('Project_id', text='Project')
    tab2.heading('Network_id', text='Network')
    tab2.heading('ip_version', text='IP Version')
    tab2.heading('ipv6_address_mode', text='IPv6 Addr Mode')
    tab2.heading('ipv6_ra_mode', text='IPv6 Router Advert Mode')
    tab2.heading('CIDR', text='CIDR')
    tab2.heading('AllocationPool', text='Allocation Pool')
    tab2.heading('DNS', text='DNS')
    tab2.heading('Gateway', text='Gateway IP')
    tab2['show'] = 'headings'
    tab2.pack(expand=YES, fill=BOTH, padx = 5, pady = 5)
    id = 0
    for sid in subnetids:
        row = osdata.dbconn.execute("SELECT * from SUBNETS WHERE ID=?", (sid,)).fetchone()
        tab2.insert('', 'end', iid=id, values=(row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9], row[10], row[11], row[12], row[13]))
        id += 1
    windowDetail.mainloop()


def networkDetails(netID):
    global conn
    windowDetail = Tk()
    windowDetail.title("OSupervisor")
    windowDetail.geometry('800x200')
    windowDetail.resizable(True, True)
    DetailFrame = LabelFrame(windowDetail, text="Network Details")
    DetailFrame.pack(fill="both", expand="yes",padx=10, pady=10)
    tab2 = Treeview(DetailFrame, selectmode="extended", columns=('Created_at', 'Name', 'Project', 'Network_type', 'Subnets', 'is_router_external','mtu','is_vlan_transparent', 'Status'))
    scroll = Scrollbar(tab2, orient="vertical", command=tab2.yview)
    scroll.pack(side='right', fill='y')
    tab2.configure(yscrollcommand=scroll.set)
    hscroll = Scrollbar(tab2, orient="horizontal", command=tab2.xview)
    hscroll.pack(side='bottom', fill='x')
    tab2.configure(xscrollcommand=hscroll.set)
    tab2.heading('Created_at', text='Created at')
    tab2.heading('Name', text='Name')
    tab2.heading('Project', text='Project')
    tab2.heading('Network_type', text='Network Type')
    tab2.heading('Subnets', text='Subnets')
    tab2.heading('is_router_external', text='Is Router External')
    tab2.heading('mtu', text='MTU')
    tab2.heading('is_vlan_transparent', text='Is VLAN Transparent')
    tab2.heading('Status', text='Status')
    tab2['show'] = 'headings'
    tab2.pack(expand=YES, fill=BOTH, padx = 5, pady = 5)
    row = osdata.dbconn.execute("SELECT * from NETWORKS WHERE ID=?", (netID,)).fetchone()
    tab2.insert('', 'end', iid=0, values=(row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9]))
    windowDetail.mainloop()


def serverImageDetails(imageid):
    global conn
    windowDetail = Tk()
    windowDetail.title("OSupervisor")
    windowDetail.geometry('800x200')
    windowDetail.resizable(True, True)
    DetailFrame = LabelFrame(windowDetail, text="Network Details")
    DetailFrame.pack(fill="both", expand="yes",padx=10, pady=10)
    tab2 = Treeview(DetailFrame, selectmode="extended", columns=('Created_at', 'Name', 'Size', 'min_disk', 'min_ram', 'progress', 'Status'))
    scroll = Scrollbar(tab2, orient="vertical", command=tab2.yview)
    scroll.pack(side='right', fill='y')
    tab2.configure(yscrollcommand=scroll.set)
    hscroll = Scrollbar(tab2, orient="horizontal", command=tab2.xview)
    hscroll.pack(side='bottom', fill='x')
    tab2.configure(xscrollcommand=hscroll.set)
    tab2.heading('Created_at', text='Created at')
    tab2.heading('Name', text='Name')
    tab2.heading('Size', text='Size')
    tab2.heading('min_disk', text='Min Disk (Gio)')
    tab2.heading('min_ram', text='Min Ram (Mio)')
    tab2.heading('progress', text='Progress %')
    tab2.heading('Status', text='Status')
    tab2['show'] = 'headings'
    tab2.pack(expand=YES, fill=BOTH, padx = 5, pady = 5)
    row = osdata.dbconn.execute("SELECT * from IMAGES WHERE ID=?", (imageid,)).fetchone()
    tab2.insert('', 'end', iid=0, values=(row[1], row[2], row[3], row[4], row[5], row[6], row[7]))
    windowDetail.mainloop()


def secGroupRules(secgroupid):
    global conn, createRuleButton, deleteRuleButton
    clearMainFrame(mainFrame)
    if osdata.getSecGroupRulesData:
        osdata.listSecGroupRules(conn)
        osdata.setSecGroupRuleData(False)
    tab2 = Treeview(mainFrame, selectmode="extended", columns=('rule_id', 'group_id', 'Created_at', 'project_id', 'direction', 'port_range_min', 'port_range_max', 'protocol', 'remote_ip_prefix'))
    scroll = Scrollbar(tab2, orient="vertical", command=tab2.yview)
    scroll.pack(side='right', fill='y')
    tab2.configure(yscrollcommand=scroll.set)
    hscroll = Scrollbar(tab2, orient="horizontal", command=tab2.xview)
    hscroll.pack(side='bottom', fill='x')
    tab2.configure(xscrollcommand=hscroll.set)
    tab2.heading('rule_id', text='ID')
    tab2.heading('group_id', text='Security Group ID')
    tab2.heading('Created_at', text='Created at')
    tab2.heading('project_id', text='Project')
    tab2.heading('direction', text='Direction')
    tab2.heading('port_range_min', text='Port Range Min')
    tab2.heading('port_range_max', text='Port Range Max')
    tab2.heading('protocol', text='Protocol')
    tab2.heading('remote_ip_prefix', text='Remote IP Prefix')
    tab2['show'] = 'headings'
    tab2.pack(expand=YES, fill=BOTH, padx = 5, pady = 5)
    id = 0
    ruleSelect = []
    cursor = osdata.dbconn.execute("SELECT * FROM SECURITY_GROUP_RULES WHERE SECURITY_GROUP_ID=?", (secgroupid,))
    for row in cursor:
        tab2.insert('', 'end', iid=id, values=(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8]))
        ruleSelect.append(row[0])
        id += 1
    ruleControlVar = StringVar(mainFrame)
    ruleControlVar.set(ruleSelect[0])
    selector = OptionMenu(mainFrame, ruleControlVar, ruleSelect[0], *ruleSelect[1:len(ruleSelect)])
    returnb = Button(mainFrame, text="Return", command= lambda : displaySecurityGroups(mainFrame))
    returnb.pack(padx=20,pady=20, side=LEFT)
    selector.pack(padx = 10, pady = 10, side = 'left')
    createRuleButton=Button(mainFrame, text="Create Security Group Rule", command=lambda: createRule(secgroupid))
    deleteRuleButton=Button(mainFrame, text="Delete Security Group Rule", command=lambda: deleteRule(ruleControlVar.get()))
    setButtons(monitor)





#Add item

def addProject():
    global conn
    clearMainFrame(mainFrame)
    
    #Project Name input
    labelName = Label(mainFrame, text="Project Name", bg="grey")
    labelName.pack(pady=10)
    valueName = StringVar()
    valueName.set("")
    entryName = Entry(mainFrame, textvariable=valueName, width=30, fg="red", bd=5)
    entryName.pack()
    
    #Description input
    labelDes = Label(mainFrame, text="Description", bg="grey")
    labelDes.pack(pady=10)
    valueDes = StringVar()
    valueDes.set("")
    entryDes = Entry(mainFrame, textvariable=valueDes, width=30, fg="red", bd=5)
    entryDes.pack()
    
    #DomainID input
    labelID = Label(mainFrame, text="Domain ID", bg="grey")
    labelID.pack(pady=10)
    valueID = StringVar()
    valueID.set("default")
    entryID = Entry(mainFrame, textvariable=valueID, width=30, fg="red", bd=5)
    entryID.pack()

    #Enabled input
    labelEnabled = Label(mainFrame, text="Enabled (True/False)", bg="grey")
    labelEnabled.pack(pady=10)
    valueEnabled = StringVar()
    valueEnabled.set("True")
    entryEnabled = Entry(mainFrame, textvariable=valueEnabled, width=30, fg="red", bd=5)
    entryEnabled.pack()
    
    #Add button
    addb = Button(mainFrame, text="Add Project", command= lambda : addProjectFunction(valueName.get(), valueDes.get(), valueEnabled.get(), valueID.get()))
    addb.pack(padx=20,pady=20, side=RIGHT)

    #Return button
    returnb = Button(mainFrame, text="Return", command= lambda : displayProjects(mainFrame))
    returnb.pack(padx=20,pady=20, side=LEFT)


def addProjectFunction(valueName, valueDes, valueEnabled, valueID):
    global conn
    name = valueName
    des = valueDes
    domainid = valueID
    enabled = valueEnabled
    cursor = osdata.dbconn.execute("SELECT NAME from PROJECTS")
    for row in cursor:
        if name == row[0]:
            showerror(title="ERROR", message="This Project Name already exists")
            return
            
    if name == "":
        showerror(title="ERROR", message="Project Name can not be empty")
        return
        
    else:
        if enabled == "True":
            enabled = True
        if enabled == "False":
            enabled = False
        conn.create_project(name, description=des, domain_id=domainid, enabled = enabled)
        osdata.setProjectData(True)
        displayProjects(mainFrame)


def addUser():
    global conn
    clearMainFrame(mainFrame)
    
    #User Name input
    labelName = Label(mainFrame, text="User Name", bg="grey")
    labelName.pack(pady=10)
    valueName = StringVar()
    valueName.set("")
    entryName = Entry(mainFrame, textvariable=valueName, width=30, fg="red", bd=5)
    entryName.pack()
    
    #Password input
    labelPass = Label(mainFrame, text="Password", bg="grey")
    labelPass.pack(pady=10)
    valuePass = StringVar()
    valuePass.set("")
    entryPass = Entry(mainFrame, textvariable=valuePass, width=30, fg="red", bd=5, show="*")
    entryPass.pack()
    
    #Email input
    labelEmail = Label(mainFrame, text="Email", bg="grey")
    labelEmail.pack(pady=10)
    valueEmail = StringVar()
    valueEmail.set("")
    entryEmail = Entry(mainFrame, textvariable=valueEmail, width=30, fg="red", bd=5)
    entryEmail.pack()

    #Project List
    labelProject = Label(mainFrame, text="Project", bg="grey")
    labelProject.pack(pady=10)
    projectList = []
    cursor = osdata.dbconn.execute("SELECT NAME from PROJECTS")
    for row in cursor:
        projectList.append(row[0])
    valueProject = StringVar()
    valueProject.set(projectList[0])
    selector = OptionMenu(mainFrame, valueProject, projectList[0], *projectList[1:len(projectList)])
    selector.pack()
    
    #Enabled input
    labelEnabled = Label(mainFrame, text="Enabled (True/False)", bg="grey")
    labelEnabled.pack(pady=10)
    valueEnabled = StringVar()
    valueEnabled.set("True")
    entryEnabled = Entry(mainFrame, textvariable=valueEnabled, width=30, fg="red", bd=5)
    entryEnabled.pack()

    #DomainID input
    labelID = Label(mainFrame, text="Domain ID", bg="grey")
    labelID.pack(pady=10)
    valueID = StringVar()
    valueID.set("default")
    entryID = Entry(mainFrame, textvariable=valueID, width=30, fg="red", bd=5)
    entryID.pack()

    #Description input
    labelDes = Label(mainFrame, text="Description", bg="grey")
    labelDes.pack(pady=10)
    valueDes = StringVar()
    valueDes.set("")
    entryDes = Entry(mainFrame, textvariable=valueDes, width=30, fg="red", bd=5)
    entryDes.pack()
    
    #Add button
    addb = Button(mainFrame, text="Add User", command= lambda : addUserFunction(valueName.get(), valuePass.get(), valueEmail.get(), valueProject.get(), 
    valueEnabled.get(), valueID.get(), valueDes.get()))
    addb.pack(padx=20,pady=20, side=RIGHT)

    #Return button
    returnb = Button(mainFrame, text="Return", command= lambda : displayUsers(mainFrame))
    returnb.pack(padx=20,pady=20, side=LEFT)


def addUserFunction(valueName, valuePass, valueEmail, valueProject, valueEnabled, valueID, valueDes):
    global conn
    project = osdata.dbconn.execute("SELECT ID from PROJECTS WHERE NAME=?", (valueProject,)).fetchone()[0]
    enabled = valueEnabled
    
    cursor = osdata.dbconn.execute("SELECT NAME from USERS")
    for row in cursor:
        if valueName == row[0]:
            showerror(title="ERROR", message="This User Name already exists")
            return
            
    if valueName == "":
        showerror(title="ERROR", message="User Name can not be empty")
        return
        
    else:
        if enabled == "True":
            enabled = True
        if enabled == "False":
            enabled = False
        print(project)
        conn.create_user(valueName, password=valuePass, email=valueEmail, enabled=enabled, domain_id=valueID, description=valueDes)
        conn.identity.assign_project_role_to_user(project, conn.get_user(valueName), conn.get_role("member"))
        osdata.setUserData(True)
        displayUsers(mainFrame)


def addServer():
    global conn
    clearMainFrame(mainFrame)
    
    #Server Name input
    labelName = Label(mainFrame, text="Server Name", bg="grey")
    labelName.pack(pady=10)
    valueName = StringVar()
    valueName.set("")
    entryName = Entry(mainFrame, textvariable=valueName, width=30, fg="red", bd=5)
    entryName.pack()
    
    #Flavor List
    labelFlavor = Label(mainFrame, text="Flavor", bg="grey")
    labelFlavor.pack(pady=10)
    flavorList = []
    for x in conn.list_flavors():
        flavorList.append(x.name)
    valueFlavor = StringVar()
    valueFlavor.set(flavorList[0])
    selector = OptionMenu(mainFrame, valueFlavor, flavorList[0], *flavorList[1:len(flavorList)])
    selector.pack()
    
    #Image List
    labelImage= Label(mainFrame, text="Image", bg="grey")
    labelImage.pack(pady=10)
    imageList = []
    cursor = osdata.dbconn.execute("SELECT NAME from IMAGES")
    for row in cursor:
        imageList.append(row[0])
    valueImage = StringVar()
    valueImage.set(imageList[0])
    selector = OptionMenu(mainFrame, valueImage, imageList[0], *imageList[1:len(imageList)])
    selector.pack()

    #Network List
    labelNetwork = Label(mainFrame, text="External Network", bg="grey")
    labelNetwork.pack(pady=10)
    networkList = []
    cursor = osdata.dbconn.execute("SELECT NAME from NETWORKS")
    for row in cursor:
        networkList.append(row[0])
    valueNetName = StringVar()
    valueNetName.set(networkList[0])
    selector = OptionMenu(mainFrame, valueNetName, networkList[0], *networkList[1:len(networkList)])
    selector.pack()

    #Add button
    addb = Button(mainFrame, text="Add Server", command= lambda : addServerFunction(valueName.get(), valueFlavor.get(), valueImage.get(), valueNetName.get()))
    addb.pack(padx=20,pady=20, side=RIGHT)

    #Return button
    returnb = Button(mainFrame, text="Return", command= lambda : displayServers(mainFrame))
    returnb.pack(padx=20,pady=20, side=LEFT)


def addServerFunction(valueName, valueFlavor, valueImage, valueNetName):
    global conn
    name = valueName
    flavor = conn.get_flavor(valueFlavor).id
    image = conn.get_image(valueImage).id
    network = osdata.dbconn.execute("SELECT ID FROM NETWORKS WHERE NAME=?", (valueNetName,)).fetchone()[0]
    
    cursor = osdata.dbconn.execute("SELECT NAME from SERVERS")
    for row in cursor:
        if name == row[0]:
            showerror(title="ERROR", message="This Server Name already exists")
            return
            
    if name == "":
        showerror(title="ERROR", message="Server Name can not be empty")
        return
        
    else:
        conn.create_server(name, flavor=flavor, image=image, network=network)
        osdata.setServerData(True)
        displayServers(mainFrame)


def addNetwork():
    global conn
    clearMainFrame(mainFrame)
    
    #Network Name input
    labelName = Label(mainFrame, text="Network Name", bg="grey")
    labelName.pack(pady=10)
    valueName = StringVar()
    valueName.set("")
    entryName = Entry(mainFrame, textvariable=valueName, width=30, fg="red", bd=5)
    entryName.pack()

    #Shared input
    labelShared = Label(mainFrame, text="Shared (True/False)", bg="grey")
    labelShared.pack(pady=10)
    valueShared = StringVar()
    valueShared.set("False")
    entryShared = Entry(mainFrame, textvariable=valueShared, width=30, fg="red", bd=5)
    entryShared.pack()

    #Admin State input
    labelAdminState = Label(mainFrame, text="Admin State Up (True/False)", bg="grey")
    labelAdminState.pack(pady=10)
    valueAdminState = StringVar()
    valueAdminState.set("True")
    entryAdminState = Entry(mainFrame, textvariable=valueAdminState, width=30, fg="red", bd=5)
    entryAdminState.pack()

    #External input
    labelExternal = Label(mainFrame, text="External (True/False)", bg="grey")
    labelExternal.pack(pady=10)
    valueExternal = StringVar()
    valueExternal.set("False")
    entryExternal = Entry(mainFrame, textvariable=valueExternal, width=30, fg="red", bd=5)
    entryExternal.pack()

    #Project List
    labelProject = Label(mainFrame, text="Project", bg="grey")
    labelProject.pack(pady=10)
    projectList = []
    cursor = osdata.dbconn.execute("SELECT NAME from PROJECTS")
    for row in cursor:
        projectList.append(row[0])
    valueProject = StringVar()
    valueProject.set(projectList[0])
    selector = OptionMenu(mainFrame, valueProject, projectList[0], *projectList[1:len(projectList)])
    selector.pack()
    
    #Add button
    addb = Button(mainFrame, text="Add Network", command= lambda : addNetworkFunction(valueName.get(), valueShared.get(), valueAdminState.get(), valueExternal.get(), 
    valueProject.get()))
    addb.pack(padx=20,pady=20, side=RIGHT)

    #Return button
    returnb = Button(mainFrame, text="Return", command= lambda : displayNetworks(mainFrame))
    returnb.pack(padx=20,pady=20, side=LEFT)


def addNetworkFunction(valueName, valueShared, valueAdminState, valueExternal, valueProject):
    global conn
    shared = valueShared
    adminstate = valueAdminState
    external = valueExternal
    project = osdata.dbconn.execute("SELECT ID from PROJECTS WHERE NAME=?", (valueProject,)).fetchone()[0]
    
    cursor = osdata.dbconn.execute("SELECT NAME from NETWORKS")
    for row in cursor:
        if valueName == row[0]:
            showerror(title="ERROR", message="This Network Name already exists")
            return
            
    if valueName == "":
        showerror(title="ERROR", message="Network Name can not be empty")
        return
        
    else:
        if shared == "True":
            shared = True
        else:
            shared = False
        if adminstate == "True":
            adminstate = True
        else:
            adminstate = False
        if external == "True":
            external = True
        else:
            external = False
        conn.create_network(valueName, shared=shared, admin_state_up=adminstate, external=external, project_id=project)
        osdata.setNetworkData(True)
        displayNetworks(mainFrame)


def addSubnet():
    global conn
    clearMainFrame(mainFrame)

    #Network List
    labelNetwork = Label(mainFrame, text="Network", bg="grey")
    labelNetwork.grid(row=0, column=0)
    networkList = []
    cursor = osdata.dbconn.execute("SELECT NAME from NETWORKS")
    for row in cursor:
        networkList.append(row[0])
    valueNetName = StringVar()
    valueNetName.set(networkList[0])
    selector = OptionMenu(mainFrame, valueNetName, networkList[0], *networkList[1:len(networkList)])
    selector.grid(row=1, column=0)

    #Subnet Name input
    labelSubName = Label(mainFrame, text="Subnet Name", bg="grey")
    labelSubName.grid(row=3, column=0)
    valueSubName = StringVar()
    valueSubName.set("")
    entrySubName = Entry(mainFrame, textvariable=valueSubName, width=30, fg="red", bd=5)
    entrySubName.grid(row=4, column=0)

    #CIDR input
    labelCidr = Label(mainFrame, text="CIDR (ex: 192.168.0.0/16, fc00::/64)", bg="grey")
    labelCidr.grid(row=6, column=0)
    valueCidr = StringVar()
    valueCidr.set("")
    entryCidr = Entry(mainFrame, textvariable=valueCidr, width=30, fg="red", bd=5)
    entryCidr.grid(row=7, column=0)

    #ip version input
    labelIPv = Label(mainFrame, text="IP version", bg="grey")
    labelIPv.grid(row=9, column=0)
    ipList = ["4", "6"]
    valueIPv = StringVar()
    valueIPv.set(ipList[0])
    selector = OptionMenu(mainFrame, valueIPv, ipList[0], ipList[1])
    selector.grid(row=10, column=0)

    #Enable DHCP input
    labelDHCP = Label(mainFrame, text="Enable DHCP (True/False)", bg="grey")
    labelDHCP.grid(row=12, column=0)
    valueDHCP = StringVar()
    valueDHCP.set("False")
    entryDHCP = Entry(mainFrame, textvariable=valueDHCP, width=30, fg="red", bd=5)
    entryDHCP.grid(row=13, column=0)

    #Allocation Start input
    labelStart = Label(mainFrame, text="Allocation Pool Start (ex: 192.168.0.2, fc00::2)", bg="grey")
    labelStart.grid(row=15, column=0)
    valueStart = StringVar()
    valueStart.set("")
    entryStart = Entry(mainFrame, textvariable=valueStart, width=30, fg="red", bd=5)
    entryStart.grid(row=16, column=0)

    #Allocation End input
    labelEnd = Label(mainFrame, text="Allocation Pool End (ex: 192.168.0.5, fc00::ffff:ffff:ffff:ffff)", bg="grey")
    labelEnd.grid(row=18, column=0)
    valueEnd = StringVar()
    valueEnd.set("")
    entryEnd = Entry(mainFrame, textvariable=valueEnd, width=30, fg="red", bd=5)
    entryEnd.grid(row=19, column=0)

    #Gateway input
    labelGateway = Label(mainFrame, text="Gateway IP (ex: 192.168.0.1, fc00::1)", bg="grey")
    labelGateway.grid(row=1, column=6)
    valueGateway = StringVar()
    valueGateway.set("")
    entryGateway = Entry(mainFrame, textvariable=valueGateway, width=30, fg="red", bd=5)
    entryGateway.grid(row=2, column=6)

    #DNS input
    labelDNS = Label(mainFrame, text="DNS (ex: 8.8.8.8, 2001:4860:4860::8888)", bg="grey")
    labelDNS.grid(row=4, column=6)
    valueDNS = StringVar()
    valueDNS.set("")
    entryDNS = Entry(mainFrame, textvariable=valueDNS, width=30, fg="red", bd=5)
    entryDNS.grid(row=5, column=6)

    #ipv6 ra mode input
    labelIPv6ra = Label(mainFrame, text="IPv6 Router Advertisement Mode", bg="grey")
    labelIPv6ra.grid(row=7, column=6)
    ipv6raList = ["IPv4 Subnet", "slaac", "dhcpv6-stateful", "dhcpv6-stateless"]
    valueIPv6ra = StringVar()
    valueIPv6ra.set(ipv6raList[0])
    selector = OptionMenu(mainFrame, valueIPv6ra, ipv6raList[0], ipv6raList[1], ipv6raList[2], ipv6raList[3])
    selector.grid(row=8, column=6)

    #ipv6 address mode input
    labelIPv6add = Label(mainFrame, text="IPv6 Address Mode", bg="grey")
    labelIPv6add.grid(row=10, column=6)
    ipv6addList = ["IPv4 Subnet", "slaac", "dhcpv6-stateful", "dhcpv6-stateless"]
    valueIPv6add = StringVar()
    valueIPv6add.set(ipv6addList[0])
    selector = OptionMenu(mainFrame, valueIPv6add, ipv6addList[0], ipv6addList[1], ipv6addList[2], ipv6addList[3])
    selector.grid(row=11, column=6)

    #Project List
    labelProject = Label(mainFrame, text="Project", bg="grey")
    labelProject.grid(row=13, column=6)
    projectList = []
    cursor = osdata.dbconn.execute("SELECT NAME from PROJECTS")
    for row in cursor:
        projectList.append(row[0])
    valueProject = StringVar()
    valueProject.set(projectList[0])
    selector = OptionMenu(mainFrame, valueProject, projectList[0], *projectList[1:len(projectList)])
    selector.grid(row=14, column=6)
    
    #Add button
    addb = Button(mainFrame, text="Add Subnet", command= lambda : addSubnetFunction(valueNetName.get(), valueCidr.get(), valueIPv.get(), valueDHCP.get(), valueSubName.get()
    , valueStart.get(), valueEnd.get(), valueGateway.get(), valueDNS.get(), valueIPv6ra.get(), valueIPv6add.get(), valueProject.get()))
    addb.grid(row=25,column=13)

    #Return button
    returnb = Button(mainFrame, text="Return", command= lambda : displaySubnets(mainFrame))
    returnb.grid(row=25,column=0)


def addSubnetFunction(valueNetName, valueCidr, valueIPv, valueDHCP, valueSubName, valueStart, valueEnd, valueGateway, valueDNS, valueIPv6ra, valueIPv6add, valueProject):
    global conn
    netName = conn.get_network(valueNetName)
    cidr = valueCidr
    ipversion = valueIPv
    dhcp = valueDHCP
    subname = valueSubName
    start = valueStart
    end = valueEnd
    gateway = valueGateway
    dns = valueDNS
    project = osdata.dbconn.execute("SELECT ID from PROJECTS WHERE NAME=?", (valueProject,)).fetchone()[0]
    ipv6ra = valueIPv6ra
    ipv6add = valueIPv6add
    v6raOK = False
    v6addOK = False
    
    cursor = osdata.dbconn.execute("SELECT NAME from SUBNETS")
    for row in cursor:
        if subname == row[0]:
            showerror(title="ERROR", message="This Subnet Name already exists")
            return
            
    if subname == "":
        showerror(title="ERROR", message="Subnet Name can not be empty")
        return
    
    if cidr == "":
        showerror(title="ERROR", message="CIDR address can not be empty")
        return

    if gateway == "":
        showerror(title="ERROR", message="Gateway address can not be empty")
        return

    if dns == "":
        showerror(title="ERROR", message="DNS can not be empty")
        return

    if start == "" or end == "":
        showerror(title="ERROR", message="Allocation Pool can not be empty")
        return
    
    if ipv6ra != "IPv4 Subnet":
        v6raOK = True
    
    if ipv6add != "IPv4 Subnet":
        v6addOK = True

    if dhcp == "True":
        dhcp = True
    else:
        dhcp = False
    

    if ipversion == "4":
        conn.create_subnet(netName, cidr=cidr, ip_version="4", enable_dhcp=dhcp, subnet_name=subname, allocation_pools=[{"start":start, "end":end}], gateway_ip=gateway,
        dns_nameservers=[dns], project_id=project)
        osdata.setSubnetData(True)
        displaySubnets(mainFrame)
    elif ipversion == "6" and v6addOK and v6raOK:
        conn.create_subnet(netName, cidr=cidr, ip_version="6", enable_dhcp=dhcp, subnet_name=subname, allocation_pools=[{"start":start, "end":end}], gateway_ip=gateway,
        dns_nameservers=[dns], ipv6_ra_mode=ipv6ra, ipv6_address_mode=ipv6add, project_id=project)
        osdata.setSubnetData(True)
        displaySubnets(mainFrame)
    elif ipversion == "6" and v6addOK and not v6raOK:
        conn.create_subnet(netName, cidr=cidr, ip_version="6", enable_dhcp=dhcp, subnet_name=subname, allocation_pools=[{"start":start, "end":end}], gateway_ip=gateway,
        dns_nameservers=[dns], ipv6_address_mode=ipv6add, project_id=project)
        osdata.setSubnetData(True)
        displaySubnets(mainFrame)
    elif ipversion == "6" and not v6addOK and v6raOK:
        conn.create_subnet(netName, cidr=cidr, ip_version="6", enable_dhcp=dhcp, subnet_name=subname, allocation_pools=[{"start":start, "end":end}], gateway_ip=gateway,
        dns_nameservers=[dns], ipv6_ra_mode=ipv6ra, project_id=project)
        osdata.setSubnetData(True)
        displaySubnets(mainFrame)
    else :
        conn.create_subnet(netName, cidr=cidr, ip_version="6", enable_dhcp=dhcp, subnet_name=subname, allocation_pools=[{"start":start, "end":end}], gateway_ip=gateway,
        dns_nameservers=[dns], project_id=project)
        osdata.setSubnetData(True)
        displaySubnets(mainFrame)


def addRouter():
    global conn
    clearMainFrame(mainFrame)
    
    #Router Name input
    labelName = Label(mainFrame, text="Router Name", bg="grey")
    labelName.pack(pady=10)
    valueName = StringVar()
    valueName.set("")
    entryName = Entry(mainFrame, textvariable=valueName, width=30, fg="red", bd=5)
    entryName.pack()

    #Admin State input
    labelAdminState = Label(mainFrame, text="Admin State Up (True/False)", bg="grey")
    labelAdminState.pack(pady=10)
    valueAdminState = StringVar()
    valueAdminState.set("True")
    entryAdminState = Entry(mainFrame, textvariable=valueAdminState, width=30, fg="red", bd=5)
    entryAdminState.pack()

    #Network List
    labelNetwork = Label(mainFrame, text="External Network", bg="grey")
    labelNetwork.pack(pady=10)
    networkList = []
    cursor = osdata.dbconn.execute("SELECT NAME from NETWORKS")
    for row in cursor:
        networkList.append(row[0])
    valueNetName = StringVar()
    valueNetName.set(networkList[0])
    selector = OptionMenu(mainFrame, valueNetName, networkList[0], *networkList[1:len(networkList)])
    selector.pack()

    #Enable SNAT input
    labelSNAT = Label(mainFrame, text="Enable SNAT (True/False)", bg="grey")
    labelSNAT.pack(pady=10)
    valueSNAT = StringVar()
    valueSNAT.set("False")
    entrySNAT = Entry(mainFrame, textvariable=valueSNAT, width=30, fg="red", bd=5)
    entrySNAT.pack()

    #Project List
    labelProject = Label(mainFrame, text="Project", bg="grey")
    labelProject.pack(pady=10)
    projectList = []
    cursor = osdata.dbconn.execute("SELECT NAME from PROJECTS")
    for row in cursor:
        projectList.append(row[0])
    valueProject = StringVar()
    valueProject.set(projectList[0])
    selector = OptionMenu(mainFrame, valueProject, projectList[0], *projectList[1:len(projectList)])
    selector.pack()
    
    #Add button
    addb = Button(mainFrame, text="Add Router", command= lambda : addRouterFunction(valueName.get(), valueAdminState.get(), valueNetName.get(), valueSNAT.get(), valueProject.get()))
    addb.pack(padx=20,pady=20, side=RIGHT)

    #Return button
    returnb = Button(mainFrame, text="Return", command= lambda : displayRouters(mainFrame))
    returnb.pack(padx=20,pady=20, side=LEFT)


def addRouterFunction(valueName, valueAdminState, valueNetName, valueSNAT, valueProject):
    global conn
    name = valueName
    adminstate = valueAdminState
    network = osdata.dbconn.execute("SELECT ID FROM NETWORKS WHERE NAME=?", (valueNetName,)).fetchone()[0] 
    SNAT = valueSNAT
    project = osdata.dbconn.execute("SELECT ID from PROJECTS WHERE NAME=?", (valueProject,)).fetchone()[0]
    
    
    cursor = osdata.dbconn.execute("SELECT NAME from ROUTERS")
    for row in cursor:
        if name == row[0]:
            showerror(title="ERROR", message="This Router Name already exists")
            return
            
    if name == "":
        showerror(title="ERROR", message="Network Name can not be empty")
        return
        
    else:
        if SNAT == "True":
            SNAT = True
        else:
            SNAT = False
        if adminstate == "True":
            adminstate = True
        else:
            adminstate = False
        conn.create_router(name=name, admin_state_up=adminstate, ext_gateway_net_id=network, enable_snat=SNAT, project_id=project)
        osdata.setRouterData(True)
        displayRouters(mainFrame)


def addPort():
    global conn
    clearMainFrame(mainFrame)
    
    #Port Name input
    labelName = Label(mainFrame, text="Port Name", bg="grey")
    labelName.pack(pady=10)
    valueName = StringVar()
    valueName.set("")
    entryName = Entry(mainFrame, textvariable=valueName, width=30, fg="red", bd=5)
    entryName.pack()

    #Network List
    labelNetwork = Label(mainFrame, text="Network", bg="grey")
    labelNetwork.pack(pady=10)
    networkList = []
    cursor = osdata.dbconn.execute("SELECT NAME from NETWORKS")
    for row in cursor:
        networkList.append(row[0])
    valueNetName = StringVar()
    valueNetName.set(networkList[0])
    selector = OptionMenu(mainFrame, valueNetName, networkList[0], *networkList[1:len(networkList)])
    selector.pack()
    
    #Add button
    addb = Button(mainFrame, text="Add Port", command= lambda : addPortFunction(valueName.get(), valueNetName.get()))
    addb.pack(padx=20,pady=20, side=RIGHT)

    #Return button
    returnb = Button(mainFrame, text="Return", command= lambda : displayPorts(mainFrame))
    returnb.pack(padx=20,pady=20, side=LEFT)


def addPortFunction(valueName, valueNetName):
    global conn
    name = valueName
    network = osdata.dbconn.execute("SELECT ID FROM NETWORKS WHERE NAME=?", (valueNetName,)).fetchone()[0]
    
    if name == "":
        showerror(title="ERROR", message="Port Name can not be empty")
        return
    
    cursor = osdata.dbconn.execute("SELECT NAME from PORTS")
    for row in cursor:
        if name == row[0]:
            showerror(title="ERROR", message="This Port Name already exists")
            return
            
    conn.create_port(name=name, network_id=network)
    osdata.setPortData(True)
    displayPorts(mainFrame)


def addSecGroup():
    global conn
    clearMainFrame(mainFrame)
    
    #SecGroup Name input
    labelName = Label(mainFrame, text="Security Group Name", bg="grey")
    labelName.pack(pady=10)
    valueName = StringVar()
    valueName.set("")
    entryName = Entry(mainFrame, textvariable=valueName, width=30, fg="red", bd=5)
    entryName.pack()

    #Description input
    labelDes = Label(mainFrame, text="Description", bg="grey")
    labelDes.pack(pady=10)
    valueDes = StringVar()
    valueDes.set("")
    entryDes = Entry(mainFrame, textvariable=valueDes, width=30, fg="red", bd=5)
    entryDes.pack()

    #Project List
    labelProject = Label(mainFrame, text="Project", bg="grey")
    labelProject.pack(pady=10)
    projectList = []
    cursor = osdata.dbconn.execute("SELECT NAME from PROJECTS")
    for row in cursor:
        projectList.append(row[0])
    valueProject = StringVar()
    valueProject.set(projectList[0])
    selector = OptionMenu(mainFrame, valueProject, projectList[0], *projectList[1:len(projectList)])
    selector.pack()
    
    #Add button
    addb = Button(mainFrame, text="Add Security Group", command= lambda : addSecGroupFunction(valueName.get(), valueDes.get(), valueProject.get()))
    addb.pack(padx=20,pady=20, side=RIGHT)

    #Return button
    returnb = Button(mainFrame, text="Return", command= lambda : displaySecurityGroups(mainFrame))
    returnb.pack(padx=20,pady=20, side=LEFT)


def addSecGroupFunction(valueName, valueDes, valueProject):
    global conn
    name = valueName
    project = osdata.dbconn.execute("SELECT ID from PROJECTS WHERE NAME=?", (valueProject,)).fetchone()[0]
    
    cursor = osdata.dbconn.execute("SELECT NAME from SECURITY_GROUPS")
    for row in cursor:
        if name == row[0]:
            showerror(title="ERROR", message="This Security Group Name already exists")
            return
            
    if name == "":
        showerror(title="ERROR", message="Security Group Name can not be empty")
        return
        
    else:
        conn.create_security_group(name, description=valueDes, project_id=project)
        osdata.setSecGroupData(True)
        displaySecurityGroups(mainFrame)


def createRule(secGroupID):
    global conn
    clearMainFrame(mainFrame)
    
    #Port Min input
    labelPortMin = Label(mainFrame, text="Port Range Min (Optional)", bg="grey")
    labelPortMin.pack(pady=10)
    valuePortMin = IntVar()
    valuePortMin.set(-1)
    entryPortMin = Entry(mainFrame, textvariable=valuePortMin, width=30, fg="red", bd=5)
    entryPortMin.pack()

    #Port Max input
    labelPortMax = Label(mainFrame, text="Port Range Max (Optional)", bg="grey")
    labelPortMax.pack(pady=10)
    valuePortMax = IntVar()
    valuePortMax.set(-1)
    entryPortMax = Entry(mainFrame, textvariable=valuePortMax, width=30, fg="red", bd=5)
    entryPortMax.pack()

    #Protocol input
    labelProtocol = Label(mainFrame, text="Protocol", bg="grey")
    labelProtocol.pack(pady=10)
    protocolList = ["None", "tcp", "udp", "icmp", "ipv6-icmp"]
    valueProtocol = StringVar()
    valueProtocol.set(protocolList[0])
    selector = OptionMenu(mainFrame, valueProtocol, protocolList[0], protocolList[1], protocolList[2], protocolList[3], protocolList[4])
    selector.pack()

    #Direction input
    labelDirection = Label(mainFrame, text="Direction", bg="grey")
    labelDirection.pack(pady=10)
    directionList = ["ingress", "egress"]
    valueDirection = StringVar()
    valueDirection.set(directionList[0])
    selector = OptionMenu(mainFrame, valueDirection, directionList[0], directionList[1])
    selector.pack()

    #Ethertype input
    labelEther = Label(mainFrame, text="Ethertype", bg="grey")
    labelEther.pack(pady=10)
    etherList = ["IPv4", "IPv6"]
    valueEther = StringVar()
    valueEther.set(etherList[0])
    selector = OptionMenu(mainFrame, valueEther, etherList[0], etherList[1])
    selector.pack()

    #Project List
    labelProject = Label(mainFrame, text="Project", bg="grey")
    labelProject.pack(pady=10)
    projectList = []
    cursor = osdata.dbconn.execute("SELECT NAME from PROJECTS")
    for row in cursor:
        projectList.append(row[0])
    valueProject = StringVar()
    valueProject.set(projectList[0])
    selector = OptionMenu(mainFrame, valueProject, projectList[0], *projectList[1:len(projectList)])
    selector.pack()
    
    #Add button
    addb = Button(mainFrame, text="Create Security Group Rule", command= lambda : createRuleFunction(secGroupID, valuePortMin.get(), valuePortMax.get(), valueProtocol.get(),
    valueDirection.get(), valueEther.get(), valueProject.get()))
    addb.pack(padx=20,pady=20, side=RIGHT)

    #Return button
    returnb = Button(mainFrame, text="Return", command= lambda : displaySecurityGroups(mainFrame))
    returnb.pack(padx=20,pady=20, side=LEFT)


def createRuleFunction(secGroupID, valuePortMin, valuePortMax, valueProtocol, valueDirection, valueEther, valueProject):
    global conn
    project = osdata.dbconn.execute("SELECT ID from PROJECTS WHERE NAME=?", (valueProject,)).fetchone()[0]
    
    if valuePortMin==-1 or valuePortMax==-1:
        conn.create_security_group_rule(secGroupID, protocol=valueProtocol, direction=valueDirection, ethertype=valueEther, project_id=project)
        osdata.setSecGroupData(True)
        displaySecurityGroups(mainFrame)
    else :
        conn.create_security_group_rule(secGroupID, port_range_min=valuePortMin, port_range_max=valuePortMax, protocol=valueProtocol, direction=valueDirection, 
        ethertype=valueEther, project_id=project)
        osdata.setSecGroupData(True)
        displaySecurityGroups(mainFrame)



#Delete item

def deleteProject(project_id):
    global conn
    if askyesno('WARNING', 'Delete Project ?'):
        osdata.dbconn.execute("DELETE from PROJECTS where ID=?", (project_id,))
        osdata.dbconn.commit()
        conn.delete_project(project_id)
        osdata.setProjectData(True)
        displayProjects(mainFrame)
    
def deleteUser(user_id):
    global conn
    if askyesno('WARNING', 'Delete selected user ?'):
        osdata.dbconn.execute("DELETE from USERS where ID=?", (user_id,))
        osdata.dbconn.commit()
        conn.delete_user(user_id)
        osdata.setUserData(True)
        displayUsers(mainFrame)

def deleteNetwork(network_id):
    global conn
    if askyesno('WARNING', 'Delete selected network ?'):
        osdata.dbconn.execute("DELETE from NETWORKS where ID=?", (network_id,))
        osdata.dbconn.commit()
        conn.delete_network(network_id)
        osdata.setNetworkData(True)
        displayNetworks(mainFrame)

def deleteFloatingIP(fip_id):
    global conn
    if askyesno('WARNING', 'Delete selected floating ip ?'):
        osdata.dbconn.execute("DELETE from FLOATING_IPS where ID=?", (fip_id,))
        osdata.dbconn.commit()
        conn.delete_floating_ip(fip_id)
        osdata.setFloatingIPData(True)
        displayFloatingIPs(mainFrame)

def deleteSubnet(subnet_id):
    global conn
    if askyesno('WARNING', 'Delete selected subnet ?'):
        osdata.dbconn.execute("DELETE from SUBNETS where ID=?", (subnet_id,))
        osdata.dbconn.commit()
        conn.delete_subnet(subnet_id)
        osdata.setSubnetData(True)
        displaySubnets(mainFrame)

def deleteRouter(router_id):
    global conn
    if askyesno('WARNING', 'Delete selected router ?'):
        osdata.dbconn.execute("DELETE from ROUTERS where ID=?", (router_id,))
        osdata.dbconn.commit()
        conn.delete_router(router_id)
        osdata.setRouterData(True)
        displayRouters(mainFrame)

def deletePort(port_id):
    global conn
    if askyesno('WARNING', 'Delete selected port ?'):
        osdata.dbconn.execute("DELETE from PORTS where ID=?", (port_id,))
        osdata.dbconn.commit()
        conn.delete_port(port_id)
        osdata.setPortData(True)
        displayPorts(mainFrame)

def deleteImage(image_id):
    global conn
    if askyesno('WARNING', 'Delete selected image ?'):
        osdata.dbconn.execute("DELETE from IMAGES where ID=?", (image_id,))
        osdata.dbconn.commit()
        conn.delete_image(image_id)
        osdata.setImageData(True)
        displayImages(mainFrame)

def deleteServer(server_id):
    global conn
    if askyesno('WARNING', 'Delete selected server ?'):
        osdata.dbconn.execute("DELETE from SERVERS where ID=?", (server_id,))
        osdata.dbconn.commit()
        conn.delete_server(server_id)
        osdata.setServerData(True)
        displayServers(mainFrame)

def deleteSecGroup(secgroup_id):
    global conn
    if askyesno('WARNING', 'Delete selected security group ?'):
        osdata.dbconn.execute("DELETE from SECURITY_GROUPS where ID=?", (secgroup_id,))
        osdata.dbconn.commit()
        conn.delete_security_group(secgroup_id)
        osdata.setSecGroupData(True)
        displaySecurityGroups(mainFrame)

def deleteRule(ruleID):
    global conn
    if askyesno('WARNING', 'Delete selected security group rule ?'):
        osdata.dbconn.execute("DELETE from SECURITY_GROUP_RULES where ID=?", (ruleID,))
        osdata.dbconn.commit()
        conn.delete_security_group_rule(ruleID)
        osdata.setSecGroupData(True)
        displaySecurityGroups(mainFrame)




#Tkinter Loop
def on_closing():
    if askokcancel("Quit", "Do you want to quit?"):
        stopThread()
        window.quit()

window.protocol("WM_DELETE_WINDOW", on_closing)
window.mainloop()



