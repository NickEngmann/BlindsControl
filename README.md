# Blinds Control
Control the blinds in your room using Raspberry and Stepper Motors!</br>
Click the image below to watch the video. </br>
[![Watch the video](https://github.com/NickEngmann/BlindsControl/blob/master/img/youtube.png)](https://youtu.be/fzvNv4QeY4A)

## Necessary Hardware:
<a href="https://www.adafruit.com/product/3055" target="__blank">Raspberry Pi 3 </a></br>
<a href="https://github.com/NickEngmann/BlindsControl/tree/master/model" target="__blank">2x Motor Housing </a></br>
<a href="https://github.com/NickEngmann/BlindsControl/tree/master/model" target="__blank">2x Rod Controller </a></br>
2x <a href="https://www.amazon.com/Stepper-Bipolar-4-lead-Connector-Printer/dp/B00PNEQKC0/ref=sr_1_4?ie=UTF8&qid=1514777861&sr=8-4&keywords=nema+17" target="__blank">Nema 17 Stepper Motor</a>

[![Hardware](https://github.com/NickEngmann/BlindsControl/blob/master/img/1.jpg)]

## Instructions:
If you want to emulate this project the instructions are fairly simple. Attach the 3D printed portions to your motor, and wire the Motor appropriately to the Adafruit Motor Hat. Attach the Rod Controller to your blinds, and screw the Motor Container to the window frame. 

### Raspberry PI Installation
To get the Raspberry Pi up and running we need to install the necessary libraries

```bash
pip install python-firebase
pip install requests
sudo pip install git+https://github.com/adafruit/Adafruit-Motor-HAT-Python-Library
```

Setup I2C on your Raspberry Pi: </br>
https://learn.adafruit.com/adafruits-raspberry-pi-lesson-4-gpio-setup/configuring-i2c
</br>
Get the Service File Running on Boot: </br>
https://www.raspberrypi-spy.co.uk/2015/10/how-to-autorun-a-python-script-on-boot-using-systemd/
</br>

After setting up the service file your Raspberry Pi should automatically start blindscontrol on boot.

### Alexa Installation
(TBD)

## Running
```bash
python3 blindscontrol_controller_interface.py
```

## Different Alexa Commands Supported:
Alexa open BlindsControl </br>
Open blinds </br>
Close blinds </br>

## 3D Model
![3DModel](https://github.com/NickEngmann/BlindsControl/blob/master/model/3DModel.png)