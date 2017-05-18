#!/usr/bin/env python3
"""
Author: David Crook
Copyright Microsoft Corporation 2017
"""

import tensorflow as tf
import time
import TFNetworks.Vgg3ServoBot as vgg3
import CONSTANTS as CONSTANTS
import TFNetworks.Inputs as Inputs
from scipy import misc
import numpy as np
import pickle

model = vgg3.Vgg3Model()

def gradients_summary(gradients):
    for grad, var in gradients:
        if grad is not None:
            tf.summary.histogram('{}/gradients'.format(var.op.name), grad)


def create_sess_ops():
    '''
    Creates and returns operations needed for running
    a tensorflow training session
    '''
    GRAPH = tf.Graph()
    with GRAPH.as_default():
        examples, labels = Inputs.read_inputs(CONSTANTS.RecordPaths,
                                              batch_size=CONSTANTS.BATCH_SIZE,
                                              img_shape=CONSTANTS.IMAGE_SHAPE,
                                              num_threads=CONSTANTS.INPUT_PIPELINE_THREADS,
                                              label_shape=CONSTANTS.LABEL_SHAPE)
        examples = tf.reshape(examples, [-1, CONSTANTS.IMAGE_SHAPE[0], CONSTANTS.IMAGE_SHAPE[1], CONSTANTS.IMAGE_SHAPE[2]])
        logits = model.inference(examples)
        loss = model.loss(logits, labels)
        OPTIMIZER = tf.train.AdamOptimizer(CONSTANTS.LEARNING_RATE)
        gradients = OPTIMIZER.compute_gradients(loss)
        apply_gradient_op = OPTIMIZER.apply_gradients(gradients)
        gradients_summary(gradients)
        summaries_op = tf.summary.merge_all()
        return [apply_gradient_op, summaries_op, loss, logits], GRAPH

def main():
    '''
    Run and Train CIFAR 10
    '''
    print('starting...')
    ops, GRAPH = create_sess_ops()
    total_duration = 0.0
    with tf.Session(graph=GRAPH) as SESSION:
        COORDINATOR = tf.train.Coordinator()
        THREADS = tf.train.start_queue_runners(SESSION, COORDINATOR)
        SESSION.run(tf.global_variables_initializer())
        SUMMARY_WRITER = tf.summary.FileWriter(CONSTANTS.mounted_basedir + 'Tensorboard/' + CONSTANTS.MODEL_NAME, graph=GRAPH)
        GRAPH_SAVER = tf.train.Saver()

        for EPOCH in range(CONSTANTS.EPOCHS):
            duration = 0
            error = 0.0
            start_time = time.time()
            for batch in range(CONSTANTS.MINI_BATCHES):
                _, summaries, cost_val, prediction = SESSION.run(ops)
                error += cost_val
            duration += time.time() - start_time
            total_duration += duration
            SUMMARY_WRITER.add_summary(summaries, EPOCH)
            print('Epoch %d: loss = %.2f (%.3f sec)' % (EPOCH, error, duration))
            if EPOCH == CONSTANTS.EPOCHS - 1 or error < 0.005:
                print(
                    'Done training for %d epochs. (%.3f sec)' % (EPOCH, total_duration)
                )
                break
            if EPOCH % CONSTANTS.CHECKPOINT_EPOCHS == 0:
                GRAPH_SAVER.save(SESSION, CONSTANTS.mounted_basedir + 'models/' + CONSTANTS.MODEL_NAME + '.model')
                with open(CONSTANTS.mounted_basedir + 'models/' + CONSTANTS.MODEL_NAME + '.pkl', 'wb') as output:
                    pickle.dump(model, output)
        GRAPH_SAVER.save(SESSION, CONSTANTS.mounted_basedir + 'models/' + CONSTANTS.MODEL_NAME + '.model')
        with open(CONSTANTS.mounted_basedir + 'models/' + CONSTANTS.MODEL_NAME + '.pkl', 'wb') as output:
            pickle.dump(model, output)
        COORDINATOR.request_stop()
        COORDINATOR.join(THREADS)

if __name__ == "__main__":
    main()

