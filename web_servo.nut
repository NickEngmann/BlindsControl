
require(["GPIO","PWM","Capture", "string","ADC"]);
dofile("sd:/LIB/motors/SERVO/SERVO.NUT");
dofile("sd:/lib/sensors/dht11/dht11.nut");
led <- GPIO(LED_BUILTIN);       // LED built into board 
led.output();                   // sets the digital pin as output
// Create our sensor objects
sensor <- DHT11(/*Pin*/ 6, /*PWM*/ 1, /*Channel*/ 0, /*Divider*/ 256)
adc <- ADC(0);

// Use 16-bit resolution
adc.resolution(16);

// /* Control a servo on PWM0 channel 0 (GPIO pin 2 on Esquilo) */
 pwm <- PWM(0)
 servo1 <- Servo(pwm, 0);
 servo1.setPulses(0.70,2.58); //pulse width as measured for my particular servos
 servo1.setRange(0.0,180.0); //degrees
 servo1.setFrequency(50); //frequency

 // /* Control a servo on PWM0 channel 1 (GPIO pin 3 on Esquilo) */
 servo2 <- Servo(pwm, 1);
 servo2.setPulses(0.70,2.58); //pulse width
 servo2.setRange(0.0,180.0); //degrees
 servo2.setFrequency(50); //frequency

function sweep() {
    for (local i = 0.0; i < 180.0; i++) {
        servo1.position(i);
        delay(1);
    }
    servo1.position(0.0);
    for (local i = 0.0; i < 180.0; i++) {
        servo2.position(i);
        delay(1);
    }
    servo2.position(0.0);
    led.low();                    // sets the LED off
}

function set_position1 (_angle) {
    servo1.position(_angle);
    delay(1);
    //led.low();                    // sets the LED off
}

function set_position2 (_angle) {
    servo2.position(_angle);
    delay(1);
    //led.low();                    // sets the LED off
}
function getWeather()
{
    local photoResistor = 0;
    local photoResistorReading = 0;
    photoResistorReading = adc.read(photoResistor);
    //print(photoResistorReading);
    //print("\n");
    local values = []
    try{
    	values = sensor.read();
        //values.push(0)
        //values.push(1)
    }catch(exception){
        values.push(0)
        values.push(1)
    }
    return {
        temp = values[1],
        humidity = values[0],
        //temp = 99,
        //humidity = 99,
        light = photoResistorReading,
    };
}

print("Weather station ready!\n");
set_position1(0);
while (true) {
    led.high();                   // sets the LED on
    delay(500);
    led.low();                    // sets the LED off
    delay(500);
}