## RNN
- The RNN is essentially a neural network with delay time added while predicting the output
- For the backprop to work the network needs to be acyclic graph. But the delay connection like below makes the network have cycles. The solution to the problem is to unroll the network across time and do the training.
- The Encoder, $g$ and Decoder have shared parameters (are the same) across time. So the gradients with respect to the parameters is just summation across the gradients from each time step for the respective network i.e. either encoder, decoder, $g$.
    -  This follows from the shared parameter logic that final gradient at the time of backprop for a shared parameter is the sum of gradients from each copy. Explained in the previous lecture.
