# Dart Scoring System

EN.525.743 - Embedded Systems Development Laboratory project

This project was completed within the Embedded Systems Development Laboratory course at Johns Hopkins University. It uses a GPU-based processor to detect darts on a dartboard via object detection and sends dart location information to a Raspberry Pi so dart games can be automatically scored. Interaction with the system occurs through a GUI on the Raspberry Pi.

# Imaging System
The Imaging System uses a Nivida Jetson Nano as the main processor. This system relies upon [Jetson Inference](https://github.com/dusty-nv/jetson-inference/) from Nvidia to collect, train, and use custom detection datasets. Single Shot Detection MultiBox Detector algorithms were used with trained models to identify darts. Information on the imaging system can be viewed [here](imaging/README.md)

# Scoring System
The Scoring System uses a Raspberry Pi 3B+ as the main processor. This system implements two dart games, '501' and 'Around the World'. Information on the Scoring System can be viewed [here](scoring/README.md)
