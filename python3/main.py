#!/usr/bin/python
# -*- coding:utf-8 -*-

import os
import time
import datetime
import csv  # to write to csv file for nfs
import ADS1256
import RPi.GPIO as GPIO

workpath = '/home/pi/Documents/GMT_PressFlowMonitor/python3/'
slowFile = 'output/slowPFMdata.csv'
fastFile = 'output/fastPFMdata.csv'

#**Object Definitions**
class logFile:
  def __init__(self, filePath, sampleTime):
    self.fileDate = datetime.now()
    self.fileDateStr = self.fileDate.strftime("%m/%d/%Y, %H:%M:%S")
    self.filePath = filePath       
    self.row = 0
    self.timeStart = time.time()#timeStart
    self.sampleTime = sampleTime
    self.ADC = ADC
    self.ADC = ADS1256.ADS1256()


    
  def recordData():
    self.ADC.ADS1256_init()
    with open(self.filePath, 'w', newline='') as csvfile:
        dataWriter = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        if self.row == 0:
            dataWriter.writerow(
                ['Rod 1 (V)'] + ['Back 1 (V)'] + ['Rod 2 (V)'] + ['Back 2 (V)'] + ['Rod 3 (V)'] + ['Back 3 (V)'] + ['Flow 1 (V)'] + [
                    'Flow 2'] + ['Time (s)'])  # write header
            self.row += 1  # toggle to show that header has been written
        #while (row <= numRows): #DEBUG replace with GPIO trigger
        while isLogging:
            ADC_Value = self.ADC.ADS1256_GetAll()
            timeDelta = time.time() - self.timeStart
            
            dataWriter.writerow(
                ['%lf' % (ADC_Value[0] * 5.0 / 0x7fffff)] + ['%lf' % (ADC_Value[1] * 5.0 / 0x7fffff)] + [
                    '%lf' % (ADC_Value[2] * 5.0 / 0x7fffff)] + ['%lf' % (ADC_Value[3] * 5.0 / 0x7fffff)] + [
                    '%lf' % (ADC_Value[4] * 5.0 / 0x7fffff)] + ['%lf' % (ADC_Value[5] * 5.0 / 0x7fffff)] + [
                    '%lf' % (ADC_Value[6] * 5.0 / 0x7fffff)] + ['%lf' % (ADC_Value[7] * 5.0 / 0x7fffff)] + ['%lf' % timeDelta])
            #print ("0 ADC = %lf"%(ADC_Value[0]*5.0/0x7fffff))
            self.row += 1
            csvfile.flush()
            time.sleep(self.sampleTime)
            
            
#            if not fastLogging:
#              time.sleep(1)  #1 Hz
#            else:
#              time.sleep(0.001)  #1kHz *DEBUG: this implementation only leads to about 20 Hz real-time
              
#Change directory to directory of main file
os.chdir(os.path.dirname(workpath))

try:
    #ADC = ADS1256.ADS1256()
    #ADC.ADS1256_init()


    #    while(1):
    #        ADC_Value = ADC.ADS1256_GetAll()
    #        print ("0 ADC = %lf"%(ADC_Value[0]*5.0/0x7fffff)) #cylinder 1 back
    #        print ("1 ADC = %lf"%(ADC_Value[1]*5.0/0x7fffff)) #cylinder 1 rod
    #        print ("2 ADC = %lf"%(ADC_Value[2]*5.0/0x7fffff)) #cylinder 2 back
    #        print ("3 ADC = %lf"%(ADC_Value[3]*5.0/0x7fffff)) #cylinder 2 rod
    #        print ("4 ADC = %lf"%(ADC_Value[4]*5.0/0x7fffff)) #cylinder 3 back
    #        print ("5 ADC = %lf"%(ADC_Value[5]*5.0/0x7fffff)) #cylinder 3 rod
    #        print ("6 ADC = %lf"%(ADC_Value[6]*5.0/0x7fffff)) #flow sensor 1
    #        print ("7 ADC = %lf"%(ADC_Value[7]*5.0/0x7fffff)) #flow sensor 2 (if used)
    #        print ("\33[9A")
    #row = 0  # To indicate if header needs to be written
    #numRows = 10
    isLogging = True
    fastLogging = False
    #timeStart = time.time()
    
    slowLogfile = logFile(slowFile, 1) 

    slowLogfile.recordData()

except:
    GPIO.cleanup()
    print("\r\nProgram end     ")
    exit()
