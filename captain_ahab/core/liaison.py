import asyncio
from . import randomizer


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
        asyncio.run(self.operate())

    async def operate(self):
        """ Main logic loop """

        while not self.captain.dead:
            if not self.captain.ready:
                await self.captain.train()

            # start a task to update the captain and his timepieces
            # update_task = asyncio.create_task(self.captain.update())

            # await update_task
            self.captain.dead = True

            # Wait a random amount before proceeding
            await asyncio.sleep(randomizer.random_wait())


__all__ = ['AnimaLiaison']
