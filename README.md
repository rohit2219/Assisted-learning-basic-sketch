
This is a very crude implementation of an assisted learning process which can analyse Linux logs and identify the best possible error.


The statistics part has not been implemented, but using a queue based ranking algorithm. Have to further refine this
with nltk.. To carry on this later..

1) written in emacs, so expected alignment problems..

2) Not the final piece but a sketch

3) basic idea is that the texts floser to the standard error messages in unix/linux have the highest possible option to detect an error.
If one analyses the words closer to the error message, Tokenize using
NLTK ,rank the error , , CONFIRM to the algorithm that this is the files/scripts which could be the problem, the algorithm will take care of analysing the error, 