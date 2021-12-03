#! /usr/bin/env python

"""TTS as a Service."""


import click
import pyttsx3
import zerorpc
from rich.console import Console


console = Console()


class TTSRPC(object):

    def __init__(self):
        console.log("initialising engine")
        self._engine = pyttsx3.init(debug=True)

    def speech(self, text, voice_id=None, tune_down=-20):
        console.log("slowing down a bit")
        rate = self._engine.getProperty('rate')
        self._engine.setProperty('rate', rate + tune_down)

        if voice_id is not None:
            voice = self._engine.getProperty('voices')[voice_id]
            self._engine.setProperty('voice', voice.id)
            console.log(f"using voice #{voice_id}: {voice.name}")

        console.log("queuing text task")
        self._engine.say(text)
        console.log("synthetizing speech...")
        self._engine.runAndWait()

        return "ok"

    def __del__(self, *args, **kwargs):
        console.log("shutting down engine")
        self._engine.stop()


@click.command()
@click.option("-p", "--port", default=4242)
def serve(port):
    console.log("initializing RPC service")
    service = zerorpc.Server(TTSRPC())
    service.bind(f'tcp://0.0.0.0:{port}')

    console.log(f'listening on tcp://0.0.0.0:{port}')
    try:
        service.run()
    except KeyboardInterrupt:
        console.log("caught interruption, shutting down")


if __name__ == '__main__':
    serve()
