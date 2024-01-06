import random
import time
from spade.behaviour import CyclicBehaviour
import jsonpickle
import math
from spade.message import Message
from Classes.position import Position

class Listening_Veiculo_Behaviour(CyclicBehaviour):
    async def run(self):
        msg = await self.receive(timeout=300)
        if msg:
            if msg.get_metadata("performative") == "request":
                pedido = jsonpickle.decode(msg.body)
                if self.agent.atributos.isAvailable():
                    if self.agent.atributos.getTipo() == 'Helicoptero':
                        distance = (
                                abs(self.agent.atributos.getPosition().getX() - pedido.getPosition().getX()) +
                                abs(self.agent.atributos.getPosition().getY() - pedido.getPosition().getY())
                        )
                    else:
                        distance = math.sqrt(
                            math.pow(self.agent.atributos.getPosition().getX() - pedido.getPosition().getX(), 2) +
                            math.pow(self.agent.atributos.getPosition().getY() - pedido.getPosition().getY(), 2)
                        )
                    if self.agent.atributos.getTipo() != 'Helicoptero':
                        velocidade = 120
                    else:
                        velocidade = 400

                    time.sleep(distance/velocidade)
                    self.agent.processos = pedido
                    self.agent.atributos.setPosition(pedido.getPosition())
                    resposta = Message(to=str(msg.sender))
                    resposta.set_metadata("performative", "confirm")
                    resposta.body = msg.body
                    await self.send(resposta)
                    print(str(self.agent.jid) + ": chegou ao paciente")

                else:
                    resposta = Message(to=str(msg.sender))
                    resposta.set_metadata("performative", "refuse")
                    resposta.body = msg.body
                    await self.send(resposta)
                    print(str(self.agent.jid) + ": recusou pedido")

            elif msg.get_metadata("performative") == "inform":
                hospital = jsonpickle.decode(msg.body)
                if self.agent.atributos.getTipo() == 'Helicoptero':
                    distance = (
                            abs(self.agent.atributos.getPosition().getX() - hospital.getPosition().getX()) +
                            abs(self.agent.atributos.getPosition().getY() - hospital.getPosition().getY())
                    )
                else:
                    distance = math.sqrt(
                        math.pow(self.agent.atributos.getPosition().getX() - hospital.getPosition().getX(), 2) +
                        math.pow(self.agent.atributos.getPosition().getY() - hospital.getPosition().getY(), 2)
                    )
                if self.agent.atributos.getTipo() != 'Helicoptero':
                    velocidade = 120
                else:
                    velocidade = 400
                time.sleep(distance / velocidade)

                self.agent.atributos.setPosition(hospital.getPosition())
                resposta = Message(to=str(msg.sender))
                resposta.set_metadata("performative", "inform")
                resposta.body = jsonpickle.encode(self.agent.processos)
                await self.send(resposta)

                resposta = Message(to=hospital.getAgent())
                resposta.set_metadata("performative", "inform")
                resposta.body = jsonpickle.encode(self.agent.processos)
                await self.send(resposta)

                print(str(self.agent.jid) + ": paciente chegou ao hospital")
                x,y = random.randint(1,1000), random.randint(1,1000)
                self.agent.atributos.setPosition(Position(x, y))
                self.agent.atributos.setAvailable(True)
                msg = Message(to=self.agent.get("ugve_contact"))
                msg.body = jsonpickle.encode(self.agent.atributos)
                msg.set_metadata("performative", "subscribe")
                await self.send(msg)
        else:
            print(self.agent.atributos.getAgent() + "is about to kill himself")
            self.kill()

    async def on_end(self):
        await self.agent.stop()