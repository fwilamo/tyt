#!/usr/bin/env


##########    Tune Your Twizy    ###########
# This tool can be used to configure some controller parameter of your Renault Twizy.
# This graphical tool communicates with an OVMS, which has to be connected to the Twizy before. 
#
# Copyright (C) 2015  Falk Wilamowski
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


from gi.repository import Gtk
import serial
import sys
import platform
import os


class Handler:
    def onDeleteWindow(self, *args):
        Gtk.main_quit(*args)

    #    def onButtonPressed(self, button):
    #    print("Hello World!")



def get_available_serial_interfaces():


    if  platform.system() == "Linux":
         
        try:
            all_serial_devices = os.listdir("/dev/serial/by-id")
            return all_serial_devices

        except OSError:
            print "Keine seriellen Ports gefunden"
            return None
    
    # TODO muss noch unter Windows ausprobiert und erweitert werden !
    elif platform.system() == "Windows":
        print "bin unter windows. wie bekommt man alle COM ports ?"
    
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
            

    # TODO muss noch unter Windows ausprobiert und erweitert werden !
    elif platform.system() == "Windows":
        try :    
            serial_interface_handler = serial.Serial()       # open the first COM port available
        except serial.SerialException, e:
            print("Could not open serial port: %s" % ( e))
            print "In case your user has not the necessary permissions, try:sudo usermod -a -G dialout $USER and sudo apt-get remove modemmanager"
        

    else:
        print "Betriebssystem momentan nicht unterstuetzt"


    return serial_interface_handler




# load the GUI from a glade file
builder = Gtk.Builder()
builder.add_from_file("tyt.glade")
       
# connect signals
builder.connect_signals(Handler())

# get main window object and resize it
window = builder.get_object("MainWindow")
window.set_default_size(550,400)


# prepare the statusbar
tyt_statusbar = builder.get_object("tyt_statusbar") 
context_id_1 = tyt_statusbar.get_context_id("interface")


# prepare the interface combobox and show all available serial interfaces
interfaces_combo_box = builder.get_object("combobox_interface")
available_serial_interfaces = get_available_serial_interfaces()

if available_serial_interfaces:
    tyt_statusbar.push(context_id_1, "Bitte eine Schnittstelle auswaehlen und auf Verbinden klicken.")

    for interface in available_serial_interfaces:
        interfaces_combo_box.append_text(interface)
else:
    tyt_statusbar.push(context_id_1, "Es wurden keine seriellen Schnittstellen gefunden.")

# everything is prepared - show window and start listening
window.show_all()

Gtk.main()

'''

    if ser:
        print("Opened serial port: %s with properties: %s" % (ser.name, ser.getSettingsDict()))
    else:
        print "Opening serial port was not successful."
'''