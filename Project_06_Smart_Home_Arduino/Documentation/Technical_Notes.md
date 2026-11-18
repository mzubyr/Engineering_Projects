# Technical notes: smart-home firmware and hardware

These notes describe the Arduino sketch and the hardware it drives.

## Files

- `Firmware/corrected/smart_home.ino`: the sketch to build.
- `Firmware/as_printed/smart_home_as_printed.ino`: the same sketch exactly as printed in Section 5.4 of the dissertation (pages 63 to 67 of the PDF in `Thesis/`).
- `Results/`: figures taken from the dissertation, named after their figure numbers: Figure 4 (block diagram, page 38), Figure 5 (flowchart, page 39), Figure 20 (phone app, page 53), Figure 21 (Proteus circuit, page 55) and Figure 22 (prototype photo, page 56). Figure 22 is a low-resolution photo (377 x 226 pixels).
- The PDF in `Thesis/` is the copy supplied by the author.

## Hardware and wiring

| Module | Connection |
|---|---|
| Arduino Uno | ATmega328P controller, powered over USB or an external supply |
| HC-05 Bluetooth | Hardware serial: module TX to Arduino RX (pin 0), module RX to Arduino TX (pin 1); 3.3 V supply |
| 16x2 LCD | `LiquidCrystal lcd(8,7,3,4,5,6)`: RS = 8, EN = 7, data = 3, 4, 5, 6 |
| DHT11 | VCC to 5 V, GND to GND, DATA to A0 |
| Touch sensor (TTP223) | VCC to 5 V, GND to GND, output to A5 |
| SIM900 GSM | `SoftwareSerial mySerial(10, 11)` (RX = 10, TX = 11), so the module's TX goes to pin 10 and its RX to pin 11 |
| First lamp (relay module) | Pin 9 |
| Second lamp (relay module) | Pin 13 |
| Buzzer | Pin 2 |

Pins 0 and 1 are shared with the USB serial port. Disconnect the Bluetooth module while uploading a sketch.

## Firmware

**Libraries:** LiquidCrystal and SoftwareSerial (bundled with the Arduino IDE) and SimpleDHT.

**Serial links:** the hardware serial port (phone over Bluetooth) and the SIM900 port both run at 9600 baud.

**Commands** (one ASCII character from the phone's Bluetooth terminal app):

| Character | Action | LCD and phone message |
|---|---|---|
| `1` | First lamp on (pin 9 high) | FIRST BULB ON |
| `2` | First lamp off (pin 9 low) | FIRST BULB OFF |
| `3` | Second lamp on (pin 13 high) | SECOND BULB ON |
| `4` | Second lamp off (pin 13 low) | SECOND BULB OFF |
| `0` | Read the DHT11 and show temperature and humidity on the LCD for 5 s | Temp & Humidity |

Any other character is ignored. Each lamp command waits 500 ms, shows its message for 2 s, then clears the LCD.

**Intruder alarm:** each pass of `loop()` reads the touch sensor with `analogRead(A5)` and prints `INPUT VALUE:` and the reading on the serial port. If the reading is below `alarmval` (600), the sketch:

1. sends an SMS through the SIM900: `AT+CMGF=1` (text mode), `AT+CMGS="<number>"`, the text `INTRUDER DETECTED!!!`, then a terminator character, with 1 s between each step;
2. turns the buzzer on for 500 ms.

Otherwise it turns the buzzer off and waits 1 s. The phone number is redacted in the source as `+91......`. Use your own number and do not commit a real one.

## Firmware versions

The corrected sketch differs from the printed one by two edits only:

| Problem in the printed sketch | Fix |
|---|---|
| `SimpleDHT11 dht11(pinDHT11);` uses `pinDHT11` before it is declared | `int pinDHT11=A0;` moved above it |
| `pinMode(touchsensorpin,,INPUT);` has a doubled comma | One comma removed |

Pins, commands and behaviour are otherwise unchanged.

**What has been checked.** I compiled both sketches on a computer against stand-in versions of the Arduino libraries. The printed sketch fails with exactly the two errors above, and the corrected sketch compiles with no warnings. A simulated run confirmed the command handling and the alarm sequence described above.

**What has not been checked.** The sketch has not been built for a real Uno with the real libraries, and it has not been run on hardware as part of preparing this repository.

## Behaviour to know about

- While the alarm condition holds, a new SMS is sent on every pass, about every 4.5 s. Commands are not read while an SMS is being sent.
- When the alarm is not triggered, a pass takes about 1 s, so a command can take up to about a second to be picked up.
- The `INPUT VALUE:` prints use the same serial port as the Bluetooth module, so they probably also reach the phone app.
- `lcd.println` and the `\n` characters in the weather text send newline characters to the LCD, which may show as odd symbols.
- The return value of the DHT11 read is not checked, so a failed read leaves the temperature and humidity at 0.

## Points to check on hardware

1. **Touch-sensor direction.** The alarm fires when the reading is below 600. This works if the sensor reads low when touched. If the sensor reads high when touched (the usual default for a TTP223 module), the alarm fires while nobody is touching it. Open the Serial Monitor and compare the readings touched and untouched.
2. **SMS terminator.** The sketch ends the SMS with `(char)20`. The SIM900 normally expects Ctrl-Z, which is ASCII 26, to send a message. Send a test SMS with the SIM900 to confirm which value works.
3. **SimpleDHT version.** The sketch uses the library's older `read(pin, ...)` call together with a constructor that takes the pin. A newer version may print a deprecation warning.
4. **Phone number.** Replace the placeholder before testing the SMS.
