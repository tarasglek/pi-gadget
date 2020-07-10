#!/bin/bash

# Konfiguration fuer ein Composite Gadget Device
# mit mehreren HID und Flash Komponenten
set -x
#Kernelmodul aktivieren
modprobe libcomposite

#board config anlegen
mkdir /sys/kernel/config/usb_gadget/multiDeskBoard
cd /sys/kernel/config/usb_gadget/multiDeskBoard

#hardware id setzen
echo 0x0419 > bcdDevice
echo 0x0200 > bcdUSB
echo 0x1d6b > idVendor
echo 0x0104 > idProduct

#Geraetetyp setzen
echo 0xEF > bDeviceClass
echo 0x02 > bDeviceSubClass
echo 0x01 > bDeviceProtocol
echo 0x08 > bMaxPacketSize0

#klartextbeschreibung setzen
mkdir strings/0x409
mkdir strings/0x407
cd strings/0x409
echo "RSI_HUD_Solutions" > manufacturer
echo "MultiDeskBoard" > product
echo "1337" > serialnumber
cd ../../
cd strings/0x407
echo "RSI_HUD_Solutions" > manufacturer
echo "MultiDeskBoard" > product
echo "1337" > serialnumber
cd ../../

#geraetefunktion setzen
mkdir functions/mass_storage.usb0
mkdir functions/hid.usb0
mkdir functions/ecm.usb0

# networking
# first byte of address must be even
HOST="48:6f:73:74:50:43" # "HostPC"
SELF="42:61:64:55:53:42" # "BadUSB"
echo $HOST > functions/ecm.usb0/host_addr
echo $SELF > functions/ecm.usb0/dev_addr


#HID0 Funktion Konfiguration auf keyboard setzen
cd functions/hid.usb0
echo 1 > protocol
echo 8 > report_length
echo 1 > subclass
#cp /home/pi/USBConfigBuffer/mediaKeyboardRepDesc report_desc
cd ../../

#Mass Storage 0 Konfiguration setzen
cd functions/mass_storage.usb0
echo 0 > stall
echo 1 > lun.0/removable
echo 0 > lun.0/ro
echo /home/pi/proxmox-ve_6.2-1.iso > lun.0/file
cd ../../

#OS Descriptor fuer Windoof setzen
cd os_desc
echo 1 > use
echo 0xcd > b_vendor_code
echo MSFT100 > qw_sign
cd ../

#Bus Hardware Konfig anlegen und verlinken
mkdir configs/c.1
cd configs/c.1
echo 0x80 > bmAttributes
echo 100 > MaxPower
mkdir strings/0x409
echo "MDB Config1" > strings/0x409/configuration
mkdir strings/0x407
echo "MDB Config1" > strings/0x407/configuration
cd ../../
ln -s functions/mass_storage.usb0 configs/c.1
ln -s functions/hid.usb0 configs/c.1
ln -s functions/ecm.usb0 configs/c.1
ln -s configs/c.1 os_desc

#Geraet aktivieren
ls /sys/class/udc > UDC
