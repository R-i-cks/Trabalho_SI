from spade import agent
from Behaviours.listening_behaviour import Listening_Behaviour

class UgveAgent(agent.Agent):

    hospitais = []
    veiculos = []
    processos = {}
    async def setup(self):
        print("Agent {}".format(str(self.jid)) + " starting...")
        a = Listening_Behaviour()
        self.add_behaviour(a)