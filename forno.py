
class Forno():
    def __init__(self):
        self.estado = False
        self.temp_interna = 0
        self.temp_referencia = 0
        self.temp_ambiente = 0
        self.funcionando = False

    def liga(self):
        self.estado = True
    
    def desliga(self)
        self.estado = False
    
    def funcionando(self):
        return self.funcionando
    
    def inicia_processo(self):
        self.funcionando = True

    def cancela_processo(self):
        self.funcionando = False
    
    def atualiza_temps(self,interna,referencia,ambiente):
        self.temp_interna = interna
        self.temp_referencia = referencia
        self.temp_ambiente = ambiente
        
    