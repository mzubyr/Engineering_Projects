# Technical notes: smart home dissertation

Notes on how the repository material was transcribed from the dissertation, and on the differences found between its text and its printed code. Page numbers refer to the PDF in `Thesis/`.

## Source

- Dissertation: *Design and Implementation of Smart Home*, Mewar University, Chittorgarh, M.Tech Robotics and Embedded Systems, session 2020-2021, dated March 2021.
- The PDF is the copy supplied by the author. Its cover reads "Month - Year", and the recommendation and certificate pages (pages 3 and 4) are unsigned. Replace it with the signed final copy if one exists.
- The figures in `Results/` are the images embedded in the dissertation: Figure 4 (page 38), Figure 5 (page 39), Figure 20 (page 53), Figure 21 (page 55) and Figure 22 (page 56). Figure 22 is a low-resolution photo (377 x 226 pixels).

## Wiring tables in the dissertation

| Module | Dissertation table | Connection |
|---|---|---|
| HC-05 | Table 2 | VCC to 3.3 V, GND to ground, TX to RX, RX to TX |
| 16x2 LCD | Table 4 | LCD data pins 7, 8, 9, 10 to d3, d4, d5, d6; EN to d7; RS to d8 |
| DHT11 | Table 6 | VCC to 5 V, DATA to A1, GND to GND |
| Touch sensor | Table 8 | VCC to 5 V, GND to GND, DATA to A5 |
| SIM900 | Table 9 | TX to pin 11, RX to pin 10 |

The sketch also uses pin 9 and pin 13 for the two lamps (through relay modules) and pin 2 for the buzzer. The dissertation has no wiring table for these.

## Differences between the dissertation text and the printed sketch

1. **Command characters.** Table 11 gives `0` / `1` for the first lamp on / off, `2` / `3` for the second lamp, and `4` for the weather display. The sketch uses `1` / `2`, `3` / `4` and `0`. Every action is shifted by one.
2. **DHT11 pin.** Table 6 and Figure 12 show the data line on A1. The sketch sets `pinDHT11=A0`.
3. **SIM900 wiring.** Table 9 connects the SIM900 TX to pin 11 and RX to pin 10. The sketch declares `SoftwareSerial mySerial(10, 11); // RX, TX`, which makes pin 10 the Arduino's receive pin. With a straight TX-to-RX connection the module's TX would go to pin 10, not 11. Check against the built prototype.
4. **Invalid commands.** Section 4.2.2 and the flowchart (Figure 5) say an invalid command shows "Invalid signal" on the phone and the LCD. The printed sketch has no `default` case in its `switch`.
5. **Alarm condition.** The sketch reads the touch sensor with `analogRead` and raises the alarm when `inputval < alarmval` (600). Check that this matches the sensor module's real output when touched. The sketch also sends a new SMS on each loop pass while the condition holds.

## Compile errors in the printed sketch

| Problem | Fix applied in `Firmware/corrected/smart_home.ino` |
|---|---|
| `SimpleDHT11 dht11(pinDHT11);` uses `pinDHT11` before it is declared | The line `int pinDHT11=A0;` was moved above it |
| `pinMode(touchsensorpin,,INPUT);` has a doubled comma | One comma removed |

Nothing else was changed. The difference between the two files is exactly these two edits.

The corrected sketch has not been compiled or run on hardware by whoever prepared it. The version of the SimpleDHT library used originally is not recorded; the call `dht11.read(pinDHT11, &temp, &humidity, NULL)` follows that library's older interface and may produce a deprecation warning in newer versions.

## Other notes

- Sections 3.5 and 4.2 of the dissertation refer to "figure []" and "table []" with the numbers left blank. The block diagram is Figure 4, the flowchart Figure 5 and the command table Table 11.
- The abstract says the user can control and monitor up to four devices including sensors. The conclusion mentions two outlets for appliances. In this repository I describe it as two lamp outputs plus the sensors.
