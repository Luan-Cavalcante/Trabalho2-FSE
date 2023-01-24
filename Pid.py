class PID():
    def __init__(self) -> None:
        # interface de comando 
        self.sinal_de_controle = 0.0
        self.referencia = 0.0
        self.Kp = 0.0  # Ganho Proporcional
        self.Ki = 0.0  # Ganho Integral
        self.Kd = 0.0  # Ganho Derivativo
        self.T = 1.0   # Período de Amostragem (ms)
        self.erro_total = 0.0
        self.erro_anterior = 0.0
        self.sinal_de_controle_MAX = 100.0
        self.sinal_de_controle_MIN = -100.0

    def pid_configura_constantes(self,Kp_, Ki_, Kd_):
        self.Kp = Kp_
        self.Ki = Ki_
        self.Kd = Kd_

    def pid_controle(self,saida_medida: float)-> float:
        erro = self.referencia - saida_medida
        print(self.referencia)
        print(f'error eh de {erro}')
        self.erro_total += erro

        if self.erro_total >= self.sinal_de_controle_MAX:
            self.erro_total = self.sinal_de_controle_MAX

        elif self.erro_total <= self.sinal_de_controle_MIN:
            self.erro_total = self.sinal_de_controle_MIN
            
        delta_error = erro - self.erro_anterior
        print(delta_error)

        self.sinal_de_controle = self.Kp*erro + (self.Ki*self.T)*self.erro_total + (self.Kd/self.T)*delta_error
        
        print(self.sinal_de_controle)

        if self.sinal_de_controle >= self.sinal_de_controle_MAX:
            self.sinal_de_controle = self.sinal_de_controle_MAX

        elif self.sinal_de_controle <= self.sinal_de_controle_MIN:
            self.sinal_de_controle = self.sinal_de_controle_MIN
        
        print(self.erro_anterior)
        self.erro_anterior = erro

        return self.sinal_de_controle

    def pid_atualiza_referencia(self,referencia_):
        self.referencia = referencia_
    
