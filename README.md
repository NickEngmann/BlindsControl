# Blinds Control
Control the blinds in your room using Raspberry and Stepper Motors!</br>
Click the image below to watch the video. </br>
[![Watch the video](https://github.com/NickEngmann/BlindsControl/blob/master/img/youtube.png)](https://youtu.be/fzvNv4QeY4A)

## Necessary Hardware:
<a href="https://www.adafruit.com/product/3055" target="__blank">Raspberry Pi 3 </a></br>
<a href="https://www.amazon.com/gp/product/B00TIY5JM8/ref=oh_aui_detailpage_o08_s00?ie=UTF8&psc=1" target="__blank">Adafruit Motor Hat for Raspberry Pi</a></br>
<a href="https://www.amazon.com/gp/product/B011EBSKK0/ref=oh_aui_detailpage_o01_s00?ie=UTF8&psc=1" target="__blank">DC 5-12V Buck Boost Converter</a></br>
<a href="https://github.com/NickEngmann/BlindsControl/tree/master/model" target="__blank">2x Motor Housing </a></br>
<a href="https://github.com/NickEngmann/BlindsControl/tree/master/model" target="__blank">2x Rod Controller </a></br>
2x <a href="https://www.amazon.com/Stepper-Bipolar-4-lead-Connector-Printer/dp/B00PNEQKC0/ref=sr_1_4?ie=UTF8&qid=1514777861&sr=8-4&keywords=nema+17" target="__blank">Nema 17 Stepper Motor</a>

## Instructions:
If you want to emulate this project the instructions are fairly simple. Attach the 3D printed portions to your motor, and wire the Motor appropriately to the Adafruit Motor Hat. Attach the Rod Controller to your blinds, and screw the Motor Container to the window frame.  

![Hardware](https://github.com/NickEngmann/BlindsControl/blob/master/img/1.jpg)
</br>
Power the Raspberry Pi with any 5V supply and power the Motor Hat either using a 12V supply or a 5V supply and the 5-12V Buck Boost Converter. Now you are ready to install the necessary software

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
Now you are ready to clone the repo on the raspberry pi </br>
```bash
cd ~
git clone https://github.com/NickEngmann/BlindsControl
```

Then follow the following instructions to take the blindscontrol.service file and enable it with systemd </br>
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
"Alexa open BlindsControl" </br>
"Open blinds" </br>
"Close blinds" </br>

## 3D Model
![3DModel](https://github.com/NickEngmann/BlindsControl/blob/master/model/3DModel.png)