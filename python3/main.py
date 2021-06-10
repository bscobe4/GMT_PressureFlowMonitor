#!/usr/bin/python
# -*- coding:utf-8 -*-

import os
import time
import csv  # to write to csv file for nfs
import ADS1256
import RPi.GPIO as GPIO
import keyboard
from datetime import datetime
import sys
import select
import tty
import termios
import configparser

workpath = '/home/pi/Documents/GMT_PressFlowMonitor/python3/'
slowFile = 'output/slowPFMdata'
fastFile = 'output/fastPFMdata'
outputpath = workpath #default outputpath
fastLogDuration = 60 #defailt fast logging duration

KEY_ESC = '\x1b'
KEY_FAST = 'f'
KEY_DURATION = 'd'
HELPMSG ='\nPressure & Flow Monitor Help\n*************************************************************************\nPress "f" to start fast logging. A unique timestamped file will be created. Only one fast logging process can run at a time. \nThe duration of fast logging is set in PFMconfig.ini (if no config found, set to default) \nPress ESC to stop fast logging \nPress ESC again to exit pressure & flow monitor \n*************************************************************************'

row = 0  # To indicate if header needs to be written
fastrow = 0
fastLoggingTime = 10
isLogging = True
startFast = False
isFast = False

keyListen_fastLog = True
escape = False
timeLast = 2

#**Function Definitions**

def isData(): #keypress-function to know if there is input available
  return select.select([sys.stdin], [], [], 0) == ([sys.stdin], [], []) #keypress

os.chdir(os.path.dirname(workpath))

old_settings = termios.tcgetattr(sys.stdin) #keypress-save terminal settings

try:
    print(HELPMSG)
    
    config = configparser.ConfigParser()
    config.read('PFMconfig.ini')
    outputpath = config['DEFAULT']['outputAddress']#workpath #debug- need to read from config file later
    #slowFile = outputpath + slowFile
    
    tty.setcbreak(sys.stdin.fileno()) #keypress- set the terminal to character input mode
    
    ADC = ADS1256.ADS1256()
    ADC.ADS1256_init()

    timeStart = time.time()
    dNow = datetime.now()
    strDate = dNow.strftime("%m-%d-%Y_%H:%M:%S")
    slowFile = outputpath + slowFile + strDate + '.csv'
    
    
    
    with open(slowFile, 'w', newline='') as slowCSV:
    
        slowWriter = csv.writer(slowCSV, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        #fastWriter = csv.writer(fastCSV, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        
        if row == 0:
            slowWriter.writerow(
                ['Rod 1 (V)'] + ['Back 1 (V)'] + ['Rod 2 (V)'] + ['Back 2 (V)'] + ['Rod 3 (V)'] + ['Back 3 (V)'] + ['Flow 1 (V)'] + [
                    'Flow 2 (V)'] + ['Time (s)'])  # write header
            row += 1  # toggle to show that header has been written            
        
        while isLogging:
            ADC_Value = ADC.ADS1256_GetAll()
            timeDelta = time.time() - timeStart
            print('Delta')
            
            if startFast:
              dNow = datetime.now()
              strDate = dNow.strftime("%m-%d-%Y_%H:%M:%S")
              fastFile = outputpath + fastFile + strDate + '.csv'
              fastLogDuration = float(config['DEFAULT']['fastLogDuration'])
              timeStartFast = timeDelta
              print("debug 1")
              
            
            if timeDelta-timeLast > 1:
              slowWriter.writerow(
                  ['%lf' % (ADC_Value[0] * 5.0 / 0x7fffff)] + ['%lf' % (ADC_Value[1] * 5.0 / 0x7fffff)] + [
                      '%lf' % (ADC_Value[2] * 5.0 / 0x7fffff)] + ['%lf' % (ADC_Value[3] * 5.0 / 0x7fffff)] + [
                      '%lf' % (ADC_Value[4] * 5.0 / 0x7fffff)] + ['%lf' % (ADC_Value[5] * 5.0 / 0x7fffff)] + [
                      '%lf' % (ADC_Value[6] * 5.0 / 0x7fffff)] + ['%lf' % (ADC_Value[7] * 5.0 / 0x7fffff)] + ['%lf' % timeDelta])
              #print ("0 ADC = %lf"%(ADC_Value[0]*5.0/0x7fffff))
              row += 1
              slowCSV.flush()
            
            timeLast = timeDelta
            print('timeLast')
            
            if isFast:
            
                with open(fastFile, 'w', newline='') as fastCSV:
                    fastWriter = csv.writer(fastCSV, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
                    if startFast:
                        print('debug 2')
                        fastRow = 0
                        startFast = False
                        fastWriter.writerow(
                          ['Rod 1 (V)'] + ['Back 1 (V)'] + ['Rod 2 (V)'] + ['Back 2 (V)'] + ['Rod 3 (V)'] + ['Back 3 (V)'] + ['Flow 1 (V)'] + [
                          'Flow 2 (V)'] + ['Time (s)'])  # write header
                        fastrow += 1  # toggle to show that header has been written
                        fastCSV.flush()
                        print('debug 3')
                        
                    #print('debug 4')
                    fastWriter.writerow(
                      ['%lf' % (ADC_Value[0] * 5.0 / 0x7fffff)] + ['%lf' % (ADC_Value[1] * 5.0 / 0x7fffff)] + [
                        '%lf' % (ADC_Value[2] * 5.0 / 0x7fffff)] + ['%lf' % (ADC_Value[3] * 5.0 / 0x7fffff)] + [
                        '%lf' % (ADC_Value[4] * 5.0 / 0x7fffff)] + ['%lf' % (ADC_Value[5] * 5.0 / 0x7fffff)] + [
                        '%lf' % (ADC_Value[6] * 5.0 / 0x7fffff)] + ['%lf' % (ADC_Value[7] * 5.0 / 0x7fffff)] + ['%lf' % timeDelta])
                    fastrow += 1
                    fastCSV.flush()

            if isFast:
              if timeDelta - timeStartFast > fastLogDuration:
                escape = True 
                        
            #keypress- listen for input
            if isData():
              c = sys.stdin.read(1)
              if c == KEY_ESC: #esc key
                escape = True
              if c == KEY_FAST: #f key
                if not isFast:
                  startFast = True
                  isFast = True
                  print("started fast logging") 
                else:
                  print("Fast Logging already running. Press ESC to abort")   
            
            if escape:
              if not isFast:
                isLogging = False
              else:
                isFast = False
                escape = False
                fastFile = 'output/fastPFMdata'
                print("\r\nexited Fast Logging")

            if not isFast:
              time.sleep(1)  #1 Hz
            else:

              #fastLogProcess = subprocess.Popen(["python3", "fastLogging.py"]) #can't interact with this subprocess
              #startFast = False
              #time.sleep(1)
              time.sleep(0.001)  #1kHz *DEBUG: this implementation only leads to about 20 Hz real-time

except:
    GPIO.cleanup()
    termios.tcsetattr(sys.stdin, termios.TCSADRAIN, old_settings) #keypress-restore console state
    print("\r\nexited pressure & flow monitor (exception)")
    exit()
    
finally:
      termios.tcsetattr(sys.stdin, termios.TCSADRAIN, old_settings) #keypress-restore console state
      print("exited pressure & flow monitor (exited)")
      exit()
