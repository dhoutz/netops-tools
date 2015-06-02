#!/usr/bin/python

'''
This script utilizes the junos-pyez netconf library to connect to a given list
of Junos devices and check the status of installed license. The script returns
a list of devices needing a license install.

Author: Dan Houtz
Email: dhoutz@gmail.com

'''

from multiprocessing import Pool
from jnpr.junos import Device
from jnpr.junos.factory import loadyaml
import logging

#Disable logging handler warnings
logging.root.manager.emittedNoHandlerWarning = True

#Load license TABLE/VIEW data from yaml file
globals().update( loadyaml('license'))

# Default variables
failed_check = []

#Set number of worker threads
maxThreads=10

#Array of devices to check
device_list = []

#SSH username/password to connect to devices
user = ''
password = ''

#Array of devices to ignore during processing
filtered_device_list = []

def startThreads(devices):
    pool = Pool(processes=maxThreads)
    results = pool.map(process_device, devices)
    return results

def process_device(device):
  #print "Processing", device
  try:
    needs_license = "no"
    dev = Device(device, user=user, password=password)
    dev.open()
    license_data = LicenseTable(dev)
    license_data.get()
    dev.close()
    for license in license_data:
      if int(license.needed) > 0:
        needs_license = "yes"
    return (device, needs_license)
  except:
    #print "Check failed for ", device
    failed_check.append(device)
    return (device, "failed")

##########
# MAIN 
##########

if __name__ == "__main__":
  counter = 0
  for device in device_list:
    for filtered_device in filtered_device_list:
      if device == filtered_device:
        #print "Ignoring", device
        device_list.pop(counter)
    counter = counter + 1

  results = startThreads(device_list)

  #Output results
  print ""
  print "The following devices require license:"
  for result in results:
    if result[1] == "yes":
      print result[0]

  print ""
  print "License check failed for the following devices:"
  for result in results:
    if result[1] == "failed":
      print result[0]

  print ""
  print "The following devices were filtered:"
  for filtered_device in filtered_device_list:
    print filtered_device
