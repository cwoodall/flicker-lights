import pyglet
import time
import serial
import yaml
import logging
import click
import flickerlights.proto as pb

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

@click.command()
@click.option("--port", "-p", type=str, default = "/dev/ttyACM0",
              help="Serial port to use [default = /dev/ttyACM0]",)
@click.argument("show_file", type=click.File('rb'))
def cli(port, show_file):
    # Configure pyglet to use openAL if available
    pyglet.options['audio'] = ('openal', 'pulse', 'silent')

    s = serial.Serial(port)
    show_config = yaml.load(show_file.read())
    click.echo("Playing show {0} starting at time {1} with {2}x speed".format(
        show_config['title'], show_config['start_time'], show_config['speed']))

    show = show_config["show"]

    song = pyglet.media.load(show_config["location"])
    player = pyglet.media.Player()
    player.queue(song)
    player.pitch = float(show_config['speed'])
    # for some reason pyglet Players fail if you set start_time to 0
    start_time = float(show_config["start_time"]) + .00001
    player.seek(start_time)
    player.play()

    for i, step  in enumerate(show):
        commands = step['commands']
        while player.time < (float(step['time'])+start_time):
            time.sleep(.01)

        for command in commands:
            msg = pb.FlickerBaseMessage()
            msg.groupid = 0
            msg.timestamp = 0
            msg.setColor.dest_color = int(command['color'])
            print(msg)
            serial_msg = pb.FlickerSerialMsg(msg)
            s.write(serial_msg.serialize())

    player.pause()
    s.close()

if __name__ == "__main__":
    cli()
