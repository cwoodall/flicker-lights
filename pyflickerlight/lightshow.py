import pyglet
import csv
import time
import serial
import threading
import yaml
import logging
from argparse import ArgumentParser
import click

import flickerlights.proto as pb_message

from six import iterbytes

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
def EncodeMessage(msg):
    final_msg = b"\x7D"
    for b in msg:
        if b in [0x7D, 0x7E]:
            logger.critical(b)
            final_msg += b'\x7E'
        final_msg += bytes(b)
    final_msg += b'\x7D'
    logger.critical(final_msg)
    return final_msg

if __name__ == "__main__":
    # Configure pyglet to use openAL if available
    pyglet.options['audio'] = ('openal', 'pulse', 'silent')

    # CLI arguments
    parser = ArgumentParser(
        description="Playback a flicker-light show.yaml file.")
    parser.add_argument("--port", "-p", type=str,
                        help="Serial port to use [default = /dev/ttyACM0]",
                        default = "/dev/ttyACM0")
    parser.add_argument("show", type=str,
                        help="Lightshow.yaml file to playback.")

    args = parser.parse_args()

    s = serial.Serial(args.port)

    show_config = None
    with open(args.show, 'rb') as show_file:
        show_config = yaml.load(show_file.read())

    logger.debug("Playing show {0} starting at time {1} with {2}x speed".format(
        show_config['title'], show_config['start_time'], show_config['speed']))

    show = show_config["show"]
    song = pyglet.media.load(show_config["location"])
    player = pyglet.media.Player()
    player.queue(song)
    player.pitch = float(show_config['speed'])
    start_time = float(show_config["start_time"]) + .00001 # for some reason pyglet Players fail if you set start_time to 0
    player.seek(start_time)
    player.play()


    for i, step  in enumerate(show):
        commands = step['commands']
        while player.time < (float(step['time'])+start_time):
            # if (s.inWaiting()):
            #     print(s.read(s.inWaiting()))
            time.sleep(.01)

        for command in commands:
            msg = pb_message.FlickerBaseMessage()
            msg.groupid = 0
            msg.timestamp = 0
            msg.setColor.dest_color = int(command['color'])
            msg_serialized = msg.SerializeToString()
            s.write(EncodeMessage(msg_serialized))

    player.pause()
    s.close()
