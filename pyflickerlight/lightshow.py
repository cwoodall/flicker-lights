import pyglet
import csv
import time
import serial
import threading
import yaml

s = serial.Serial("/dev/ttyACM0")

pyglet.options['audio'] = ('openal', 'pulse', 'silent')

show_config = None
with open("show.yaml", 'rb') as show_file:
    show_config = yaml.load(show_file.read())

print("Playing show {0} starting at time {1} with {2}x speed".format(
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
        # print player.time
        # print float(step['time'])+start_time
        time.sleep(.01)

    for command in commands:
        print "c {0:06x}|".format(command['color'])
        s.write('c {0:06x}\n'.format(command['color']))
#
# t.run()
# time.sleep(100)
player.pause()
s.close()
