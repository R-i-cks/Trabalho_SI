from spade import agent

from Behaviours.Register_Hospital_Behaviour import RegisterHospital_Behav
from Behaviours.verificar_especialidade import VerificarEspecialidade_Behav
from Behaviours.listening_hospital_behav import Listening_Hospital_Behaviour

class HospitalAgent(agent.Agent):

    atributos = None

    async def setup(self):
        print("Agent {}".format(str(self.jid)) + " starting...")
        a = RegisterHospital_Behav()
        b = VerificarEspecialidade_Behav(period=24)
        c = Listening_Hospital_Behaviour()
        self.add_behaviour(a)
        self.add_behaviour(b)
        self.add_behaviour(c)