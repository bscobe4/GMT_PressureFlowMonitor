#!/usr/bin/python
# -*- coding:utf-8 -*-

import os
import time
import keyboard
import csv  # to write to csv file for nfs
import ADS1256
import RPi.GPIO as GPIO
from datetime import datetime
import sys
import select
import tty
import termios

workpath = '/home/pi/Documents/GMT_PressFlowMonitor/python3/'
slowFile = 'output/slowPFMdata.csv'
fastFile = 'output/fastPFMdata'

KEY_ESC = '\x1b'

row = 0  # To indicate if header needs to be written
numRows = 10
isLogging = True
fastLogging = True

escape = False
#**Function definitions**
def isData(): #keypress
        return select.select([sys.stdin], [], [], 0) == ([sys.stdin], [], [])

os.chdir(os.path.dirname(workpath))

old_settings = termios.tcgetattr(sys.stdin) #keypress

try:
    tty.setcbreak(sys.stdin.fileno()) #keypress
    
    ADC = ADS1256.ADS1256()
    ADC.ADS1256_init()

    #Add timestamp in filename
    timeStart = time.time()
    dNow = datetime.now()
    strDate = dNow.strftime("%m-%d-%Y_%H:%M:%S")
    fastFile = fastFile + strDate + '.csv'
    
    

    with open(fastFile, 'w', newline='') as csvfile:
        dataWriter = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        if row == 0:
            dataWriter.writerow(
                ['Rod 1 (V)'] + ['Back 1 (V)'] + ['Rod 2 (V)'] + ['Back 2 (V)'] + ['Rod 3 (V)'] + ['Back 3 (V)'] + ['Flow 1 (V)'] + [
                    'Flow 2'] + ['Time (s)'])  # write header
            row += 1  # toggle to show that header has been written
        #while (row <= numRows): #DEBUG replace with GPIO trigger
        while isLogging:
            ADC_Value = ADC.ADS1256_GetAll()
            timeDelta = time.time() - timeStart
            
            dataWriter.writerow(
                ['%lf' % (ADC_Value[0] * 5.0 / 0x7fffff)] + ['%lf' % (ADC_Value[1] * 5.0 / 0x7fffff)] + [
                    '%lf' % (ADC_Value[2] * 5.0 / 0x7fffff)] + ['%lf' % (ADC_Value[3] * 5.0 / 0x7fffff)] + [
                    '%lf' % (ADC_Value[4] * 5.0 / 0x7fffff)] + ['%lf' % (ADC_Value[5] * 5.0 / 0x7fffff)] + [
                    '%lf' % (ADC_Value[6] * 5.0 / 0x7fffff)] + ['%lf' % (ADC_Value[7] * 5.0 / 0x7fffff)] + ['%lf' % timeDelta])
            #print ("0 ADC = %lf"%(ADC_Value[0]*5.0/0x7fffff))
            row += 1
            csvfile.flush() #debug try to remove
            
            #keypress- listen for input
            if isData():
              c = sys.stdin.read(1)
              if c == KEY_ESC: #esc key
                escape = True
                print("esc fastLog") #debug
            
            if escape:
              isLogging = False
            
            if not fastLogging:
              time.sleep(1)  #1 Hz
            else:
              time.sleep(0.001)  #1kHz *DEBUG: this implementation only leads to about 20 Hz real-time


except:
    GPIO.cleanup()
    termios.tcsetattr(sys.stdin, termios.TCSADRAIN, old_settings)
    print("\r\nfastLogging end (exception)    ")
    exit()

finally:
        termios.tcsetattr(sys.stdin, termios.TCSADRAIN, old_settings)
        print("fastLogging end (exited)")
