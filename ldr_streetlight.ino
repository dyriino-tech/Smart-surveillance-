// Set pin numbers
// const won't change
const int ledPin = 13;
const int ldrPin = A0;

void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  pinMode(ledPin, OUTPUT);
  pinMode(ldrPin, INPUT);
}

void loop() {
  // put your main code here, to run repeatedly:
  int ldrStatus = analogRead(ldrPin);

  if (ldrStatus <= 300) {
    digitalWrite(ledPin, HIGH);
    Serial.println("LDR IS DARK, LED IS ON");
  }
  else {
    digitalWrite(ledPin, LOW);
    Serial.println("LDR IS BRIGHT, LED IS OFF");
  }
}
