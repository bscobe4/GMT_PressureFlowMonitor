#!/usr/bin/python
# -*- coding:utf-8 -*-


import time
import csv  # to write to csv file for nfs
import ADS1256
import RPi.GPIO as GPIO

try:
    ADC = ADS1256.ADS1256()
    ADC.ADS1256_init()


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
    row = 0  # To indicate if header needs to be written
    numRows = 10

    with open('pressureFlowData.csv', 'w', newline='') as csvfile:
        dataWriter = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        if row == 0:
            dataWriter.writerow(
                ['Rod 1'] + ['Back 1'] + ['Rod 2'] + ['Back 2'] + ['Rod 3'] + ['Back 3'] + ['Flow 1'] + [
                    'Flow 2'])  # write header
            row += 1  # toggle to show that header has been written
        while (row <= numRows): #DEBUG replace with GPIO trigger
            ADC_Value = ADC.ADS1256_GetAll()
            dataWriter.writerow(
                ['%lf' % (ADC_Value[0] * 5.0 / 0x7fffff)] + ['%lf' % (ADC_Value[1] * 5.0 / 0x7fffff)] + [
                    '%lf' % (ADC_Value[2] * 5.0 / 0x7fffff)] + ['%lf' % (ADC_Value[3] * 5.0 / 0x7fffff)] + [
                    '%lf' % (ADC_Value[4] * 5.0 / 0x7fffff)] + ['%lf' % (ADC_Value[5] * 5.0 / 0x7fffff)] + [
                    '%lf' % (ADC_Value[6] * 5.0 / 0x7fffff)] + ['%lf' % (ADC_Value[7] * 5.0 / 0x7fffff)])
            row += 1


except:
    GPIO.cleanup()
    print("\r\nProgram end     ")
    exit()
