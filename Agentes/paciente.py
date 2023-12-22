from spade import agent
from Behaviours.request_help import Request_Help

class PacienteAgent(agent.Agent):
    pedido = None

    async def setup(self):
        print("Agent {}".format(str(self.jid)) + " starting...")
        a = Request_Help()
        self.add_behaviour(a)