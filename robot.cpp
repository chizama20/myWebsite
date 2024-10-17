#include <Servo.h>

// Create servo object to control a servo
Servo myservo;

// Define positions
int pos = 0;

// Define input and output pins
const int outputs[] = {2, 3, 4, 5, 6}; // Digital output pins
const int inputPins[] = {A0, A1, A2};  // Analog input pins

void setup() {
  // Attach the servo to pin 11
  myservo.attach(11);

  // Setup output pins as OUTPUT
  for (int i = 0; i < 5; i++) {
    pinMode(outputs[i], OUTPUT);
  }

  // Setup analog input pins as INPUT
  for (int i = 0; i < 3; i++) {
    pinMode(inputPins[i], INPUT);
  }

  // Begin serial communication
  Serial.begin(9600);

  // Turn output pin 6 HIGH initially
  digitalWrite(outputs[4], HIGH);
}

// Function to move servo back and forth between 60 and 120 degrees
void moveServo() {
  for (pos = 60; pos <= 120; pos += 1) {
    myservo.write(pos);
    delay(15);
  }
  for (pos = 120; pos >= 60; pos -= 1) {
    myservo.write(pos);
    delay(15);
  }
}

// Function to set all output pins LOW
void setAllLow() {
  for (int i = 0; i < 4; i++) {
    digitalWrite(outputs[i], LOW);
  }
  digitalWrite(outputs[4], LOW);
}

void loop() {
  // Read analog input values
  int a = analogRead(inputPins[0]);
  int b = analogRead(inputPins[1]);
  int c = analogRead(inputPins[2]);

  // Print sensor values to Serial Monitor
  Serial.print(a); Serial.print("    ");
  Serial.print(b); Serial.print("    ");
  Serial.print(c); Serial.println("    ");
  delay(50);

  // Conditions based on analog inputs
  if (a <= 250) {
    setAllLow();
    moveServo();  // Move servo for condition A
  } 
  else if (b <= 450) {
    setAllLow();
    moveServo();  // Move servo for condition B
  } 
  else if (c <= 250) {
    setAllLow();
    moveServo();  // Move servo for condition C
  } 
  else if (a >= 251 && a <= 700) {
    digitalWrite(outputs[4], HIGH);  // Keep output pin 6 HIGH
    digitalWrite(outputs[1], LOW);
    digitalWrite(outputs[2], HIGH);
    digitalWrite(outputs[3], HIGH);
    delay(500);
    digitalWrite(outputs[0], HIGH);
    digitalWrite(outputs[1], LOW);
    digitalWrite(outputs[2], HIGH);
    digitalWrite(outputs[3], LOW);
    delay(500);
  } 
  else if (b >= 251 && b <= 800) {
    digitalWrite(outputs[0], LOW);
    digitalWrite(outputs[1], HIGH);
    digitalWrite(outputs[2], HIGH);
    digitalWrite(outputs[3], LOW);
    digitalWrite(outputs[4], HIGH);
  } 
  else if (c >= 251 && c <= 800) {
    digitalWrite(outputs[0], HIGH);
    digitalWrite(outputs[1], LOW);
    digitalWrite(outputs[2], LOW);
    digitalWrite(outputs[3], HIGH);
    digitalWrite(outputs[4], HIGH);
    delay(500);
    digitalWrite(outputs[0], HIGH);
    digitalWrite(outputs[1], LOW);
    digitalWrite(outputs[2], HIGH);
    digitalWrite(outputs[3], LOW);
    delay(500);
  } 
  else {
    // Default case
    digitalWrite(outputs[4], HIGH);
    digitalWrite(outputs[0], HIGH);
    digitalWrite(outputs[1], LOW);
    digitalWrite(outputs[2], HIGH);
    digitalWrite(outputs[3], LOW);
  }
}
