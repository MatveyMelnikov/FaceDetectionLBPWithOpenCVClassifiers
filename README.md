# Viola Jones With OpenCV Classifiers

Python implementation of the face detection algorithm by Paul Viola and Michael J. Jones with OpenCV classifiers.
In fact, it is a simple compilation of two projects from [Simon Hohberg](https://github.com/Simon-Hohberg) and [Tommy Chheng](https://github.com/tc). Thanks!

## Install

Run:

    pip install -e <path to viola-jones>

## How to use

File [main.py](https://github.com/MatveyMelnikov/ViolaJonesWithOpenCVClassifiers/blob/master/main.py) demonstrates face detection in multiple photos.
With the [PrepareDataset.py](https://github.com/MatveyMelnikov/ViolaJonesWithOpenCVClassifiers/blob/master/PrepareDataset.py) file you can prepare your own photos for training or testing. OpenCV classifier is located [here](https://github.com/MatveyMelnikov/ViolaJonesWithOpenCVClassifiers/blob/master/classifiers/haarcascade_frontalface_default.xml). It is parsed by [OpenCVClassifierParser](https://github.com/MatveyMelnikov/ViolaJonesWithOpenCVClassifiers/blob/master/OpenCVClassifierParser.py).

## Links
* [jviolajones](https://github.com/tc/jviolajones) - readable implementation of Viola-Jones algorithm in Java;
* [Viola-Jones](https://github.com/Simon-Hohberg/Viola-Jones) - extremely simple and clear implementation of the Viola-Jones algorithm in python;
* [OpenCV](https://github.com/opencv/opencv) - already trained classifiers and augmented implementation of the algorithm.
