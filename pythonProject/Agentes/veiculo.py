from spade import agent
from Behaviours.Register_Veiculo_Behaviour import RegisterVeiculo_Behav

class VeiculoAgent(agent.Agent):

    atributos = None

    async def setup(self):
        print("Agent {}".format(str(self.jid)) + " starting...")
        a = RegisterVeiculo_Behav()
        self.add_behaviour(a)