import random

from spade.behaviour import PeriodicBehaviour
from spade.message import Message

import jsonpickle

class VerificarEspecialidade_Behav (PeriodicBehaviour):

    async def run(self):


        if random.randint(-100, 10) > 0:
            self.agent.atributos.removeEspecialidade(random.sample(self.agent.atributos.getEspecialidade(),
                                                                   random.randint(1,len(self.agent.atributos.getEspecialidade()))))

            msg = Message(to=self.agent.get("ugve_contact"))
            msg.body = jsonpickle.encode(self.agent.atributos)
            msg.set_metadata("performative", "subscribe")
            await self.send(msg)

        print("Agent {}:".format(str(self.agent.jid)) + " Hospital Agent subscribing to UGVE Agent {}".format(str(self.agent.get("ugve_contact"))))
