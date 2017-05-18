#!/usr/bin/env python3
"""
Author: David Crook
Copyright Microsoft Corporation 2017
"""

import tensorflow as tf
import time

def read_and_decode(filename_queue, image_shape, label_shape):
    '''
    USES TFRecord Reader to read and decode records from tfRecord files
    '''
    reader = tf.TFRecordReader()
    _, example = reader.read(filename_queue)
    features = tf.parse_single_example(example, features={
        'example': tf.FixedLenFeature([], tf.string),
        'label': tf.FixedLenFeature([], tf.string)
    })
    img_sample = tf.decode_raw(features['example'], tf.float32)
    img_sample = tf.reshape(img_sample, image_shape)
    label = tf.decode_raw(features['label'], tf.float32)
    label = tf.reshape(label, label_shape)
    label = tf.squeeze(label)
    return img_sample, label

def read_inputs(file_paths, batch_size, capacity=1000, min_after_dequeue=900, num_threads=2, img_shape=None, label_shape=None):
    '''
    Reads TFRecords and shuffles batches for use in a training session
    '''
    with tf.name_scope('input'):
        filename_queue = tf.train.string_input_producer(file_paths)
        example, label = read_and_decode(filename_queue, img_shape, label_shape)
        examples, labels = tf.train.shuffle_batch(
            [example, label], batch_size=batch_size, num_threads=num_threads,
            capacity=capacity, min_after_dequeue=min_after_dequeue
        )
        return examples, labels
