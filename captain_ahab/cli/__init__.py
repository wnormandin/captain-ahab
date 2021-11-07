import click
import click_log
import logging

from ..core import CaptainAhab


logger = logging.getLogger(__name__)
click_log.basic_config(logger)


@click.group()
@click_log.simple_verbosity_option(logger=logger)
def cli():
    """ CaptainAhab's Command-Line Interface """


@cli.command()
def start():
    """ Start CaptainAhab (hit Ctrl+C to kill) """
    CaptainAhab.run()


if __name__ == '__main__':
    cli(prog_name='captain-ahab')
