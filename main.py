import numpy as np
import tensorflow as tf

# Hyper Parameters
num_iterations = 100
batch_size = 100
learning_rate = 0.001

dim_word  = 2000
dim_embed = 1500

hidden_size = 50

# Load training and test dataset
train_x = None
train_y = None

test_x = None
test_y = None

# BASIC STRUCTURE
# INPUT -> EMBEDDING ENCODE -> ENCODE -> Thought Vector -> DECODE -> OUTPUT

# Neural Network
inputs = tf.placeholder(tf.int32, shape=[None, None, dim_word]) # [batch_size, sequence_length, word_dimension]

#  Embed
embedding_matrix = tf.Variable(tf.random_normal([dim_word, dim_embed], stddev=1/np.sqrt(dim_word)), name="embedding_matrix")
embedded = tf.nn.embedding_lookup(embedding_matrix, inputs)

#  Encode
encoder = tf.contrib.cudnn_rnn.CudnnCompatibleGRUCell(hidden_size)
encoder_outputs, encoder_final_state = tf.nn.dynamic_rnn(encoder, embedded)

#  Decode
decoder_input = tf.constant()
decoder = tf.contrib.cudnn_rnn.CudnnCompatibleGRU(hidden_size)
decoder_outputs, decoder_final_state = tf.nn.dynamic_rnn(decoder, decoder_input, initial_state=encoder_final_state)

# Train
loss = tf.contrib.seq2seq.sequence_loss(logits=, targets=, weights=)
optimize = tf.train.AdamOptimizer(learning_rate=learning_rate).minimize(loss)

# Run
sess = tf.Session()

if __name__ == '__main__':
    sess.run(tf.global_variables_initializer())

    for i in range(num_iterations):
        feed_dict=None
        sess.run(optimize, feed_dict=feed_dict)