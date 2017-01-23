#!/usr/bin/env
 # -*- coding: UTF8 -*-

##########    Tune Your Twizy    ###########
# This tool can be used to configure some controller parameter of your Renault Twizy.
# This graphical tool communicates with an OVMS, which has to be connected to the Twizy before. 
#
# Copyright (C) 2015  Falk Wilamowski (falk@wilamowski.de)
# code for windows serial port detection from Eli Bendersky (eliben@gmail.com)
#
#############################################




# This program is free software; you can redistribute it and/or modify it under the terms of the 
# GNU General Public License as published by the Free Software Foundation; either version 2 of the License,
# or (at your option) any later version. 
#
# This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; 
# without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. 
# See the GNU General Public License for more details. 
#
# You should have received a copy of the GNU General Public License along with this program; if not, write
# to the Free Software Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA 02110, USA
#
#
# Dieses Programm ist freie Software. Sie können es unter den Bedingungen der GNU General Public License,
# wie von der Free Software Foundation veröffentlicht, weitergeben und/oder modifizieren, entweder gemäß Version 2
# der Lizenz oder (nach Ihrer Option) jeder späteren Version. 
#
# Die Veröffentlichung dieses Programms erfolgt in der Hoffnung, daß es Ihnen von Nutzen sein wird, 
# aber OHNE IRGENDEINE GARANTIE, sogar ohne die implizite Garantie der MARKTREIFE oder der VERWENDBARKEIT
# FÜR EINEN BESTIMMTEN ZWECK. Details finden Sie in der GNU General Public License. 
#
# Sie sollten ein Exemplar der GNU General Public License zusammen mit diesem Programm erhalten haben.
# Falls nicht, schreiben Sie an die Free Software Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA 02110, USA.


import serial
import sys
import platform
import os

import re, itertools
import _winreg as winreg
   
def get_full_port_name_windows(portname):
    """ Given a port-name (of the form COM7, 
        COM12, CNCA0, etc.) returns a full 
        name suitable for opening with the 
        Serial class.
    """
    m = re.match('^COM(\d+)$', portname)
    if m and int(m.group(1)) < 10:
        return portname    
    return '\\\\.\\' + portname    
    

def detected_serial_ports_in_windows():
    """ Uses the Win32 registry to return an 
        iterator of serial (COM) ports 
        existing on this computer.
    """
    path = 'HARDWARE\\DEVICEMAP\\SERIALCOMM'
    try:
        key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, path)
    except WindowsError:
        raise IterationError

    for i in itertools.count():
        try:
            val = winreg.EnumValue(key, i)
            yield str(val[1])
        except EnvironmentError:
            break


def get_available_serial_interfaces():
    all_serial_devices = []

    if  platform.system() == "Linux":
         
        try:
            all_serial_devices = os.listdir("/dev/serial/by-id")
            return all_serial_devices

        except OSError:
            print "Keine seriellen Ports gefunden"
            return None
    
    
    elif platform.system() == "Windows":
        for p in detected_serial_ports_in_windows():
            all_serial_devices.append(get_full_port_name_windows(p))

        return all_serial_devices
    
    
    elif platform.system() == "Darwin":
        print "Mac OS erkannt"
        all_serial_devices = os.listdir("/dev")

        selectable_serial_interfaces = []
        for device in all_serial_devices:
            #print device
            if device.startswith("tty."):

                selectable_serial_interfaces.append(device) 

        return selectable_serial_interfaces

    else:
        print "Betriebssystem momentan nicht unterstuetzt"





def open_selected_serial_interface(selected_interface):

    serial_interface_handler = None

    if  platform.system() == "Linux":
         
        try :    
            serial_interface_handler = serial.Serial(port = "/dev/serial/by-id/%s" % selected_interface)
        except serial.SerialException, e:
            print("Could not open serial port: %s" % ( e))
            print "In case your user has not the necessary permissions, try:sudo usermod -a -G dialout $USER and sudo apt-get remove modemmanager"
            

    elif platform.system() == "Windows":
        try :    
            serial_interface_handler = serial.Serial()       # open the first COM port available
        except serial.SerialException, e:
            print("Could not open serial port: %s" % ( e))
            

    elif platform.system() == "Darwin":
        try:
            print "öffne port", selected_interface
            serial_interface_handler = serial.Serial(port = "/dev/%s" % selected_interface)
        except serial.SerialException, e:
            print("Could not open serial port: %s" % ( e))
            
    else:
        print "Betriebssystem momentan nicht unterstützt"


    return serial_interface_handler


# just test code to test the both serial port functions

available_serial_interfaces = get_available_serial_interfaces()
print available_serial_interfaces

if available_serial_interfaces and  len(available_serial_interfaces)>0:
    # example: open second found interface 
    opened_serial_interface = open_selected_serial_interface(available_serial_interfaces[0])
    print opened_serial_interface
else:
    print "keine serielle Schnittstelle gefunden."

