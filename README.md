# Blinds Control

Control the blinds in your room using Raspberry Pi and Stepper Motors!</br>
Click the image below to watch the video. </br>
[![Watch the video](https://github.com/NickEngmann/BlindsCont

## Installation

### Prerequisites
- Raspberry Pi (tested on Raspberry Pi 3/4)
- Python 3.8+
- Stepper motor and driver compatible with Raspberry Pi GPIO
- Firebase project for Alexa integration

### Setup

1. Clone the repository:
```bash
git clone https://github.com/NickEngmann/BlindsControl.git
cd BlindsControl
```

2. Install dependencies:
```bash
pip install --no-cache-dir pytest fake-rpi Pillow
pip install pytest
```

3. Configure GPIO pins in `blindscontrol_controller_interface.py` according to your hardware setup

4. Set up Firebase credentials and Alexa skill as described in the project structure section

## Usage

### Running the Controller

1. Ensure your Raspberry Pi is properly connected to the stepper motor driver
2. Run the main controller:
```bash
python blindscontrol_controller_interface.py
```

3. The controller will:
   - Initialize the state machine
   - Connect to Firebase for real-time updates
   - Poll for state changes every 3 seconds
   - Update the blind position based on events

### State Machine

The system uses a state machine to manage blind operations:
- `OPEN`: Blinds fully open
- `CLOSED`: Blinds fully closed
- `OPENING`: Blinds moving up
- `CLOSING`: Blinds moving down
- `STOPPED`: Blinds stationary

### Alexa Integration

1. Set up an Alexa skill with Firebase Smart Home skill
2. Link your Firebase project in the Alexa developer console
3. Use voice commands like:
   - "Alexa, open the blinds"
   - "Alexa, close the blinds"
   - "Alexa, set blinds to 50%"

## Testing

Run the test suite using pytest:

```bash
python -m pytest tests/ -v
```

### Hardware Mocking

The project uses `fake-rpi` to mock Raspberry Pi GPIO operations for testing:

```bash
pip install fake-rpi
```

## Project Structure

```
BlindsControl/
├── blindscontrol_controller_interface.py  # Main controller script
├── blindscontrol_state_machine.py         # State machine implementation
├── blindscontrol_alexa_interface.py       # Firebase/Alexa integration
├── blindscontrol_command_interface.py     # Command processing
├── tests/                                 # Test files
├── requirements.txt                       # Python dependencies
└── README.md                              # This file
```

## Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

Distributed under the MIT License. See `LICENSE` for more information.

## Acknowledgements

- [Raspberry Pi Documentation](https://www.raspberrypi.org/documentation/)
- [Alexa Skills Kit](https://developer.amazon.com/alexa)
- [Firebase](https://firebase.google.com/)rol/blob/master/img/youtube.png)](https://youtu.be/fzvNv4QeY4A)

Table of Contents
============
* [Instructions](#instructions)
* [Necessary Hardware](#necessary-hardware)
* [Hardware Build](#hardware-build)
* [Software Install](#software-install)
* [Alexa Integration](#alexa-integration)
* [Running](#running)
* [Model](#model)
* [License](#license)

Instructions
============
*** NOTE: The instructions below are written for getting just one stepper motor up and running, however the code and the hardware can easily support 2 stepper motors. So if you want to control two blinds with one Raspberry Pi just 3D print another model set and wire it up *** </br>



Necessary Hardware
============
<a href="https://www.adafruit.com/product/3055" target="__blank">Raspberry Pi 3 </a></br>
<a href="https://www.amazon.com/gp/product/B00TIY5JM8/ref=oh_aui_detailpage_o08_s00?ie=UTF8&psc=1" target="__blank">Adafruit Motor Hat for Raspberry Pi</a></br>
<a href="https://www.amazon.com/gp/product/B011EBSKK0/ref=oh_aui_detailpage_o01_s00?ie=UTF8&psc=1" target="__blank">DC 5-12V Buck Boost Converter</a></br>
<a href="https://github.com/NickEngmann/BlindsControl/tree/master/model" target="__blank">Motor Container </a></br>
<a href="https://github.com/NickEngmann/BlindsControl/tree/master/model" target="__blank">Rod Controller </a></br>
2x <a href="https://www.amazon.com/Stepper-Bipolar-4-lead-Connector-Printer/dp/B00PNEQKC0/ref=sr_1_4?ie=UTF8&qid=1514777861&sr=8-4&keywords=nema+17" target="__blank">Nema 17 Stepper Motor</a>

Hardware build
============
![Hardware](https://github.com/NickEngmann/BlindsControl/blob/master/img/1.jpg)
</br>
If you want to emulate this project the instructions are fairly simple. Attach the 3D printed portions to your motor, and wire the Motor appropriately to the Adafruit Motor Hat. Attach the Rod Controller to your blinds, and screw the Motor Container to the window frame.  </br>
Power the Raspberry Pi with any 5V supply and power the Motor Hat either using a 12V supply or a 5V supply and the 5-12V Buck Boost Converter. Now you are ready to install the necessary software

Software install
============

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

Alexa Integration
============
Go to the alexa directory and install node dependencies.
```bash
cd alexa-blindcontrol
npm install
```

Go to firebase and set up a firebase application. Get config data from firebase and save it as config.json </br>

```bash 
config = {
    apiKey: "{api-key}",
    authDomain: "{app-id}.firebaseapp.com",
    databaseURL: "https://{app-id}.firebaseio.com",
    projectId: "{app-id}",
    storageBucket: "{app-id}.appspot.com",
    messagingSenderId: ""
  }
```
Save all items in the folder as a .zip file.

Follow the following instructions from Amazon to set up your own Lambda service and nodejs skill:</br>
https://developer.amazon.com/alexa-skills-kit/alexa-skill-quick-start-tutorial </br>
Load the .zip file into your lambda service </br>

Add the following command configurations to your Alexa skill in the Alexa skill developer portal </br>
## Different Alexa Commands Supported:
"Alexa open BlindsControl" </br>
"Open blinds" </br>
"Close blinds" </br>

Running
============
```bash
python3 blindscontrol_controller_interface.py
```


Model
============
![3DModel](https://github.com/NickEngmann/BlindsControl/blob/master/model/3DModel.png)


License
============
The MIT License

Copyright (c) 2004-2018 Quod Certamine

Permission is hereby granted, free of charge, to any person obtaining
a copy of this software and associated documentation files (the
"Software"), to deal in the Software without restriction, including
without limitation the rights to use, copy, modify, merge, publish,
distribute, sublicense, and/or sell copies of the Software, and to
permit persons to whom the Software is furnished to do so, subject to
the following conditions:

The above copyright notice and this permission notice shall be
included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE
LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION
WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
