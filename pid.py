from ctypes import * 
import os

so_file = os.path.join(os.path.dirname(__file__),'src/pid/pid.so')

pid_functions = CDLL(so_file)
pid_functions.pid_configura_constantes.argtypes = [c_double,c_double,c_double]
pid_functions.pid_atualiza_referencia.argtypes = [c_double]
pid_functions.pid_controle.argtypes = [c_double]
pid_functions.pid_controle.restype = c_double

def pid_configura_constantes(kp,ki,kd):
    pid_functions.pid_configura_constantes(kp,ki,kd)

def pid_atualiza_referencia(referencia):    
    pid_functions.pid_atualiza_referencia(referencia)

def pid_controle(temp_interna):
    return pid_functions.pid_controle(temp_interna)

