#!/usr/bin/env python3
"""
Author: David Crook
Copyright Microsoft Corporation 2017
"""

import tensorflow as tf

def variable_on_cpu(name, shape, initializer, dtype=tf.float32):
    '''
    Create a shareable variable.
    '''

    with tf.device('/cpu:0'):
        var = tf.get_variable(name, shape, initializer=initializer, dtype=dtype)
    return var

def mlp_layer(X, n_in, n_out, scope, name_postfix = None, act_func=None):
    '''
    Creates a feed forward layer.
    '''
    if name_postfix is not None:
        W = variable_on_cpu('W' + name_postfix, [n_in, n_out],
                            tf.contrib.layers.xavier_initializer(dtype=tf.float32))
        B = variable_on_cpu('B' + name_postfix, [n_out], tf.constant_initializer(0.0))
    else:
        W = variable_on_cpu('W', [n_in, n_out],
                            tf.contrib.layers.xavier_initializer(dtype=tf.float32))
        B = variable_on_cpu('B', [n_out], tf.constant_initializer(0.0))
    if act_func is not None:
        activation = act_func(tf.matmul(X, W) + B, name=scope.name)
    else:
        activation = tf.add(tf.matmul(X, W), B, name=scope.name)
    #reports full activation spectrum
    tf.summary.histogram('{}/activations'.format(scope.name), activation)
    #reports fraction of zeros (dead neurons) in activation
    tf.summary.scalar('{}/sparsity'.format(scope.name), tf.nn.zero_fraction(activation))
    return activation

def cnn_layer(X, shape, strides, scope, name_postfix=None, padding='SAME'):
    '''
    Create a convolution layer.
    '''
    if name_postfix is not None:
        kernel = variable_on_cpu('kernel' + name_postfix, shape,
                                 tf.contrib.layers.xavier_initializer(dtype=tf.float32))
        biases = variable_on_cpu('b' + name_postfix, [shape[-1]], tf.constant_initializer(0.0))
    else:
        kernel = variable_on_cpu('kernel', shape,
                                 tf.contrib.layers.xavier_initializer(dtype=tf.float32))
        biases = variable_on_cpu('b', [shape[-1]], tf.constant_initializer(0.0))
    conv = tf.nn.conv2d(X, kernel, strides, padding=padding)
    activation = tf.nn.relu(conv + biases, name=scope.name)
    #reports the full activation spectrum
    tf.summary.histogram('{}/activations'.format(scope.name), activation)
    #reports fraction of zeros (dead neurons) in activation
    tf.summary.scalar('{}/sparsity'.format(scope.name), tf.nn.zero_fraction(activation))
    return activation

def pool_layer(X, window_size, strides, scope, padding='SAME'):
    '''
    Creates a max pooling layer
    '''
    return tf.nn.max_pool(X, ksize=window_size, strides=strides,
                          padding=padding, name=scope.name)
