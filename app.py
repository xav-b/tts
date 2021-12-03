#! /usr/bin/env python

"""Tinkering."""


import click
import pyttsx3
from rich.console import Console
from rich.table import Table


console = Console()

TEXT = "If you get installation errors , make sure you first upgrade your wheel version."


@click.group()
def cli():
    pass


@cli.command('voices')
def list_voices():
    engine = pyttsx3.init()

    table = Table(show_header=True, header_style='bold yellow')
    table.add_column('ID', style='dim')
    table.add_column('Name')
    table.add_column('Gender')
    table.add_column('Languages')
    table.add_column('Age', justify='right')

    for i, voice in enumerate(engine.getProperty('voices')):
        table.add_row(
            str(i),
            voice.name,
            voice.gender.replace('VoiceGender', ''),
            ', '.join(voice.languages),
            str(voice.age),
        )

    console.print(table)
    engine.stop()


@cli.command()
@click.option('--debug/--no-debug', default=False)
@click.option("-v", "--voice", "voice_id", type=click.INT, help="voice id to set")
@click.option("-t", "--text", required=True)
def speech(debug, voice_id, text):
    console.log(f"Debug mode is {'on' if debug else 'off'}")

    console.log("initialising engine")
    engine = pyttsx3.init(debug=debug)

    console.log("slowing down a bit")
    rate = engine.getProperty('rate')
    engine.setProperty('rate', rate - 20)

    if voice_id is not None:
        voice = engine.getProperty('voices')[voice_id]
        engine.setProperty('voice', voice.id)
        console.log(f"using voice #{voice_id}: {voice.name}")

    console.log("queuing text task")
    engine.say(text)
    console.log("synthetizing speech...")
    engine.runAndWait()

    console.log("shutting down engine")
    engine.stop()


if __name__ == '__main__':
    cli()
