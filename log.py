import time 

from datetime import datetime, timezone,timedelta


def log(mensagem):
    diferenca = timedelta(hours=-3)
    fuso_horario = timezone(diferenca)
    data_e_hora_atuais = datetime.now()
    data_e_hora_sao_paulo = data_e_hora_atuais.astimezone(fuso_horario)
    data_e_hora_sao_paulo_em_texto = data_e_hora_sao_paulo.strftime("%d/%m/%Y, %H:%M")

    with open("log.csv","a") as f:
        f.write(data_e_hora_sao_paulo_em_texto+','+mensagem)
        f.close()