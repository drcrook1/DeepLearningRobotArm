'''
Author: David Crook
Module which contains functions for pre-processing image data
'''
import math
import os
import tensorflow as tf
import pandas as pd
import numpy as np
from scipy import misc

def bytes_feature(value):
    '''
    Creates a TensorFlow Record Feature with value as a byte array
    '''
    return tf.train.Feature(bytes_list=tf.train.BytesList(value=[value]))

def int64_feature(value):
    '''
    Creates a TensorFlow Record Feature with value as a 64 bit integer.
    '''
    return tf.train.Feature(int64_list=tf.train.Int64List(value=[value]))

def write_record(dest_path, df):
    '''
    Writes an actual TF record from a data frame
    '''
    writer = tf.python_io.TFRecordWriter(dest_path)
    for i in range(len(df)):
        example = tf.train.Example(features=tf.train.Features(feature={
            'example': bytes_feature(df['image'][i]),
            'label': bytes_feature(np.fromstring(df['label'][i][1:-1], dtype=np.float32, sep=' ').tostring())
        }))
        writer.write(example.SerializeToString())
    writer.close()

def read_image_to_bytestring(path):
    '''
    Reads an image from a path and converts it
    to a flattened byte string
    '''
    img = misc.imread(path).astype(np.float32) / 255.0
    return img.reshape((480, 720, 3)).flatten().tostring()

def write_records_from_file(labels_file, dest_folder, num_records, postfix = ''):
    '''
    Takes a label file as a path and converts entries into a tf record
    for image classification.
    '''
    if not os.path.exists(dest_folder):
        os.makedirs(dest_folder)
    labels = pd.read_csv(labels_file)
    #read image, flatten and then convert to a string
    img_arrs = [read_image_to_bytestring(path) for path in labels['examplepath']]
    labels['image'] = pd.Series(img_arrs)
    start_idx = 0
    ex_per_rec = math.ceil(len(labels) / num_records)
    for i in range(1, num_records):
        rec_path = dest_folder + str(i) + postfix + '.tfrecord'
        write_record(rec_path, labels.loc[start_idx:(ex_per_rec * i) - 1].reset_index())
        start_idx += ex_per_rec
        print('wrote record: ', i)
    final_rec_path = dest_folder + str(num_records) + postfix + '.tfrecord'
    write_record(final_rec_path, labels.loc[ex_per_rec * (num_records - 1):].reset_index())
    print('wrote record: ', num_records)
    print('finished writing records...')

