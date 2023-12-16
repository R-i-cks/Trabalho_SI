from Classes.position import Position

class Reg_Ajuda:

        def __init__(self, agent_jid: str, position: Position, estado: str,especialidade:str):
            self.agent_jid = agent_jid
            self.position = position
            self.estado = estado
            self.especialidade = especialidade

        def getAgent(self):
            return self.agent_jid

        def getPosition(self):
            return self.position

        def setPosition(self, x: int, y: int):
            self.position = Position(x, y)

        def setPosition(self, position: Position):
            self.position = position

        def getEstado(self):
            return self.estado

        def getEspecialidade(self):
            return self.especialidade


        def toString(self):
            return "Reg_Ajuda [agent_jid=" + self.agent_jid + ", position=" + self.position.toString() + ", estado=" + str(
                self.estado) +" especialidade=" + str(self.especialidade) + "]"