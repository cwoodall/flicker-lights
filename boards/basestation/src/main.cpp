/**
 *
 */
#include "Arduino.h"
#include "SPI.h"
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
  m_radio.openWritingPipe(pipes[1]);
  m_radio.openReadingPipe(1, pipes[0]);
  m_radio.enableDynamicAck();

  m_radio.startListening();
}


void serviceRadio() {
  m_radio.stopListening();

//  Serial.println(F("SENDING"));

  if(!m_radio.write(&colors, sizeof(unsigned long))) {
    Serial.println(F("failed"));
  }
  m_radio.startListening();

}

char buf[256] = {};
int buf_i = 0;

void setup() {
  Serial.begin(SERIAL_BAUDRATE);
  Serial.println(F("DANCE MASTER 001"));
  Serial.println(F("Yars1"));

  radioSetup();
  // put your setup code here, to run once:

}

void loop() {
  // put your main code here, to run repeatedly:
  serviceRadio();

  if ( Serial.available() )
  {
    if (buf_i < 256) {
      char c = Serial.read();
      if (c == '\n') {
        if (buf_i >= 2) {
          char code = buf[0];
          if (code == 'c' && buf[1] == ' ') {
            if (buf_i == 8) {
              colors = strtoul(&buf[2],NULL,16);
              Serial.println(colors);
            }
          }
        }
        buf_i = 0;
      } else {
        buf[buf_i++] = c;
      }
    } else {
      buf_i = 0;
    }
  }
}
