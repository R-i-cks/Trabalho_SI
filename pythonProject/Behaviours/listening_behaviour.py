from spade.behaviour import CyclicBehaviour
import jsonpickle

class Listening_Behaviour(CyclicBehaviour):
    async def run(self):
        msg = await self.receive(timeout=10)

        if msg:
            performative = msg.get_metadata("performative")
            if performative == "subscribe":
                if "hospital" in str(msg.sender):
                    registry = jsonpickle.decode(msg.body)
                    self.agent.hospitais.append(registry)
                    print("Agent {}:".format(str(self.agent.jid)) + " Hospital Agent {} registered!".format(str(msg.sender)))
                else:
                    registry = jsonpickle.decode(msg.body)
                    self.agent.veiculos.append(registry)
                    print("Agent {}:".format(str(self.agent.jid)) + " Veiculo Agent {} registered!".format(
                        str(msg.sender)))

            elif performative == "confirm":  # Handle the taxi transportation conclusion
                msg_taxi_info = jsonpickle.decode(msg.body)
                for idx, taxi_info in enumerate(self.agent.taxis_subscribed):
                    if taxi_info.getAgent() == msg_taxi_info.getAgent():
                        print(
                            "Agent {}:".format(str(self.agent.jid)) + " Agent {} just arrived!".format(str(msg.sender)))

                        # Update selected Taxi info (i.e., Availability = False and Position = Destiny Position)
                        self.agent.taxis_subscribed[idx] = msg_taxi_info
                        break

            elif performative == "request":  # Handle the Client transport request
                print("Agent {}:".format(str(self.agent.jid)) + " Paciente Agent {} requested HEEEEEELLLLLLP!".format(
                    str(msg.sender)))
                transport_request = jsonpickle.decode(msg.body)

                # Search for closest available taxi
                closestTaxi = None
                list_pos = -1
                dist_min = 1000.0

                # Calculate distance of each taxi with customer init position
                for idx, taxi_info in enumerate(self.agent.taxis_subscribed):
                    # Verify InformPosition of Taxi Agent presents Available as True (is the Taxi available or already blocked by another transport Request?)
                    if taxi_info.isAvailable():
                        distance = math.sqrt(
                            math.pow(taxi_info.getPosition().getX() - transport_request.getInit().getX(), 2) +
                            math.pow(taxi_info.getPosition().getY() - transport_request.getInit().getY(), 2)
                        )

                        if (dist_min > distance):
                            closestTaxi = taxi_info
                            list_pos = idx
                            dist_min = distance

                # Taxi Available = send request
                if list_pos > -1:
                    print("Agent {}:".format(
                        str(self.agent.jid)) + " Taxi Agent {} selected for Transport Request!".format(
                        closestTaxi.getAgent()))

                    msg = Message(to=closestTaxi.getAgent())  # Instantiate the message
                    msg.body = jsonpickle.encode(transport_request)  # Set the message content (serialized object)
                    msg.set_metadata("performative", "request")  # Set the message performative
                    await self.send(msg)

                    # Update selected Taxi info (i.e., Availability = False and Position = Destiny Position)
                    # self.agent.taxis_subscribed[list_pos] = InformPosition(closestTaxi.getAgent(), transport_request.getDest(), False)
                    self.agent.taxis_subscribed[list_pos].setAvailable(False)
                    self.agent.taxis_subscribed[list_pos].setPosition(transport_request.getDest())

                # No Taxi Available = send refuse
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