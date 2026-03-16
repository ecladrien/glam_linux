/*
  GLAM ESP32 WROOM firmware

  Serial protocol:
  - host sends: PING\n  -> device replies: PONG
  - host sends: READ\n  -> device replies: one JSON line

  Adjust the pin mapping and calibration constants below to match the wiring and
  current sensors on the final installation.
*/

static const int PIN_NEUTRE = 32;
static const int PIN_PHASE1 = 33;
static const int PIN_PHASE2 = 34;
static const int PIN_PHASE3 = 35;

static const long SERIAL_BAUDRATE = 115200;
static const int ADC_MAX_VALUE = 4095;
static const float CURRENT_SCALE = 500.0f;
static const float VOLTAGE_REFERENCE = 3.3f;

float readCurrentFromPin(int pin) {
  long total = 0;
  const int sampleCount = 16;

  for (int index = 0; index < sampleCount; ++index) {
    total += analogRead(pin);
    delay(2);
  }

  const float averageRaw = static_cast<float>(total) / static_cast<float>(sampleCount);
  const float voltage = (averageRaw / static_cast<float>(ADC_MAX_VALUE)) * VOLTAGE_REFERENCE;
  const float current = (voltage / VOLTAGE_REFERENCE) * CURRENT_SCALE;
  return current;
}

void sendMeasurementSnapshot() {
  const float neutre = readCurrentFromPin(PIN_NEUTRE);
  const float phase1 = readCurrentFromPin(PIN_PHASE1);
  const float phase2 = readCurrentFromPin(PIN_PHASE2);
  const float phase3 = readCurrentFromPin(PIN_PHASE3);

  Serial.print("{\"status\":\"ok\",");
  Serial.print("\"device\":\"esp32-wroom\",");
  Serial.print("\"adc_max\":");
  Serial.print(ADC_MAX_VALUE);
  Serial.print(',');
  Serial.print("\"current_scale\":");
  Serial.print(CURRENT_SCALE, 2);
  Serial.print(',');
  Serial.print("\"neutre\":");
  Serial.print(neutre, 2);
  Serial.print(',');
  Serial.print("\"phase1\":");
  Serial.print(phase1, 2);
  Serial.print(',');
  Serial.print("\"phase2\":");
  Serial.print(phase2, 2);
  Serial.print(',');
  Serial.print("\"phase3\":");
  Serial.print(phase3, 2);
  Serial.println('}');
}

void handleCommand(String command) {
  command.trim();
  command.toUpperCase();

  if (command == "PING") {
    Serial.println("PONG");
    return;
  }

  if (command == "READ") {
    sendMeasurementSnapshot();
    return;
  }

  if (command == "IDENTIFY") {
    Serial.println("GLAM_ESP32_WROOM");
    return;
  }

  Serial.println("{\"status\":\"error\",\"message\":\"unknown_command\"}");
}

void setup() {
  Serial.begin(SERIAL_BAUDRATE);
  analogReadResolution(12);
  analogSetAttenuation(ADC_11db);

  pinMode(PIN_NEUTRE, INPUT);
  pinMode(PIN_PHASE1, INPUT);
  pinMode(PIN_PHASE2, INPUT);
  pinMode(PIN_PHASE3, INPUT);

  delay(250);
}

void loop() {
  if (Serial.available() <= 0) {
    delay(10);
    return;
  }

  String command = Serial.readStringUntil('\n');
  handleCommand(command);
}