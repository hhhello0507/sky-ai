int RXLED = 17;
char cmd;

void setup() {

  pinMode(RXLED, OUTPUT);
  Serial.begin(9600);
  Serial.println("Initialize Serial Monitor");

  Serial1.begin(9600);
  Serial1.println("Initialize Serial Hardware UART Pins");

  pinMode(16, OUTPUT);
  pinMode(14, OUTPUT);
}

void loop() {
  input();
}

void input() {
  if (Serial.available()) {
    cmd = Serial.read(); 
  }

  if (cmd == '1') {
    digitalWrite(16, HIGH);
    digitalWrite(14, LOW);
  } else if(cmd == '0') {
    digitalWrite(16, LOW);
    digitalWrite(14, HIGH);
  }
}