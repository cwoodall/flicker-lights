/**
 *
 */
#include "Arduino.h"
#include "SPI.h"
#include "RF24.h"
#include "pb_decode.h"
#include "pb_encode.h"
#include "flicker_base_message.pb.h"
#include "flicker_base_response.pb.h"

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

  // Serial.println(F("SENDING"));

  if(!m_radio.write(&colors, sizeof(unsigned long))) {
    Serial.println(F("failed"));
  }

  m_radio.startListening();

}

char buf[64] = {};
int buf_i = 0;

void setup() {
  Serial.begin(SERIAL_BAUDRATE);

  radioSetup();
  // put your setup code here, to run once:

}

#define MESSAGE_DELIMITER ((char)0x7D)
#define MESSAGE_ESCAPE ((char)0x7E)

void loop() {
  // put your main code here, to run repeatedly:
  serviceRadio();
  static bool escaped = false;
  static bool in_message = false;

  /**
   * 0x7D is message delimiter
   * 0x7E is escape
   */
  if (Serial.available()) {
    char c = Serial.read();
    if (!in_message) {
      switch (c) {
        case MESSAGE_DELIMITER:
          in_message = true;
          escaped = false;
          break;
        case MESSAGE_ESCAPE:
        default:
          break;
      }
    } else {
      switch (c) {
        case MESSAGE_DELIMITER:
        if (!escaped) {
          //process end of message
          FlickerBaseMessage cmd = FlickerBaseMessage_init_zero;
          pb_istream_t stream = pb_istream_from_buffer((const pb_byte_t *)buf, buf_i);
          bool status = pb_decode(&stream, FlickerBaseMessage_fields, &cmd);
          if (!status) {
            Serial.print(PB_GET_ERROR(&stream));
          }

          Serial.println(cmd.groupid);
          Serial.println(cmd.which_payload);
          if (cmd.which_payload == FlickerBaseMessage_setColor_tag) {
            Serial.println(cmd.payload.setColor.dest_color);
            colors = cmd.payload.setColor.dest_color;
          }
          in_message = false;
          escaped = false;
          buf_i = 0;
          break;
        }
        case MESSAGE_ESCAPE:
          if (!escaped) {
            escaped = true;
            break;
          } else {
            escaped = false;
          }
        default:
          buf[buf_i++] = c;
          break;
      }
    }
  }
}
