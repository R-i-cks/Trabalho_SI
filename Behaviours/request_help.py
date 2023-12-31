from spade.behaviour import OneShotBehaviour
from Classes.reg_ajuda import Reg_Ajuda
import random
from Classes.position import Position
import jsonpickle
from spade.message import Message

class Request_Help(OneShotBehaviour):

    async def run(self):
        Especialidades = ["Cardiologia", "Pneumologia", "Pediatria", "Ortopedia", "Obstetricia", "Traumatologia",
                          "Neurologia", "Urologia"]
        self.agent.atributos = Reg_Ajuda(str(self.agent.jid),
                                            Position(random.randint(1, 1000), random.randint(1, 1000)),
                                            random.choice(["MG","G","L"]),
                                            random.choice(Especialidades))

        print("Agent {}:".format(str(self.agent.jid)) + " Paciente initialized with {}".format(
            self.agent.atributos.toString()))

        msg = Message(to=self.agent.get("ugve_contact"))
        msg.body = jsonpickle.encode(self.agent.atributos)
        msg.set_metadata("performative", "request")

        print("Agent {}:".format(str(self.agent.jid)) + " HEEEEEEELLLLLLP!!! {}".format(
            str(self.agent.get("ugve_contact"))))
        await self.send(msg)

    async def on_end(self):
        await self.agent.stop()