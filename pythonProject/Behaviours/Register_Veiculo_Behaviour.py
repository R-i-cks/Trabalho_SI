import random

from spade.behaviour import OneShotBehaviour
from spade.message import Message

from Classes.reg_veiculo import Reg_Veiculo
from Classes.position import Position
import jsonpickle

class RegisterVeiculo_Behav (OneShotBehaviour):

    async def run(self):
        aleatorio = random.randint(1,10)
        if aleatorio == 10:
            escolha = "Helicoptero"
        elif aleatorio > 6:
            escolha = "Ambulancia_INEM"
        else:
            escolha = "Ambulancia"
        self.agent.atributos = Reg_Veiculo(str(self.agent.jid),
                                          Position(random.randint(1, 100), random.randint(1, 100)),True,escolha)

        print("Agent {}:".format(str(self.agent.jid)) + " Veiculo initialized with {}".format(self.agent.atributos.toString()))

        msg = Message(to=self.agent.get("ugve_contact"))
        msg.body = jsonpickle.encode(self.agent.atributos)
        msg.set_metadata("performative", "subscribe")

        print("Agent {}:".format(str(self.agent.jid)) + " Veiculo Agent subscribing to UGVE Agent {}".format(str(self.agent.get("ugve_contact"))))
        await self.send(msg)