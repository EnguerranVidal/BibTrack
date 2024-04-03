######################## IMPORTS ########################
import os
import csv

import pandas as pd
import numpy as np
import time


######################## FUNCTIONS ########################
def loadSettings(path):
    parameters = {}
    with open(path, "r") as file:
        lines = file.readlines()
    for i in range(len(lines)):
        line = lines[i].split('=')
        if line[0] in ['OPENED_RECENTLY']:
            split_setting = line[1].split(',')
            for j in range(len(split_setting)):
                split_setting[j] = split_setting[j].rstrip('\n')
            if len(split_setting) == 1 and split_setting[0] == '':
                parameters[line[0]] = []
            else:
                parameters[line[0]] = split_setting
        elif line[0] in ['MAXIMIZED', 'DARK_THEME']:
            parameters[line[0]] = bool(int(line[1].rstrip("\n")))
        else:
            parameters[line[0]] = line[1].rstrip("\n")
    return parameters


def saveSettings(parameters, path):
    with open(path, "r") as file:
        lines = file.readlines()
    with open(path, "w") as file:
        for i in range(len(lines)):
            line = lines[i].split('=')
            setting = line[0]
            if setting in ['OPENED_RECENTLY']:
                file.write(setting + '=' + ','.join(parameters[setting]) + '\n')
            elif setting in ['MAXIMIZED', 'DARK_THEME']:
                file.write(setting + '=' + str(int(parameters[setting])) + '\n')
            else:
                file.write(setting + '=' + str(parameters[setting]) + '\n')
