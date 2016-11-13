from oam.dsl import *

class Default(Flow):
    """default flow"""

    def flow(self):
        self.run(sync,
                 glsa,
                 fetch,
                 update,
                 clean,
                 qcheck,
                 kernel
        )

class ParallelDefault(Flow):
    """default flow with parallel parts"""

    def flow(self):
        self.run(sync,
                 [glsa, fetch],
                 update,
                 [clean, qcheck],
                 kernel
        )

class Update(Flow):
    """default flow for update only"""

    def flow(self):
        self.run(update,
                 [clean, qcheck],
                 kernel
        )

class Container(Flow):
    """default flow for a container"""

    def flow(self):
        self.run([glsa, layman],
                 update,
                 qcheck
        )
            
class HostAndContainers(Flow):
    """default flow for a host plus containers"""

    def flow(self):
        self.run(sync,
                 [glsa, fetch],
                 update,
                 [clean, qcheck, Container(self)],
                 kernel
        )
