from spade.behaviour import CyclicBehaviour
import jsonpickle
from spade.message import Message


class Listening_Hospital_Behaviour(CyclicBehaviour):
    async def run(self):
        msg = await self.receive(timeout=10)

        if msg:
            if msg.get_metadata("performative") == "request":
                pedido = jsonpickle.decode(msg.body)
                if pedido.getEspecialidade() in self.agent.atributos.getEspecialidade():
                    resposta = Message(to=str(msg.sender))
                    resposta.set_metadata("performative", "confirm")
                    resposta.body = msg.body
                    await self.send(resposta)
                    print("Hospital: aceitou pedido")
                else:
                    resposta = Message(to=str(msg.sender))
                    resposta.set_metadata("performative", "refuse")
                    resposta.body = msg.body
                    await self.send(resposta)
                    print("Hospital: recusou pedido")

            elif msg.get_metadata("performative") == "inform":
                if "veiculo" in str(msg.sender):
                    print("Hospital: recebeu doente")
                else:
                    self.agent.atributos.setOcupado(jsonpickle.decode(msg.body).getOcupado())
        else:
            print("Hospital: não recebeu pedido!")