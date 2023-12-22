from spade import agent
from Behaviours.Register_Veiculo_Behaviour import RegisterVeiculo_Behav
from Behaviours.listening_veiculo_behav import Listening_Veiculo_Behaviour

class VeiculoAgent(agent.Agent):

    atributos = None

    async def setup(self):
        print("Agent {}".format(str(self.jid)) + " starting...")
        a = RegisterVeiculo_Behav()
        b = Listening_Veiculo_Behaviour()
        self.add_behaviour(a)
        self.add_behaviour(b)