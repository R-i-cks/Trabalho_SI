from Classes.position import Position


class Reg_Veiculo:
    def __init__(self, agent_jid: str, position: Position, available: bool,tipo: str):
        self.agent_jid = agent_jid
        self.position = position
        self.available = available
        self.tipo = tipo

    def getAgent(self):
        return self.agent_jid

    def getPosition(self):
        return self.position

    def setPosition(self, x: int, y: int):
        self.position = Position(x, y)

    def setPosition(self, position: Position):
        self.position = position

    def isAvailable(self):
        return self.available

    def setAvailable(self, available: bool):
        self.available = available

    def getTipo(self):
        return self.tipo

    def toString(self):
        return "Reg_Veiculo [agent_jid=" + self.agent_jid + ", position=" + self.position.toString() + ", available=" + str(
            self.available) +", tipo="+ self.tipo + "]"