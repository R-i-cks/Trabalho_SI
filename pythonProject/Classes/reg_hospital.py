from Classes.position import Position

class Reg_Hospital:

        def __init__(self, agent_jid: str, position: Position, available: bool,especialidades:list):
            self.agent_jid = agent_jid
            self.position = position
            self.heliporto = available
            self.especialidade = especialidades

        def getAgent(self):
            return self.agent_jid

        def getPosition(self):
            return self.position

        def setPosition(self, x: int, y: int):
            self.position = Position(x, y)

        def setPosition(self, position: Position):
            self.position = position

        def isAvailable(self):
            return self.heliporto

        def setAvailable(self, available: bool):
            self.heliporto = available

        def getEspecialidade(self):
            return self.especialidade

        def setEspecialidade(self,novas_esp):
            self.especialidade = novas_esp

        def addEspecialidade(self,elem):
            self.especialidade.append(elem)

        def removeEspecialidade(self,elem):
            self.especialidade.remove(elem)

        def toString(self):
            return "Reg_Hospital [agent_jid=" + self.agent_jid + ", position=" + self.position.toString() + ", heliporto=" + str(
                self.heliporto) +" especialidades=" + str(self.especialidade) + "]"