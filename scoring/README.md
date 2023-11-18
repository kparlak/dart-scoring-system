# Scoring

## Requirements
- Hardware
    - Raspberry Pi (3B+ or newer)
    - [Freenove Touchscreen](https://www.amazon.com/FREENOVE-Touchscreen-Raspberry-Capacitive-Driver-Free/dp/B0B455LDKH)
    - MicroSD Card (at least 64GB)
    - Power Supply to USB-C (15W)
- Software
    - [Raspberry Pi Imager](https://www.raspberrypi.com/documentation/computers/getting-started.html#raspberry-pi-imager)/Raspbian OS
    - Python (3.6 or greater)

## Setup
- Follow instructions for setting up the Raspberry Pi: [Getting started with your Raspberry Pi](https://www.raspberrypi.com/documentation/computers/getting-started.html)
- Follow instructions for setting up the FreeNove touchscreen: [Freenove Touchscreen Monitor for Raspberry Pi](https://github.com/Freenove/Freenove_Touchscreen_Monitor_for_Raspberry_Pi)
- Install the following:
    - Python package - [PyQt5](https://pypi.org/project/PyQt5/)
        ```
        sudo pip install PyQt5
        ```
    - Python package - [pyqt5-tools](https://pypi.org/project/pyqt5-tools/)
        ```
        sudo pip install pyqt5-tools
        ```
    - Database Browser - [sqlitebrowser](https://snapcraft.io/install/sqlitebrowser/raspbian)
        ```
        sudo apt update
        sudo apt install snapd
        sudo reboot
        sudo snap install core
        sudo snap install sqlitebrowser
        ```
- Set IP addresses
    - Configure DHCP to home network using onboard Wi-Fi
    - Set local Ethernet to static IP address
        ```
        10.0.0.2/8
        ```
        Port `5000` will be used for TCP/IP traffic to the [Imaging System](https://github.com/kparlak/dart-scoring-system/tree/main/imaging)
- Initialize database
    - Make database directory
        ```
        sudo mkdir /data
        sudo chmod 777 /data
        ```
    - Create tables
        ```
        ./initialize_database.py
        ```
    An SQLite database will be created at `/data/DARTS.db` referencing the entity relationship:
    ![DARTS Database](documentation/Database_Diagram.png)

## Execution

### Application
- Generate python files from Qt ui files
    ```
    python -m PyQt5.uic.pyuic <file.ui> -o <file.py> -x
    ```
- Start state machine
    ```
    ./main_scoring.py
    ```

## License
MIT
