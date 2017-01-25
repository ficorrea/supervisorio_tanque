# -*- coding: utf-8 -*-

import threading
import time

# Classes de tipos


class Valvula():
    valor_atual = 0

    def __init__(self):
        self.valor_atual = 0


class Tanque():
    valor_atual = 0
    valor_max = 0
    valor_min = 0

    def __init__(self, valor1, valor2):
        self.valor_atual = 0
        self.valor_max = valor1
        self.valor_min = valor2

# Controle das operações

sem_valvula = threading.Semaphore(1)
sem_geral = threading.Semaphore(6)

class Controle():
    valvula = Valvula()
    valvula1 = 0
    valvula2 = 0
    valvula3 = 0
    tanque1 = Tanque(1000, 0.0)
    tanque2 = Tanque(200, 0.0)
    temp_valor = 0

    def __init__(self):
        self.valvula.valor_atual = 0
        self.valvula1 = 0
        self.valvula2 = 0
        self.valvula3 = 0
        self.tanque1.valor_atual = 0
        self.tanque2.valor_atual = 0
        self.temp_valor = 0
        self.temp_tanque = 0

# Setar valor Válvulas

    def set_valve(self):
        self.valvula.valor_atual = self.temp_valor

    def update_valve(self):
        sem_valvula.acquire()
        self.set_valve()
        sem_valvula.release()

# Update Válvula 1

    def get_valve1(self):
        sem_valvula.acquire()
        valor_valve = self.valvula1
        sem_valvula.release()
        return valor_valve

    def update_screen_valve1(self):
        valor_valve = self.get_valve1()
        return valor_valve

# Update Válvula 2

    def get_valve2(self):
        sem_valvula.acquire()
        valor_valve = self.valvula2
        sem_valvula.release()
        return valor_valve

    def update_screen_valve2(self):
        valor_valve = self.get_valve2()
        return valor_valve

# Update Válvula 3

    def get_valve3(self):
        sem_valvula.acquire()
        valor_valve = self.valvula3
        sem_valvula.release()
        return valor_valve

    def update_screen_valve3(self):
        valor_valve = self.get_valve3()
        return valor_valve


# Tanque 1

    def set_tanque1(self):
        if self.tanque1.valor_atual <= self.tanque1.valor_max:
            self.tanque1.valor_atual = (self.tanque1.valor_atual + ((self.valvula1 * 2) / 100)) - ((self.valvula2 * 1) / 100)
            self.temp_tanque = 1
        if self.tanque1.valor_atual < self.tanque1.valor_min:
            self.tanque1.valor_atual = self.tanque1.valor_min
            self.temp_tanque = 0
        return self.tanque1.valor_atual

    def update_tanque1(self):
        sem_geral.acquire()
        valor_t1 = self.set_tanque1()
        sem_geral.release()
        return valor_t1

    def alerta_tanque1(self):
        sem_geral.acquire()
        valor_t1 = self.tanque1.valor_atual
        if valor_t1 == 0:
            texto = 'Atenção tanque vazio'
        elif valor_t1 > 900:
            texto = 'Alerta tanque com 90% ou mais da capacidade total!'
        else:
            texto = 'Tanque com substância'
        sem_geral.release()
        return texto

# Tanque 2

    def set_tanque2(self):
        if self.tanque2.valor_atual <= self.tanque2.valor_max and self.temp_tanque != 0:
            self.tanque2.valor_atual = (self.tanque2.valor_atual + ((self.valvula2 * 1) / 100)) - ((self.valvula3 * 1) / 100)
        if self.temp_tanque == 0:
            self.tanque2.valor_atual = self.tanque2.valor_atual - ((self.valvula3 * 1) / 100)
        if self.tanque2.valor_atual < self.tanque2.valor_min:
            self.tanque2.valor_atual = self.tanque2.valor_min
        return self.tanque2.valor_atual

    def update_tanque2(self):
        sem_geral.acquire()
        valor_t2 = self.set_tanque2()
        sem_geral.release()
        return valor_t2

    def alerta_tanque2(self):
        sem_geral.acquire()
        valor_t2 = self.tanque2.valor_atual
        if valor_t2 == 0:
            texto = 'Atenção tanque vazio'
        elif valor_t2 > 180:
            texto = 'Alerta tanque com 90% ou mais da capacidade total!'
        else:
            texto = 'Tanque com substância'
        sem_geral.release()
        return texto



# Misturador

    def update_mix_on(self):
        sem_geral.acquire()
        texto = 'Misturador ligado'
        sem_geral.release()
        return texto

    def update_mix_off(self):
        sem_geral.acquire()
        texto = 'Misturador desligado'
        sem_geral.release()
        return texto