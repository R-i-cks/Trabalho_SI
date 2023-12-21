from spade.behaviour import CyclicBehaviour
import jsonpickle
import math
from spade.message import Message


class Listening_Hospital_Behaviour(CyclicBehaviour):
    async def run(self):
        msg = await self.receive()

        if msg:
            if msg.get_metadata("performative") == "request":
                pedido = jsonpickle.decode(msg.body)
                if pedido.getEspecialidade() in self.agent.atributos.getEspecialidade():
                    resposta = Message(to=msg.sender)
                    resposta.set_metadata("performative", "confirm")
                    resposta.body = msg.body
                    await self.send(resposta)
                    print("Hospital: aceitou pedido")
                else:
                    resposta = Message(to=msg.sender)
                    resposta.set_metadata("performative", "refuse")
                    resposta.body = msg.body
                    await self.send(resposta)
                    print("Hospital: recusou pedido")

            elif msg.get_metadata("performative") == "inform":
                print("Hospital: recebeu doente")
        else:
            print("Hospital: não recebeu pedido!")