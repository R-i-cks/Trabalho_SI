from Classes.position import Position

class Reg_Hospital:

        def __init__(self, agent_jid: str, position: Position, available: bool,especialidades:list,ocupado: bool ):
            self.agent_jid = agent_jid
            self.position = position
            self.heliporto = available
            self.especialidade = especialidades
            self.heli_ocupado = ocupado
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
        def getOcupado(self):
            return self.heli_ocupado

        def setOcupado(self,ocup):
            self.heli_ocupado = ocup
        def toString(self):
            return "Reg_Hospital [agent_jid=" + self.agent_jid + ", position=" + self.position.toString() + ", heliporto=" + str(
                self.heliporto) +" especialidades=" + str(self.especialidade) + "heliporto ocupado=" + str(self.heli_ocupado) + "]"