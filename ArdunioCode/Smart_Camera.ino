// === Smart Alarm (Stable + Robust Serial Parser) ============================
// Button short press: DISARMED <-> ARMED  (alarm only via serial)
// Serial commands (newline-terminated, case-insensitive, spaces ignored):
//   <ARM:1> / <ARM:0>
//   <ALARM:ON> / <ALARM:OFF>   (ignored if DISARMED)
//   <STATUS>
//
// Replies to every valid command:
//   ACK
//   <STATE:DISARMED|ARMED|ALARM>
//
// ---------------------------------------------------------------------------

#define BUZZER_PASSIVE true  // true: passive (tone), false: active (HIGH/LOW)

const int LED  = 7;
const int BUZZ = 8;
const int BTN  = 2;   // button to GND, using INPUT_PULLUP

// --- timings & filters ---
const unsigned long BLINK_MS       = 150;
const int           QUIET_TONE_HZ  = 800;
const unsigned long BOOT_IGNORE_MS = 1200;
const int SAMPLE_INTERVAL_MS       = 1;
const int LOW_CONSEC_REQ           = 30;   // ~30 ms LOW
const int HIGH_CONSEC_REQ          = 30;   // ~30 ms HIGH
const unsigned long PREHIGH_MS     = 200;  // need stable HIGH before we accept a press

// --- state machine ---
enum State { DISARMED, ARMED, ALARM };
State state = DISARMED;

unsigned long blinkMs = 0;
bool blinkOn = false;
unsigned long bootMs = 0;

// --- button sampling filter ---
int consecLow = 0, consecHigh = 0;
bool filtPressed = false;
unsigned long lastSampleMs = 0;
unsigned long lastStableHighStart = 0;
static bool inPress = false;
static unsigned long pressStart = 0;

// --- serial buffer ---
String rx;

// ----------------- helpers -----------------
void buzzerOn(){
#if BUZZER_PASSIVE
  tone(BUZZ, QUIET_TONE_HZ);
#else
  digitalWrite(BUZZ, HIGH);
#endif
}
void buzzerOff(){
#if BUZZER_PASSIVE
  noTone(BUZZ);
#else
  digitalWrite(BUZZ, LOW);
#endif
}

void emitState() {
  if (state == DISARMED) Serial.println("<STATE:DISARMED>");
  else if (state == ARMED) Serial.println("<STATE:ARMED>");
  else Serial.println("<STATE:ALARM>");
}

void applyIndicators(){
  if (state == DISARMED) {
    digitalWrite(LED, LOW);
    buzzerOff();
  } else if (state == ARMED) {
    digitalWrite(LED, HIGH);
    buzzerOff();
  } else { // ALARM
    if (millis() - blinkMs >= BLINK_MS) { blinkMs = millis(); blinkOn = !blinkOn; }
    digitalWrite(LED, blinkOn ? HIGH : LOW);
    buzzerOn();
  }
}

void setState(State s){
  state = s;
  blinkMs = millis(); blinkOn = false;
  if (state != ALARM) buzzerOff();
  applyIndicators();
}

void ackAndState() {
  Serial.println("ACK");
  emitState();
}

// ----------------- serial parsing (tolerant) -----------------
String normalize(String s) {
  // Remove spaces/tabs and uppercase
  String out;
  out.reserve(s.length());
  for (unsigned i=0;i<s.length();++i){
    char c = s[i];
    if (c == ' ' || c == '\t' || c == '\r') continue;
    out += (char)toupper(c);
  }
  return out;
}

void handleLine(String line){
  line.trim();
  if (line.length() == 0) return;

  // tolerant normalize
  line = normalize(line);

  // Must be bracketed
  if (!line.startsWith("<") || !line.endsWith(">")) {
    Serial.println("ERR");
    emitState();
    return;
  }

  // Strip < >
  String body = line.substring(1, line.length()-1);

  // STATUS (no colon) or KEY:VAL
  int colon = body.indexOf(':');
  String key = body;
  String val = "";
  if (colon >= 0) {
    key = body.substring(0, colon);
    val = body.substring(colon+1);
  }

  if (key == "STATUS") {
    ackAndState();
    return;
  }

  if (key == "ARM") {
    bool on = (val == "1" || val == "ON" || val == "TRUE");
    setState(on ? ARMED : DISARMED);
    ackAndState();
    return;
  }

  if (key == "ALARM") {
    // Only valid when ARMED/ALARM
    if (state == DISARMED) {
      // ignore but still ACK + state
      ackAndState();
      return;
    }
    bool on = (val == "1" || val == "ON" || val == "TRUE");
    setState(on ? ALARM : ARMED);
    ackAndState();
    return;
  }

  // Unknown command
  Serial.println("ERR");
  emitState();
}

// ----------------- button handling (stable, short press only) -----------------
void sampleButton(){
  if (millis() - lastSampleMs < SAMPLE_INTERVAL_MS) return;
  lastSampleMs = millis();

  int raw = digitalRead(BTN); // INPUT_PULLUP: HIGH idle, LOW pressed
  if (raw == LOW) { consecLow++; consecHigh = 0; }
  else            { consecHigh++; consecLow  = 0; }

  bool prev = filtPressed;
  if (!filtPressed && consecLow  >= LOW_CONSEC_REQ)  filtPressed = true;
  if ( filtPressed && consecHigh >= HIGH_CONSEC_REQ) filtPressed = false;

  // Track when we last had a stable HIGH
  if (!filtPressed && (prev != filtPressed)) {
    lastStableHighStart = millis();
  }
}

void handleButton(){
  if (millis() - bootMs < BOOT_IGNORE_MS) return;

  sampleButton();

  // start of press
  if (!inPress && filtPressed){
    if (millis() - lastStableHighStart >= PREHIGH_MS){
      inPress = true;
      pressStart = millis();
    }
  }

  // release
  if (inPress && !filtPressed){
    inPress = false;
    unsigned long held = millis() - pressStart;
    if (held >= 40) {
      // Toggle DISARMED <-> ARMED only
      setState(state == DISARMED ? ARMED : DISARMED);
      // (Optional) echo state change for host visibility:
      emitState();
    }
  }
}

// ----------------- setup/loop -----------------
void setup(){
  pinMode(LED, OUTPUT);
  pinMode(BUZZ, OUTPUT);
  pinMode(BTN, INPUT_PULLUP);   // keep internal pull-up
#if !BUZZER_PASSIVE
  digitalWrite(BUZZ, LOW);
#endif
  Serial.begin(115200);

  bootMs = millis();
  lastStableHighStart = bootMs;
  setState(DISARMED);
}

void loop(){
  // Serial receive (line-oriented)
  while (Serial.available()){
    char ch = Serial.read();
    if (ch == '\n') {
      handleLine(rx);
      rx = "";
    } else if (ch != '\r') {
      rx += ch;
      if (rx.length() > 120) rx = ""; // safety
    }
  }

  handleButton();
  applyIndicators();
}
