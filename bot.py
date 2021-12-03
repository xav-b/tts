#! /usr/bin/env python

"""Experimental assistant."""

import time

import click
from halo import Halo
import schedule
import zerorpc
from rich.console import Console


console = Console()


class Bot:


    # TODO: have persona bot inhereting from this and having their own
    # personnality (speak italian, fast, female)
    persona = None  # default to english male
    rate = 30

    def __init__(self, port: int):
        self._speaker = zerorpc.Client()
        console.log(f"connecting to tcp://127.0.0.1:{port}")
        self._speaker.connect(f"tcp://127.0.0.1:{port}")

        # TODO: have a list of funny idle things, and pick them half-randomly
        # (like could be based on time of the day)
        self._spinner = Halo(text='😪💤 ...', spinner='dots', text_color='cyan')

    def say(self, text: str):
        self._speaker.speech(text, self.persona, self.rate)

    def idle(self):
        self._spinner.start()

    def ping(self):
        # all job should start by stopping the spinner
        self._spinner.stop()

        console.print(":: PONG", time.time())


@click.command()
@click.option("-p", "--port", default=4242)
def loop(port):
    jarvis = Bot(port)
    jarvis.say("Assistant operational sir, at your service.")

    schedule.every(10).seconds.do(jarvis.ping)

    while True:
        schedule.run_pending()

        jarvis.idle()
        time.sleep(1)


if __name__ == '__main__':
    console.log("bot is starting...")
    loop()
