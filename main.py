import time

from Agentes.ugve import UgveAgent
from Agentes.hospital import HospitalAgent
from Agentes.veiculo import VeiculoAgent
from Agentes.paciente import PacienteAgent
from spade import quit_spade

XMPP_SERVER = 'desktop-seqnlnu.home'
PASSWORD = 'NOPASSWORD'

if __name__ == "__main__":

    manager_jid = 'manager@' + XMPP_SERVER
    manager_agent = UgveAgent(manager_jid, PASSWORD)

    res_manager = manager_agent.start(auto_register=True)
    res_manager.result()

    hospital_jid = 'hospital@' + XMPP_SERVER
    hospital_agent = HospitalAgent(hospital_jid, PASSWORD)
    hospital_agent.set('ugve_contact','manager@'+XMPP_SERVER)
    res_hospital = hospital_agent.start(auto_register=True)

    veiculo_jid = 'veiculo@' + XMPP_SERVER
    veiculo_agent = VeiculoAgent(veiculo_jid, PASSWORD)
    veiculo_agent.set('ugve_contact', 'manager@' + XMPP_SERVER)
    res_veiculo = veiculo_agent.start(auto_register=True)

    res_veiculo.result()
    res_hospital.result()
    paciente_jid = 'paciente@' + XMPP_SERVER
    paciente_agent = PacienteAgent(paciente_jid, PASSWORD)
    paciente_agent.set('ugve_contact', 'manager@' + XMPP_SERVER)
    res_paciente = paciente_agent.start(auto_register=True)
    while manager_agent.is_alive():
        try:
            time.sleep(1)
        except KeyboardInterrupt:
            hospital_agent.stop()
            veiculo_agent.stop()
            paciente_agent.stop()
            break
    print('Agents finished')

    # finish all the agents and behaviors running in your process
    quit_spade()