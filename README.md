# Blinds Control
Control the blinds in your room using Raspberry and Stepper Motors!</br>
Necessary Hardware:</br>
Raspberry Pi </br>
Provided 3D Model located in "model" folder </br>
<a href="https://www.amazon.com/Stepper-Bipolar-4-lead-Connector-Printer/dp/B00PNEQKC0/ref=sr_1_4?ie=UTF8&qid=1514777861&sr=8-4&keywords=nema+17" target="__blank">Nema 17</a>
<!-- ![Hardware](https://github.com/NickEngmann/BlindsControl/blob/raspberrypi/img/1.jpg) -->

## Video Example
(TBD) </br>

## Installation
Install Necessary Libraries
```bash
pip install python-firebase
pip install requests
sudo pip install git+https://github.com/adafruit/Adafruit-Motor-HAT-Python-Library
```

Setup I2C on your Raspberry Pi
https://learn.adafruit.com/adafruits-raspberry-pi-lesson-4-gpio-setup/configuring-i2c

## Running
```bash
python3 blindscontrol_controller_interface.py
```

## Different Alexa Commands Supported:

## 3D Model
![3DModel](https://github.com/NickEngmann/BlindsControl/blob/master/model/3DModel.png)