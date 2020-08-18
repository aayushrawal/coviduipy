#!/usr/bin/env python

from __future__ import print_function, division
import sys
from argparse import ArgumentParser

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

import pymoduleconnector
from pymoduleconnector import ModuleConnector
from pymoduleconnector import DataType
from pymoduleconnector import DataRecorder
from pymoduleconnector import DataPlayer
from pymoduleconnector import RecordingOptions

from pymoduleconnector.extras.auto import auto
from pymoduleconnector.ids import *

#from xt_modules_print_info import print_module_info
from xt_modules_print_info import print_sensor_settings
from xt_modules_record_playback_messages import start_recorder
from xt_modules_record_playback_messages import start_player

respiration_sensor_state_text = (
    "BREATHING", "MOVEMENT", "MOVEMENT TRACKING", "NO MOVEMENT", "INITIALIZING")
# User settings introduction

x4m200_par_settings = {'detection_zone': (0.4, 2),
                       'sensitivity': 1,
                       'tx_center_frequency': 3, # 3: TX 7.29GHz low band center frequency, 4: TX 8.748GHz low band center frequency.
                       'led_control': (XTID_LED_MODE_OFF, 0),
                       # initialize noisemap everytime when get start (approximately 120s)
                       'noisemap_control': 0b110,
                       # only uncomment the message when you need them to avoide confliction.
                       #    'output_control1': (XTS_ID_BASEBAND_IQ, 0),
                       #    'output_control2': (XTS_ID_BASEBAND_AMPLITUDE_PHASE, 0),
                       #    'output_control3': (XTS_ID_PULSEDOPPLER_FLOAT, 0),
                       #    'output_control4': (XTS_ID_PULSEDOPPLER_BYTE, 0),
                       #    'output_control5': (XTS_ID_NOISEMAP_FLOAT, 0),
                       #    'output_control6': (XTS_ID_NOISEMAP_BYTE, 0),
                       'output_control7': (XTS_ID_SLEEP_STATUS, 1),
                       #     'output_control8': (XTS_ID_RESP_STATUS, 1),
                       #    'output_control9': (XTS_ID_VITAL_SIGNS, 0),   
                       'output_control10': (XTS_ID_RESPIRATION_MOVINGLIST, 1),
                       #    'output_control11': (XTS_ID_RESPIRATION_DETECTIONLIST, 0)
                       }


def configure_x4m200(device_name, record=False, x4m200_settings=x4m200_par_settings):

    mc = ModuleConnector(device_name)
    x4m200 = mc.get_x4m200()

    print('Clearing buffer')
    while x4m200.peek_message_baseband_iq():
        x4m200.read_message_baseband_iq()
    while x4m200.peek_message_baseband_ap():
        x4m200.read_message_baseband_ap()
    while x4m200.peek_message_respiration_legacy():
        x4m200.read_message_respiration_legacy()
    while x4m200.peek_message_respiration_sleep():
        x4m200.read_message_respiration_sleep()
    while x4m200.peek_message_respiration_movinglist():
        x4m200.read_message_respiration_movinglist()
    while x4m200.peek_message_pulsedoppler_byte():
        x4m200.read_message_pulsedoppler_byte()
    while x4m200.peek_message_pulsedoppler_float():
        x4m200.read_message_pulsedoppler_float()
    while x4m200.peek_message_noisemap_byte():
        x4m200.read_message_noisemap_byte()
    while x4m200.peek_message_noisemap_float():
        x4m200.read_message_noisemap_float()

    print('Start recorder if recording is enabled')
    if record:
        start_recorder(mc)

    print('Ensuring no Xethru profile running')
    try:
        x4m200.set_sensor_mode(XTID_SM_STOP, 0)
    except RuntimeError:
        print('Xethru module could not enter stop mode')
    print('Loading new Xethru profile')

    x4m200.load_profile(XTS_ID_APP_RESPIRATION_2)

    print('Set parameters')
    for variable, value in x4m200_settings.items():
        try:
            if 'output_control' in variable:
                variable = 'output_control'
            setter_set = getattr(x4m200, 'set_' + variable)
        except AttributeError as e:
            print("X4M200 does not have a setter function for '%s'." % variable)
            raise e
        if isinstance(value, tuple):
            setter_set(*value)
        else:
            setter_set(value)
        print("Setting %s to %s" % (variable, value))

    print_sensor_settings(x4m200)

    print('Set module to RUN mode')
    try:
        x4m200.set_sensor_mode(XTID_SM_RUN, 0)  # RUN mode
    except RuntimeError:
        print('Xethru module cloud not enter run mode')

    return x4m200


def print_x4m200_messages(x4m200):
    try:
        lst_data = []
        ctr = True
        while ctr == True:
            while x4m200.peek_message_respiration_sleep(): # update every 1 second
                rdata = x4m200.read_message_respiration_sleep() 
                datavar="respiration_rate: {} movement_slow: {} movement_fast: {}".format(rdata.respiration_rate, rdata.movement_slow, rdata.movement_fast)
                #datavar = [rdata.respiration_rate, rdata.movement_slow, rdata.movement_fast]
                
                return(datavar)
                """ if(rdata.respiration_rate!=0):"""
                """ lst_data.append(datavar)
                if(count(lst_data)==10):
                    ctr = False
                    return(lst_data) """

            """ while x4m200.peek_message_respiration_movinglist(): # update every 1 second
                rdata = x4m200.read_message_respiration_movinglist() # update every 1 second
                return("message_respiration_movinglist:\ncounter: {} \nmovement_slow_items: {} \nmovement_fast_items: {}\n".format(rdata.counter, np.array(rdata.movement_slow_items), np.array(rdata.movement_fast_items))) """
    except:
        return('Messages output finish!')
    #sys.exit(0)


def main():
    
    device_name = '/dev/ttyACM0'
    if device_name:
        device_name = '/dev/ttyACM0'
    else:
        try:
            device_name = auto()[0]
        except:
            print("Port Error")
            raise
    #print_module_info(device_name)
    record = False
    x4m200 = configure_x4m200(
        device_name, record, x4m200_par_settings)

    """ else:
        player = start_player(meta_filename=args.meta_filename)
        mc = ModuleConnector(player, log_level=0)
        x4m200 = mc.get_x4m200() """
    print(print_x4m200_messages(x4m200))


if __name__ == "__main__":
    main()
