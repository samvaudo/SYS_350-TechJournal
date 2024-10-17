import json
import getpass
from pyVim.connect import SmartConnect, vim
import ssl
from time import sleep
import os


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
    os.system("clear")
    print("Options:")
    print("1: Power On VM")
    print("2: Power Off VM")
    print("3: Take a snapshot (ONLY DO IF powered off)")
    print("4: Restore a VM to a snapshot")
    print("5: Tweak VM Config (CPU or RAM)")
    print("6: Clone VM")
    print("7: Delete VM")
    print("8: Exit")
choice = 0
while True:
    printmenu()

    choice  = input("Enter an Option: ")

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
                            print(i.name, " is now powered on!")
                            sleep(3)
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
                            print(i.name, " is now powered on!")
                            sleep(3)            
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
                            sleep(3)
            else:
                print("Canceling!")
        else:
            for i in vms:
                    if poweroffname in str(i.name):
                        if i.guest.guestState == "notRunning":
                            print(i.name, " is already powered off, skipping")
                        else:
                            print(i.name, " is not powered off, powering off!")
                            i.PowerOff()
                            sleep(2)
                            print(i.name, " is now powered off!")
                            sleep(3) 
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
                        sleep(3)
            else:
                print("Canceling!")
        else:
            for i in vms:
                    if snapshotname in str(i.name):
                        snaptitle = input("What is the title of the snapshot?: ")
                        snapDescript = input("What is the snapshot description?: ")
                        print("Taking a snapshot of ", i.name)
                        i.CreateSnapshot(snaptitle , snapDescript,True,True)
                        sleep(2)
                        print(i.name, " has a snapshot saved!")
                        sleep(3)
    elif choice == "4":
        si.RetrieveContent()
        datacenter = si.content.rootFolder.childEntity[0]
        vms = datacenter.vmFolder.childEntity
        print("Vms Managed by Vcenter: ")
        for v in vms:
            print(v.name)
        restorename = input("What is the name of the VM to be restored?: ")
        for i in vms:
                    if restorename in str(i.name):
                        print(i.name, " is being restored to the most current snapshot!")
                        i.RevertToCurrentSnapshot()
                        sleep(2)
                        print(i.name, " is now restored!") 
                        sleep(3)
    elif choice == "5":
        si.RetrieveContent()
        datacenter = si.content.rootFolder.childEntity[0]
        vms = datacenter.vmFolder.childEntity
        print("Vms Managed by Vcenter: ")
        for v in vms:
            print(v.name)
        configname = input("What is the name of the VM to be configured?: ")
        for i in vms:
                    if configname in str(i.name):
                        print(i.name, " is being configured!")
                        newspec = vim.vm.ConfigSpec()
                        newspec.numCPUs = int(input("Enter the number of CPU cores to allocate (2-8): "))
                        dual = input("Cores are dual threaded? (Y/N): ")
                        if dual == "Y":
                            newspec.numCoresPerSocket = 2
                        else:
                            newspec.numCoresPerSocket = 1
                        newspec.memoryMB = int(input("How many GB of memory to allocate? (2-8): "))*1024
                        print("Configuring.....")
                        i.Reconfigure(newspec)
                        sleep(2)
                        print(i.name, " is now configured!") 
                        sleep(3)
    elif choice == "6":
        si.RetrieveContent()
        datacenter = si.content.rootFolder.childEntity[0]
        vms = datacenter.vmFolder.childEntity
        print("Vms Managed by Vcenter: ")
        for v in vms:
            print(v.name)
        restorename = input("What is the name of the VM to be cloned?: ")
        for i in vms:
                    if restorename in str(i.name):
                        print(i.name, " is being cloned!")
                        newname = input("What is the name of the clone?: ")
                        newspec = vim.vm.CloneSpec()
                        newrelocate = vim.vm.RelocateSpec()

                        newrelocate.datastore = datacenter.datastore[0]
                        newspec.location = newrelocate
                        print("Cloning......")
                        i.Clone(folder=datacenter.vmFolder,name=newname, spec=newspec)
                        sleep(2)
                        print(i.name, " is now cloned! It may take a while...") 
                        sleep(3)
    elif choice == "7":
        si.RetrieveContent()
        datacenter = si.content.rootFolder.childEntity[0]
        vms = datacenter.vmFolder.childEntity
        print("Vms Managed by Vcenter: ")
        for v in vms:
            print(v.name)
        restorename = input("What is the name of the VM to be cloned?: ")
        for i in vms:
                    if restorename in str(i.name):
                        checking = input("Are you sure you want do delete "+i.name+"? This can't be undone!! (Y/N): ")
                        if checking == "Y":
                            print(i.name, " is being deleted!")
                            i.Destroy()
                            print("Done!")
                            
                        else:
                             print("Canceling!")
                             break

    elif choice == "8":
        print("Exiting....")
        exit()