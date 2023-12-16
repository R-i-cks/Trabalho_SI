import random

from spade.behaviour import OneShotBehaviour
from spade.message import Message

from Classes.reg_hospital import Reg_Hospital
from Classes.position import Position
import jsonpickle

class RegisterHospital_Behav (OneShotBehaviour):

    async def run(self):
        Especialidades = ["Cardiologia", "Pneumologia", "Pediatria", "Ortopedia", "Obstetricia", "Traumatologia",
                          "Neurologia", "Urologia"]

        self.agent.atributos = Reg_Hospital(str(self.agent.jid),
                                          Position(random.randint(1, 100), random.randint(1, 100)),
                                            random.choice([True,False]),random.sample(Especialidades,random.randint(1,len(Especialidades))))

        print("Agent {}:".format(str(self.agent.jid)) + " Hospital initialized with {}".format(self.agent.atributos.toString()))

        msg = Message(to=self.agent.get("ugve_contact"))
        msg.body = jsonpickle.encode(self.agent.atributos)
        msg.set_metadata("performative", "subscribe")

        print("Agent {}:".format(str(self.agent.jid)) + " Hospital Agent subscribing to UGVE Agent {}".format(str(self.agent.get("ugve_contact"))))
        await self.send(msg)