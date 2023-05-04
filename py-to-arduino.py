import serial

# open a serial connection to arduino by specifying the port and baud rate
BAUD_RATE = 9600
TIMEOUT = 1.0 # 1 second
PORT = '/dev/tty.usbmodem11201' # depends on the unit running rsudp; can be "COM3" when on windows; entirely machine-dependent

print('Opening a serial connection on PORT %s with BAUD RATE %d and TIMEOUT in %d second(s)' % (PORT, BAUD_RATE, TIMEOUT))
ser = serial.Serial(PORT, BAUD_RATE)

data = "H"  # Example data to send
ser.write(str(data).encode())  # Send the data as bytes
ser.close()


# The following is C++ code that I will input back into Aduino IDE -- keeping this here for reference
# const int ledPin = 12; // Pin number connected to the LED
# const int relayPin = 13; // Pin number connected to the relay module
# const int baudRate = 9600;

# void setup() {
#   Serial.begin(baudRate);  // Set the baud rate to match the Python program
#   Serial.print("start set up");

#   pinMode(ledPin, OUTPUT); // Set the LED pin as output
#   pinMode(relayPin, OUTPUT); // Set the Relay pin as output

#   digitalWrite(ledPin, HIGH); // always turn on the ledPin
# }

# void loop() {
#   digitalWrite(relayPin, HIGH);

#   if (Serial.available()) {
#     String receivedData = Serial.readString();  // Read the data from the serial port
#     // Serial.print("Data received: ");  // Print a label or message
#     // Serial.println(receivedData);     // Print the sensor value

#     if (receivedData == "H") {
#       digitalWrite(relayPin, LOW);
#       delay(10000);
#     } else if (receivedData = "L") {
#       digitalWrite(relayPin, HIGH);
#     }
#   }

#   // // NOTE: My relay is normally closed (connected): If we turn it on, the circuit gets disconnected
#   // digitalWrite(relayPin, HIGH); // Turn on the relay
#   // delay(5000); // Wait for 1 second
#   // digitalWrite(relayPin, LOW); // Turn off the LED
#   // delay(1000); // Wait for 1 second
# }
