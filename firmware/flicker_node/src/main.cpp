/**

*/

#include <SPI.h>
#include "RF24.h"

/* ==== User Config ==== */
const int SERIAL_BAUDRATE = 9600;
const int RADIO_POWER_LEVEL = RF24_PA_LOW;

static RF24 m_radio(9, 10);
static byte pipes[][9] = {"DNCMASTR", "DNCNODE0"};

static unsigned long colors = 0;

void radioSetup() {
  m_radio.begin();
  m_radio.setPALevel(RADIO_POWER_LEVEL);
  m_radio.setDataRate( RF24_250KBPS );

  m_radio.openWritingPipe(pipes[0]);
  m_radio.openReadingPipe(1, pipes[1]);

  //  radio.enableDynamicPayloads() ;
  m_radio.enableDynamicAck();
  m_radio.startListening();
}


void serviceRadio() {
  if (m_radio.available()) {
    m_radio.read(&colors, sizeof(unsigned long) );
  }
}

  void setup() {
  Serial.begin(SERIAL_BAUDRATE);
  Serial.println(F("DANCE NODE 001"));

  pinMode(3, OUTPUT);
  pinMode(5, OUTPUT);
  pinMode(6, OUTPUT);

  radioSetup();
}

void loop() {
  serviceRadio();

  analogWrite(3, (colors)& 0xff); // nada
  analogWrite(5, (colors >>16) & 0xff); // red
  analogWrite(6, (colors>>8) & 0xff); // green

}
