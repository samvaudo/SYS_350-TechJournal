import json
import getpass
from pyVim.connect import SmartConnect, vim
import ssl
from time import sleep


def pyVimConnect(jsonfile):
    with open(jsonfile) as f:
        config = json.load(f)['vcenter'][0]

    passw = getpass.getpass()
    s=ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
    s.verify_mode=ssl.CERT_NONE


    si=SmartConnect(host=config['vcenterhost'], user=config['vcenteradmin'], pwd=passw, sslContext=s)
    return si

def searchvms(siobject, name = "ALL"):
    allobj= {}
    objectstoreturn = []
    container = siobject.content.viewManager.CreateContainerView(siobject.content.rootFolder, [vim.VirtualMachine],True)
    for objects in container.view:
        allobj.update({objects.name: objects})
        objectstoreturn.append(objects)
    if name == "ALL":
        return objectstoreturn
    else:
        if name in allobj:
            return allobj[name]
        else:
            print("name not found")
            return None

si = pyVimConnect("Milestone 5/vcenter-conf.json")

def printmenu():
    print("Options:")
    print("1: Power On VM")
    print("2: Power Off VM")
    print("3: Take a snapshot (ONLY DO IF powered off)")
    print("4: Create a clone VM (ONLY DO IF powered off)")
    print("5: Tweak VM Config (CPU or RAM)")
    print("6: Delete VM")
    print("7: Exit")
choice = 0
while True:
    printmenu()

    choice  = input("Enter an Option")

    if choice == "1":
        si.RetrieveContent()
        datacenter = si.content.rootFolder.childEntity[0]
        vms = datacenter.vmFolder.childEntity
        print("Vms Managed by Vcenter: ")
        for v in vms:
            print(v.name)
        poweronname = input("What is the name of the VM to be powered on?")

        si.RetrieveContent()
        if len(poweronname) == 0:
            checking = input("Are you sure that you want to power on all VMs? (Y/N): ")
            if checking == "Y":
                for i in vms:
                    if poweronname in str(i.name):
                        if i.guest.guestState == "running":
                            print(i.name, " is already powered on, skipping")
                        else:
                            print(i.name, " is not powered on, powering on!")
                            i.PowerOn()
                            sleep(2)
                            print(i.name, " is npw powered on!")
            else:
                print("Canceling!")
        else:
            for i in vms:
                    if poweronname in str(i.name):
                        if i.guest.guestState == "running":
                            print(i.name, " is already powered on, skipping")
                        else:
                            print(i.name, " is not powered on, powering on!")
                            i.PowerOn()
                            sleep(2)
                            print(i.name, " is npw powered on!")             
    elif choice == "2":
        si.RetrieveContent()
        datacenter = si.content.rootFolder.childEntity[0]
        vms = datacenter.vmFolder.childEntity
        print("Vms Managed by Vcenter: ")
        for v in vms:
            print(v.name)
        poweroffname = input("What is the name of the VM to be powered off?")

        si.RetrieveContent()
        if len(poweroffname) == 0:
            checking = input("Are you sure that you want to power off all VMs? (Y/N): ")
            if checking == "Y":
                for i in vms:
                    if poweroffname in str(i.name):
                        if i.guest.guestState == "notRunning":
                            print(i.name, " is already powered off, skipping")
                        else:
                            print(i.name, " is not powered off, powering off!")
                            i.PowerOff()
                            sleep(2)
                            print(i.name, " is now powered off!")
            else:
                print("Canceling!")
        else:
            for i in vms:
                    if poweroffname in str(i.name):
                        if i.guest.guestState == "notRunning":
                            print(i.name, " is already powered off, skipping")
                        else:
                            print(i.name, " is not powered off, powering on!")
                            i.PowerOff()
                            sleep(2)
                            print(i.name, " is now powered off!") 
    elif choice == "3":
        si.RetrieveContent()
        datacenter = si.content.rootFolder.childEntity[0]
        vms = datacenter.vmFolder.childEntity
        print("Vms Managed by Vcenter: ")
        for v in vms:
            print(v.name)
        snapshotname = input("What is the name of the VM that a snapshot is to be taken?")

        si.RetrieveContent()
        if len(snapshotname) == 0:
            checking = input("Are you sure that you want to take a snapshot on all VMS? (Y/N): ")
            if checking == "Y":
                for i in vms:
                    if snapshotname in str(i.name):
                        snaptitle = input("What is the title of the snapshot?: ")
                        snapDescript = input("What is the snapshot description?: ")
                        print("Taking a snapshot of ", i.name)
                        i.CreateSnapshot(snaptitle, snapDescript)
                        sleep(2)
                        print(i.name, " has a snapshot saved!")
            else:
                print("Canceling!")
        else:
            for i in vms:
                    if snapshotname in str(i.name):
                        snaptitle = input("What is the title of the snapshot?: ")
                        snapDescript = input("What is the snapshot description?: ")
                        print("Taking a snapshot of ", i.name)
                        i.CreateSnapshot(snaptitle, snapDescript)
                        sleep(2)
                        print(i.name, " has a snapshot saved!")
    elif choice == "4":
        continue
    elif choice == "5":
        continue
    elif choice == "6":
        continue
    elif choice == "7":
        print("Exiting....")
        exit()