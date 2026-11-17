// ----------------------------------------------------------------------------
// Smart home: Arduino Uno, HC-05 Bluetooth, SIM900 GSM, DHT11, touch sensor,
// 16x2 LCD, buzzer and relay-driven lamps.
//
// Corrected from the sketch printed in the M.Tech dissertation (Section 5.4).
// ONLY the two compile errors were fixed. Behaviour, pin numbers and the
// command characters are exactly as printed. NOT compiled or tested on hardware
// by whoever prepared this file; build it in the Arduino IDE before relying on it.
//
//   Fix 1: "int pinDHT11=A0;" moved above "SimpleDHT11 dht11(pinDHT11);",
//          because the pin variable was used before it was declared.
//   Fix 2: "pinMode(touchsensorpin,,INPUT);" had a doubled comma.
//
// Where the dissertation text differs from this sketch (command characters,
// DHT11 pin, SIM900 wiring, invalid-command reply), the author confirmed that
// the sketch is correct. See Documentation/Technical_Notes.md.
//
// Replace the placeholder phone number below with your own. Do not commit a
// real phone number to a public repository.
// ----------------------------------------------------------------------------
#include <LiquidCrystal.h>
#include <SoftwareSerial.h>
#include <SimpleDHT.h>
LiquidCrystal lcd(8,7,3,4,5,6);
SoftwareSerial mySerial(10, 11); // RX, TX
int pinDHT11=A0; //temperature and humidity
SimpleDHT11 dht11(pinDHT11);
int touchsensorpin=A5; //touch sensor 
int inputval=0;
int buzzer=2; //buzzer
int alarmval=600; // set value 
// SMS notification
void sendmessage() {
 mySerial.println("AT+CMGF=1");
 delay(1000);
 mySerial.println("AT+CMGS=\"+91......\"\r");
 delay(1000);
 mySerial.println("INTRUDER DETECTED!!!");
 delay(1000);
 mySerial.println((char)20);
 delay(1000); }
void setup() {
 // put your setup code here, to run once:
Serial.begin(9600);
mySerial.begin(9600);
delay(100);
pinMode(buzzer,OUTPUT);
pinMode(touchsensorpin,INPUT);
digitalWrite(buzzer,LOW);
pinMode(9,OUTPUT); //first bulb
pinMode(13,OUTPUT); //second bulb
while (!Serial)
 {
 
 }
lcd.begin(16,2);
lcd.setCursor(0,0);
}
void loop() {
 // put your main code here, to run repeatedly:
 //Automation of home applinaces
if(Serial.available())
{char key=Serial.read();
switch(key){
 case '1': //turn ON first bulb
 delay(500);
 lcd.clear();
 digitalWrite(9,HIGH);
 lcd.println("FIRST BULB ON");
 Serial.println("FIRST BULB ON");
 delay(2000);
 lcd.clear();
 break;
 
 case'2': //turn OFF first bulb
 delay(500);
 lcd.clear();
 digitalWrite(9,LOW);
 lcd.println("FIRST BULB OFF");
 Serial.println("FIRST BULB OFF");
 delay(2000);
 lcd.clear();
break;
case'3': //turn ON second bulb
delay(500);
lcd.clear();
digitalWrite(13,HIGH);
lcd.println("SECOND BULB ON");
Serial.println("SECOND BULB ON");
delay(2000);
lcd.clear();
break;
case'4': //turn OFF second bulb
delay(500);
lcd.clear();
digitalWrite(13,LOW);
lcd.println("SECOND BULB OFF");
Serial.println("SECOND BULB OFF");
delay(2000);
lcd.clear();
break;
 case'0': //Weather status display
lcd.clear();
byte temp=0;
byte humidity=0;
dht11.read(pinDHT11,&temp,&humidity, NULL);
lcd.print("Temp & Humidity :");
lcd.setCursor(0,1);
lcd.print((int)temp);
lcd.print("*C");
lcd.print(". and ");
lcd.print( (int)humidity);
lcd.print("%H.\n\n");
delay(5000);
lcd.clear();
 break;
 };}
//Security code and notification
inputval=analogRead(touchsensorpin);
Serial.print("INPUT VALUE:");
Serial.print(inputval);
Serial.print("\n");
if(inputval<alarmval)
{sendmessage(); //send message to mobile number
digitalWrite(buzzer,HIGH); //turn ON buzzer
delay(500);}
else
 {
 digitalWrite(buzzer,LOW); //turn OFF buzzer
 delay(1000);
 }
}
