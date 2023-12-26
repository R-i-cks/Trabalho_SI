import time

from Agentes.ugve import UgveAgent
from Agentes.hospital import HospitalAgent
from Agentes.veiculo import VeiculoAgent
from Agentes.paciente import PacienteAgent
from spade import quit_spade

XMPP_SERVER = 'desktop-seqnlnu.home'
PASSWORD = 'NOPASSWORD'
MAX_VEICULOS = 10
MAX_PACIENTES = 10
MAX_HOSPITAIS = 5
Especialidades = ["Cardiologia", "Pneumologia", "Pediatria", "Ortopedia", "Obstetricia", "Traumatologia",
                          "Neurologia", "Urologia"]
if __name__ == "__main__":

    veiculo_agents_list = []
    hospital_agents_list = []
    paciente_agents_list = []

    manager_jid = 'manager@' + XMPP_SERVER
    manager_agent = UgveAgent(manager_jid, PASSWORD)

    res_manager = manager_agent.start(auto_register=True)
    res_manager.result()



    for i in range(1, MAX_VEICULOS+1):

        if i % 3 == 0:
            time.sleep(1)

        veiculo_jid = 'veiculo' + str(i) + '@' + XMPP_SERVER
        veiculo_agent = VeiculoAgent(veiculo_jid, PASSWORD)
        veiculo_agent.set('ugve_contact', 'manager@' + XMPP_SERVER)
        res_veiculo = veiculo_agent.start(auto_register=True)

        res_veiculo.result()
        veiculo_agents_list.append(veiculo_agent)

    for i in range(1, MAX_HOSPITAIS+1):

        if i % 3 == 0:
            time.sleep(1)

        hospital_jid = 'hospital' + str(i) + '@' + XMPP_SERVER
        hospital_agent = HospitalAgent(hospital_jid, PASSWORD)
        hospital_agent.set('ugve_contact', 'manager@' + XMPP_SERVER)
        res_hospital = hospital_agent.start(auto_register=True)

        res_hospital.result()
        hospital_agents_list.append(hospital_agent)


    time.sleep(3)

    for i in range(1, MAX_PACIENTES + 1):

        if i % 10 == 0:
            time.sleep(1)

        paciente_jid = 'paciente' + str(i) + '@' + XMPP_SERVER
        paciente_agent = PacienteAgent(paciente_jid, PASSWORD)
        paciente_agent.set('ugve_contact', 'manager@' + XMPP_SERVER)
        res_paciente = paciente_agent.start(auto_register=True)

        res_paciente.result()
        paciente_agents_list.append(paciente_agent)
    time.sleep(3)

    while manager_agent.is_alive():
        try:
            time.sleep(1)
        except KeyboardInterrupt:
            for paciente_agent in paciente_agents_list:
                paciente_agent.stop()

            for veiculo_agent in veiculo_agents_list:
                veiculo_agent.stop()

            for hospital_agent in hospital_agents_list:
                hospital_agent.stop()

            break
    print('Agents finished')


    quit_spade()