# Technical notes: smart home dissertation

Notes on how the repository material was transcribed from the dissertation, and on the differences found between its text and its printed code. Page numbers refer to the PDF in `Thesis/`.

## Source

- Dissertation: *Design and Implementation of Smart Home*, Mewar University, Chittorgarh, M.Tech Robotics and Embedded Systems, session 2020-2021, dated March 2021.
- The PDF is the copy supplied by the author. Its cover reads "Month - Year", and the recommendation and certificate pages (pages 3 and 4) are unsigned. Replace it with the signed final copy if one exists.
- The figures in `Results/` are the images embedded in the dissertation: Figure 4 (page 38), Figure 5 (page 39), Figure 20 (page 53), Figure 21 (page 55) and Figure 22 (page 56). Figure 22 is a low-resolution photo (377 x 226 pixels).

## Wiring as built

The sketch is the reference (confirmed by the author). Where the dissertation's wiring tables differ, the tables are wrong.

| Module | Connection |
|---|---|
| HC-05 | VCC to 3.3 V, GND to ground, module TX to Arduino RX (pin 0), module RX to Arduino TX (pin 1) (Table 2) |
| 16x2 LCD | `LiquidCrystal lcd(8,7,3,4,5,6)`: RS = 8, EN = 7, data = 3, 4, 5, 6 (matches Table 4) |
| DHT11 | VCC to 5 V, DATA to **A0**, GND to GND (Table 6 says A1, which is wrong) |
| Touch sensor | VCC to 5 V, GND to GND, output to A5 (Table 8) |
| SIM900 | Arduino receives on pin 10 and transmits on pin 11 (`SoftwareSerial mySerial(10, 11); // RX, TX`). The module's TX therefore goes to pin 10 and its RX to pin 11. Table 9 lists them the other way round. |
| First lamp (relay) | Pin 9 |
| Second lamp (relay) | Pin 13 |
| Buzzer | Pin 2 |

The dissertation has no wiring table for the lamps and the buzzer.

## Differences between the dissertation text and the printed sketch

The author confirmed on 17 November 2026 that the sketch is correct. Each difference is resolved in favour of the sketch. These are corrections from the author's own check; the touch-sensor output and the wiring were not re-measured when this repository was prepared.

| Item | Dissertation | Sketch (reference) |
|---|---|---|
| Command characters | Table 11: `0` / `1` first lamp on / off, `2` / `3` second lamp on / off, `4` weather | `1` / `2` first lamp on / off, `3` / `4` second lamp on / off, `0` weather |
| DHT11 pin | A1 (Table 6, Figure 12) | A0 |
| SIM900 pins | Table 9: SIM900 TX to 11, RX to 10 | `SoftwareSerial(10, 11)`, RX = 10, TX = 11 |
| Invalid command | Section 4.2.2 and Figure 5: "Invalid signal" shown on the phone and the LCD | No `default` case, so no such reply |
| Alarm condition | Not specified | `analogRead` of the touch sensor, alarm when `inputval < 600` |

One behaviour to be aware of: the sketch sends a new SMS on every loop pass while the alarm condition holds.

## Compile errors in the printed sketch

| Problem | Fix applied in `Firmware/corrected/smart_home.ino` |
|---|---|
| `SimpleDHT11 dht11(pinDHT11);` uses `pinDHT11` before it is declared | The line `int pinDHT11=A0;` was moved above it |
| `pinMode(touchsensorpin,,INPUT);` has a doubled comma | One comma removed |

Nothing else was changed. The difference between the two files is exactly these two edits.

The corrected sketch has not been compiled by whoever prepared it, and was not run on hardware as part of preparing this repository. The version of the SimpleDHT library used originally is not recorded; the call `dht11.read(pinDHT11, &temp, &humidity, NULL)` follows that library's older interface and may produce a deprecation warning in newer versions.

## Other notes

- Sections 3.5 and 4.2 of the dissertation refer to "figure []" and "table []" with the numbers left blank. The block diagram is Figure 4, the flowchart Figure 5 and the command table Table 11.
- The abstract says the user can control and monitor up to four devices including sensors. The conclusion mentions two outlets for appliances. In this repository I describe it as two lamp outputs plus the sensors.
