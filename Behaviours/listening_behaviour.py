from spade.behaviour import CyclicBehaviour
import jsonpickle
import math
from spade.message import Message

class Listening_Behaviour(CyclicBehaviour):
    async def run(self):
        processos={}
        msg = await self.receive(timeout=10)

        if msg:
            performative = msg.get_metadata("performative")
            if performative == "subscribe":
                if "hospital" in str(msg.sender):
                    if str(msg.sender) not in self.agent.hospitais.keys():
                        registry = jsonpickle.decode(msg.body)
                        self.agent.hospitais[str(msg.sender)]=registry
                        print("Agent {}:".format(str(self.agent.jid)) + " Hospital Agent {} registered!".format(str(msg.sender)))
                    else:
                        registry = jsonpickle.decode(msg.body)
                        self.agent.hospitais[str(msg.sender)] = registry
                        print("Agent {}:".format(str(self.agent.jid)) + " Hospital Agent {} registered!".format(
                            str(msg.sender)))

                else:
                    registry = jsonpickle.decode(msg.body)
                    self.agent.veiculos.append(registry)
                    print("Agent {}:".format(str(self.agent.jid)) + " Veiculo Agent {} registered!".format(
                        str(msg.sender)))

            elif performative == "confirm":
                # Pode ser do veiculo que chegou ao paciente, que chegou ao hospital ou do hospital a confirmar que vai receber paciente
                msg_info = jsonpickle.decode(msg.body)
                if "veiculo" in str(msg.sender):
                    hospital = Message(to=processos[msg_info.getAgent()][0])
                    hospital.set_metadata("performative", "request")
                    hospital.body = jsonpickle.encode(msg_info)
                    await self.send(hospital)

                elif "hospital" in str(msg.sender):
                    veiculo = Message(to=processos[msg_info.getAgent()][1])
                    veiculo.set_metadata("performative", "inform")
                    veiculo.body = jsonpickle.encode(processos[msg_info.getAgent()][0])
                    await self.send(veiculo)

            elif performative == "inform":
                msg_info = jsonpickle.decode(msg.body)
                processos.pop(msg_info.getAgent())
                for veiculos in self.agent.veiculos:
                    if veiculos.getAgent() == msg.sender:
                        veiculos.setAvailable(True)
                print("O paciente chegou ao hospital.")

            elif performative == "refuse":
                msg_info = jsonpickle.decode(msg.body)
                dist_min = 1000
                if processos[msg_info.getAgent()][1].getTipo != 'helicoptero':

                    for ind, hospital in enumerate(self.agent.hospitais):

                        if msg_info.getEspecialidade() in hospital.getEspecialidade() :
                            distance = math.sqrt(
                                math.pow(hospital.getPosition().getX() - msg_info.getPosition().getX(),2) +
                                math.pow(hospital.getPosition().getY() - msg_info.getPosition().getY(), 2)
                                )

                            if (dist_min > distance):
                                dist_min = distance
                                processos[msg_info.getAgent()][0] = hospital

                    hospital_msg = Message(to=processos[msg_info.getAgent()][0])
                    hospital_msg.set_metadata("performative", "request")
                    hospital_msg.body = jsonpickle.encode(msg_info)
                    await self.send(hospital_msg)

                else:
                    for ind, hospital in enumerate(self.agent.hospitais):

                        if msg_info.getEspecialidade() in hospital.getEspecialidade() and hospital.isAvailable():
                            distance = (
                                    abs(hospital.getPosition().getX() - msg_info.getPosition().getX()) +
                                    abs(hospital.getPosition().getY() - msg_info.getPosition().getY())
                            )

                            if (dist_min > distance):
                                dist_min = distance
                                processos[msg_info.getAgent()][0] = hospital

                    hospital_msg = Message(to=processos[msg_info.getAgent()][0])
                    hospital_msg.set_metadata("performative", "request")
                    hospital_msg.body = jsonpickle.encode(msg_info)
                    await self.send(hospital_msg)

            elif performative == "request":
                print("Agent {}:".format(str(self.agent.jid)) + " Paciente Agent {} requested HEEEEEELLLLLLP!".format(
                    str(msg.sender)))
                transport_request = jsonpickle.decode(msg.body)

                dist_min = 1000.0

                dic_terrestre = {}
                dic_heli = {'total':0}

                for ind, hospital in enumerate(self.agent.hospitais):
                    if transport_request.getEspecialidade() in hospital.getEspecialidade():
                        distance = (
                            abs(hospital.getPosition().getX() - transport_request.getPosition().getX()) +
                            abs(hospital.getPosition().getY() - transport_request.getPosition().getY())
                        )

                        if (dist_min > distance):

                            dist_min = distance

                dic_terrestre['total'] = dist_min
                dist_min = 1000.0
                for ind, veiculos in enumerate(self.agent.veiculos):
                    if veiculos.getTipo() != 'Helicoptero' and veiculos.isAvailable():
                        distance = (
                                abs(veiculos.getPosition().getX() - transport_request.getPosition().getX()) +
                                abs(veiculos.getPosition().getY() - transport_request.getPosition().getY())
                        )

                        if (dist_min > distance):
                            dic_terrestre['veiculo'] = veiculos
                            dic_terrestre['vei_index'] = ind
                            dist_min = distance

                dic_terrestre['total'] = dic_terrestre['total'] + dist_min

                dist_min = 1000.0
                if transport_request.getEstado() == "MG":
                    for ind, hospital in enumerate(self.agent.hospitais):

                        if transport_request.getEspecialidade() in hospital.getEspecialidade() and hospital.isAvailable():
                            distance = math.sqrt(
                                math.pow(hospital.getPosition().getX() - transport_request.getPosition().getX(), 2) +
                                math.pow(hospital.getPosition().getY() - transport_request.getPosition().getY(), 2)
                            )

                            if (dist_min > distance):

                                dist_min = distance

                    dic_heli['total'] = dist_min
                    dist_min = 1000.0
                    for ind, veiculos in enumerate(self.agent.veiculos):
                        if veiculos.getTipo() == 'Helicoptero' and veiculos.isAvailable():
                            distance = math.sqrt(
                                math.pow(veiculos.getPosition().getX() - transport_request.getPosition().getX(), 2) +
                                math.pow(veiculos.getPosition().getY() - transport_request.getPosition().getY(), 2)
                            )

                            if (dist_min > distance):
                                dic_heli['veiculo'] = veiculos
                                dic_heli['vei_index'] = ind
                                dist_min = distance

                    dic_heli['total'] = dic_heli['total'] + dist_min

                if dic_terrestre['total']/120 < dic_heli['total']/400:
                    # Enviar pedido ao veiculo terrestre mais próximo
                    print("Agent {}:".format(
                        str(self.agent.jid)) + " Veiculo Agent {} selected for Transport Request!".format(
                        dic_terrestre['veiculo'].getAgent()))

                    processos[msg.sender] = [dic_terrestre['hospital'], dic_terrestre['veiculo']]
                    msg = Message(to=dic_terrestre['veiculo'].getAgent())
                    msg.body = jsonpickle.encode(transport_request)
                    msg.set_metadata("performative", "request")
                    await self.send(msg)

                    self.agent.veiculos[dic_terrestre['vei_index']].setAvailable(False)

                elif dic_terrestre['total']/120 > dic_heli['total']/400:
                    # Enviar pedido ao helicoptero mais próximo
                    print("Agent {}:".format(
                        str(self.agent.jid)) + " Veiculo Agent {} selected for Transport Request!".format(
                        dic_heli['veiculo'].getAgent()))

                    processos[msg.sender] = [dic_heli['hospital'], dic_heli['veiculo']]
                    msg = Message(to=dic_heli['veiculo'].getAgent())
                    msg.body = jsonpickle.encode(transport_request)
                    msg.set_metadata("performative", "request")
                    await self.send(msg)

                    self.agent.veiculos[dic_heli['vei_index']].setAvailable(False)

                else:
                    print("Agent {}:".format(str(self.agent.jid)) + " No Taxis available!")
                    msg = msg.make_reply()
                    msg.set_metadata("performative", "refuse")
                    await self.send(msg)

            else:
                print("Agent {}:".format(str(self.agent.jid)) + " Message not understood!")

        else:
            print("Agent {}:".format(str(self.agent.jid)) + "Did not received any message after 10 seconds")
            self.kill()

    async def on_end(self):
        await self.agent.stop()