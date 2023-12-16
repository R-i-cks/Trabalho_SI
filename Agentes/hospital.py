from spade import agent

from Behaviours.Register_Hospital_Behaviour import RegisterHospital_Behav


class HospitalAgent(agent.Agent):

    atributos = None

    async def setup(self):
        print("Agent {}".format(str(self.jid)) + " starting...")
        a = RegisterHospital_Behav()
        self.add_behaviour(a)