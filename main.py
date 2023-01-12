import pid
import temp_ambiente


pid.pid_configura_constantes(30.0,0.2,400.0)
pid.pid_atualiza_referencia(80.0)

print(pid.pid_controle(35.0))