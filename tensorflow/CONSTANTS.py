#!/usr/bin/env python3
"""
Author: David Crook
Copyright Microsoft Corporation 2017
"""

MODEL_NAME = "CIFAR_10_VGG3_50neuron_1pool_33_55_filters_1e-4lr_adam"

DEBUG = True

IMAGE_SHAPE = (480, 720, 3)
LABEL_SHAPE = (4)
NUM_CLASSES = 4

INPUT_PIPELINE_THREADS = 16
#batch size * minibatches = # samples in data set or greater.
BATCH_SIZE = 1000
MINI_BATCHES = 50
EPOCHS = 500
CHECKPOINT_EPOCHS = 25
LEARNING_RATE = 1e-4

mounted_basedir = 'C:/data/robot_arm_data/tfrecords/'

RecordPaths = [
    mounted_basedir + '1Run4.tfrecord',
    mounted_basedir + '1Run5.tfrecord',
    mounted_basedir + '1Run8.tfrecord',
    mounted_basedir + '1Run9.tfrecord',
    mounted_basedir + '2Run4.tfrecord',
    mounted_basedir + '2Run5.tfrecord',
    mounted_basedir + '2Run8.tfrecord',
    mounted_basedir + '2Run9.tfrecord',
]
