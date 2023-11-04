# Imaging
## Dependencies
- [jetson-inference](https://github.com/dusty-nv/jetson-inference/tree/master)
## Installation
- Follow instructions for setting up the Jetson Nano: [Get Started With Jetson Nano Developer Kit](https://developer.nvidia.com/embedded/learn/get-started-jetson-nano-devkit#intro)
- Install the following:
    - Retarget Python to Python 3.6
        ```
        cd /usr/bin
        sudo rm python
        sudo ln -s python3 python
        ```
    - Install setuptools
        ```
        sudo pip3 install setuptools
        ```
    - Install pandas
        ```
        sudo pip3 install pandas
        ```
    - Manually install cython (version must be below 3)
        ```
        sudo pip3 install cython <3
        ```
- Follow instructions for building Jetson Inference repository from source: [Build the Project from Source](https://github.com/dusty-nv/jetson-inference/blob/master/docs/building-repo-2.md)
    - Comment out the following from build/install_pytorch.sh
        ```
        pip3 install cython
        ```
- Install third-party applications
    - Text Editor - GNU nano
        ```
        sudo apt-get install nano
        ```
    - Jetson Monitoring - [jetson-stats](https://pypi.org/project/jetson-stats/)
        ```
        sudo pip3 install jetson-stats
        ```
    - VNC Server - tightvncserver
        ```
        sudo apt-get install tightvncserver
        ```
    - Open Computer Vision - [open-cv](https://pypi.org/project/opencv-python/)
        ```
        sudo pip install opencv-python
        ```
    - Array Computing - [numpy](https://pypi.org/project/numpy/)
        ```
        sudo pip install numpy
        ```
- Enable fan output (if applicable)
    - Create execution script
        ```
        sudo touch /usr/local/bin/fan.sh
        ``` 
    - Add PWM value to script
        ```
        #!/bin/bash
        echo 150 > /sys/devices/pwm-fan/target_pwm
        exit 0
        ```
    - Set permissions
        ```
        sudo chmod 666 /sys/devices/pwm-fan/target_pwm
        sudo chmod a+x /usr/local/bin/fan.sh
        ```
    - Add to reboot
        ```
        sudo crontab -e
        @reboot /usr/local/bin/fan.sh
        ```
## Execution
[Jetson Inference](https://github.com/dusty-nv/jetson-inference/tree/master) was used to train custom datasets for dart recognition.
- Retraining an SSD model: [Re-Training SSD-Mobilenet](https://github.com/dusty-nv/jetson-inference/blob/master/docs/pytorch-ssd.md)
- Collecting a custom dataset: [Collecting your own Custom Detection Datasets](https://github.com/dusty-nv/jetson-inference/blob/master/docs/pytorch-collect-detection.md)
- Running application:
    - Setup environment
        ```
        . setup.sh
        ```
    - Start state machine
        ```
        ./main_imaging.py
        ```
## License
MIT
