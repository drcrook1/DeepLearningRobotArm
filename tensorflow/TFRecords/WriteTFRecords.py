#!/usr/bin/env python3
"""
Author: David Crook
Copyright Microsoft Corporation 2017
"""
import PreProcess
import pandas as pd

#base directory to drop tf records for training
TF_REC_DEST = 'C:/data/robot_arm_data/tfrecords/'

LABELS_BASE_DIR = 'C:/data/robot_arm_data/fqlabels/'
LABEL_FILES = ['Run4', 'Run5', 'Run8', 'Run9']

def main():
    '''
    Main function which converts a label file into tf records
    '''
    for f in LABEL_FILES:
        PreProcess.write_records_from_file(LABELS_BASE_DIR + f + '.csv', TF_REC_DEST, 2, postfix = f)

if __name__ == "__main__":
    main()
