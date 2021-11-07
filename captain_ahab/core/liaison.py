import asyncio
import logging
from queue import Empty
from . import randomizer


logger = logging.getLogger(__name__)


class AnimaLiaison:
    """
    Anima Liaison is responsible for the actual operation of our automaton

    At its core is a state machine which queues and monitors jobs to be satisfied by the captain.  Those jobs
    are executed by calling upon the following components:

        captain.angler
        captain.eyes
        captain.legs
        captain.voice
    """

    def __init__(self, captain):
        self.captain = captain

    def dispatch(self):
        """ This is the application entry point where the `operate` coroutine is invoked """
        try:
            asyncio.run(self.operate())
        except (KeyboardInterrupt, SystemExit):
            self.captain.kill()
            logger.debug('Exiting')

    async def operate(self):
        """ Main logic loop """

        while self.captain.alive:
            if not self.captain.ready:
                await self.captain.train()

            await self.captain.update()

            self.captain.look()

            try:
                while True:
                    result = await self.captain.perform_next_action()
                    if result is not None:
                        await result()
            except Empty:
                logger.debug(f'No more actions in queue')

            # Wait a random amount before proceeding
            await asyncio.sleep(randomizer.random_wait())


__all__ = ['AnimaLiaison']
