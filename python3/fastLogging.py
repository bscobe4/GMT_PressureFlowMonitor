#!/usr/bin/python
# -*- coding:utf-8 -*-

import os
import time
import keyboard
import csv  # to write to csv file for nfs
import ADS1256
import RPi.GPIO as GPIO

workpath = '/home/pi/Documents/GMT_PressFlowMonitor/python3/'
slowFile = 'output/slowPFMdata.csv'
fastFile = 'output/fastPFMdata.csv'

row = 0  # To indicate if header needs to be written
numRows = 10
isLogging = True
fastLogging = True

os.chdir(os.path.dirname(workpath))

try:
    ADC = ADS1256.ADS1256()
    ADC.ADS1256_init()


    timeStart = time.time()

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
            csvfile.flush()
            
            if not fastLogging:
              time.sleep(1)  #1 Hz
            else:
              time.sleep(0.001)  #1kHz *DEBUG: this implementation only leads to about 20 Hz real-time


except:
    GPIO.cleanup()
    print("\r\nProgram end     ")
    exit()
