# Get access to parent directory
import os, sys
sys.path.append(os.path.dirname(os.getcwd()))

# Imports
import tensorflow as tf


class SoftAttention(tf.keras.Model):
    def __init__(self, units):
        """
            units:      number of internal units per layer
        """
        super(SoftAttention, self).__init__()
        
        # TODO
        
        pass

    def call(self, features, hidden):
        """
            features:   features observed from image
            hidden:     hidden state of the decoder network (RNN) from previous iteration
        """
        
        # TODO
        
        return None
    
    
class HardAttention(tf.keras.Model):
    
    # TODO 1: Define custom loss function?
    # TODO 2: Include running average b_k
    # TODO 3: Add entropy H[s]
    
    def __init__(self, units):
        """
            units:      number of internal units per layer
        """
        super(HardAttention, self).__init__()
        
        self.feature_weights = tf.keras.layers.Dense(units)
        self.hidden_weights = tf.keras.layers.Dense(units)
        self.attention_weights = tf.keras.layers.Dense(1)

    def call(self, features, hidden):
        """
            features:   features observed from image, output of encoder,   shape: (batch_size, num_features, embedding_dim) 
            hidden:     hidden state of the decoder network (RNN) from previous iteration, shape: (batch_size, hidden_size)
        """

        # hidden_expanded, shape: (batch_size, 1, hidden_size)
        hidden_expanded = tf.expand_dims(hidden, 1)

        # Calculate unnormalized attention weights;
        # unnormal_attent_weights, shape: (batch_size, num_features, hidden_size)
        unnormal_attent_weights = tf.nn.tanh(self.feature_weights(features) + self.hidden_weights(hidden_expanded))
        
        # Normalize attention weights to turn them into a probability-distribution;
        # attention_weights_alpha, shape: (batch_size, num_features, 1)
        attention_weights_alpha = tf.nn.softmax(self.attention_weights(unnormal_attent_weights), axis=1)
        
        # Select index of feature to attend, i.e. attention location
        # attention_location_s, shape = scalar = ();
        if tf.squeeze(tf.argmax(tensorflow_probability.distributions.Multinomial(total_count=1., probs=[0.5,0.5]))) == 0:
            # With 50% chance, set the sampled attention location s to its expected value alpha
            attention_location_s = tf.squeeze(tf.argmax(attention_weights_alpha, axis=-1))
            
        else:
            # Select feature based on stochastic sampling from Multinoulli (categorical) distribution with probabilities attention_weights_alpha
            one_hot_selection = tensorflow_probability.distributions.Multinomial(total_count=1., probs=attention_weights_alpha)
            attention_location_s = tf.squeeze(tf.argmax(one_hot_selection, axis=-1))
        
        
        # Construct context vector by selecting stochastically chosen feature to pay attention to;
        # context_vector_z, shape after selection of feature: (batch_size, embedding_dim)
        context_vector_z = features[attention_location_s,:]

        return context_vector_z, attention_weights_alpha
    

