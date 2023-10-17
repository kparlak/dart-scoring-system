# Imaging System
## Dependencies
- [jetson-inference](https://github.com/dusty-nv/jetson-inference/tree/master)
## Installation
- Follow instructions for setting up the Jetson Nano: [Get Started With Jetson Nano Developer Kit](https://developer.nvidia.com/embedded/learn/get-started-jetson-nano-devkit#intro)
- Install the following:
    - Retarget Python to Python 3.6
        ```sh
        cd /usr/bin
        sudo rm python
        sudo ln -s python3 python
        ```
    - Install setuptools
        ```sh
        sudo pip3 install setuptools
        ```
    - Install pandas
        ```sh
        sudo pip3 install pandas
        ```
    - Manually install cython (version must be below 3)
        ```sh
        sudo pip3 install cython <3
        ```
- Follow instructions for building Jetson Inference repository from source: [Build the Project from Source](https://github.com/dusty-nv/jetson-inference/blob/master/docs/building-repo-2.md)
    - Comment out the following from build/install_pytorch.sh
        ```sh
        pip3 install cython
        ```
- Install third-party applications
    - Text Editor - GNU nano
        ```sh
        sudo apt-get install nano
        ```
    - Jetson Monitoring - [jetson-stats](https://pypi.org/project/jetson-stats/)
        ```sh
        sudo pip3 install jetson-stats
        ```
    - VNC Server - tightvncserver
        ```sh
        sudo apt-get install tightvncserver
        ```
- Enable fan output (if applicable)
    - Create execution script
        ```sh
        sudo touch /usr/local/bin/fan.sh
        ``` 
    - Add PWM value to script
        ```sh
        #!/bin/bash
        echo 150 > /sys/devices/pwm-fan/target_pwm
        exit 0
        ```
    - Set permissions
        ```sh
        sudo chmod 666 /sys/devices/pwm-fan/target_pwm
        sudo chmod a+x /usr/local/bin/fan.sh
        ```
    - Add to reboot
        ```sh
        sudo crontab -e
        @reboot /usr/local/bin/fan.sh
        ```
## Execution
[Jetson Inference](https://github.com/dusty-nv/jetson-inference/tree/master) was used to train custom datasets for dart recognition.
- Retraining an SSD model: [Re-Training SSD-Mobilenet](https://github.com/dusty-nv/jetson-inference/blob/master/docs/pytorch-ssd.md)
- Training a custom dataset: [Collecting your own Custom Detection Datasets](https://github.com/dusty-nv/jetson-inference/blob/master/docs/pytorch-collect-detection.md)

## License
MIT
