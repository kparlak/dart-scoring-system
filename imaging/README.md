# Imaging

## Requirements
- Hardware
    - Nvidia Jetson Nano Developer Kit
    - [Jetson Nano Metal Case w/ PWM Fan](https://www.amazon.com/dp/B07Z2MFTYC)
    - [Waveshare Wireless NIC Module for Jetson Nano](https://www.amazon.com/dp/B07SGDRG34)
    - MicroSD Card (at least 64GB)
    - Power Supply to 2.5mm (20W)
- Software
    - [jetson-inference](https://github.com/dusty-nv/jetson-inference/tree/master)
    - Python (3.6 or greater)

## Setup
- Follow instructions for setting up the Jetson Nano: [Get Started With Jetson Nano Developer Kit](https://developer.nvidia.com/embedded/learn/get-started-jetson-nano-devkit#intro)
- Follow instructions for assembling up the Jetson Nano case: [Jetson Nano Case](https://www.waveshare.com/wiki/Jetson_Nano_Case_(C))
- Install the following:
    - Retarget Python to Python 3
        ```
        cd /usr/bin
        sudo rm python
        sudo ln -s python3 python
        ```
    - Python package - [setuptools](https://pypi.org/project/setuptools/)
        ```
        sudo pip3 install setuptools
        ```
    - Python package - [pandas](https://pypi.org/project/pandas/)
        ```
        sudo pip3 install pandas
        ```
    - Python package - [cython](https://pypi.org/project/Cython/) (version must be below 3)
        ```
        sudo pip3 install cython <3
        ```
    - Python package - [open-cv](https://pypi.org/project/opencv-python/)
        ```
        sudo pip install opencv-python
        ```
    - Python package - [numpy](https://pypi.org/project/numpy/)
        ```
        sudo pip install numpy
        ```
    - Text Editor - [GNU nano](https://www.nano-editor.org/)
        ```
        sudo apt-get install nano
        ```
    - Jetson Monitoring - [jetson-stats](https://pypi.org/project/jetson-stats/)
        ```
        sudo pip3 install jetson-stats
        ```
    - VNC Server - [tightvncserver](https://www.tightvnc.com/)
        ```
        sudo apt-get install tightvncserver
        ```
- Follow instructions for building Jetson Inference repository from source: [Build the Project from Source](https://github.com/dusty-nv/jetson-inference/blob/master/docs/building-repo-2.md)
    - Comment out the following from `build/install_pytorch.sh`
        ```
        pip3 install cython
        ```
- Enable fan output
    - Create execution script
        ```
        sudo nano /usr/local/bin/fan.sh
        ```
        ```
        #!/bin/bash
        echo 150 > /sys/devices/pwm-fan/target_pwm
        exit 0
        ```
        ```
        sudo chmod 666 /sys/devices/pwm-fan/target_pwm
        sudo chmod a+x /usr/local/bin/fan.sh
        ```
    - Add to reboot
        ```
        sudo crontab -e
        @reboot /usr/local/bin/fan.sh
        ```
- Set IP addresses
    - Configure DHCP to home network using onboard Wi-Fi
    - Set local Ethernet to static IP address
        ```
        10.0.0.3/8
        ```
    Port `5000` will be used for TCP/IP traffic to the [Scoring System](https://github.com/kparlak/dart-scoring-system/tree/main/scoring)

## Execution

### Training
[Jetson Inference](https://github.com/dusty-nv/jetson-inference/tree/master) was used to train custom datasets for dart recognition:
- Retraining an SSD model: [Re-Training SSD-Mobilenet](https://github.com/dusty-nv/jetson-inference/blob/master/docs/pytorch-ssd.md)
- Collecting a custom dataset: [Collecting your own Custom Detection Datasets](https://github.com/dusty-nv/jetson-inference/blob/master/docs/pytorch-collect-detection.md)

### Application
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
