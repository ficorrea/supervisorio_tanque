# -*- coding: utf-8 -*-

from PyQt4 import QtCore, QtGui
from PyQt4.QtCore import QThread, SIGNAL
import view.interface
import threading
import sys
import time
from model.classe_controle import Controle

semaforo = threading.Semaphore(1)
evento = threading.Event()


class tela(QtGui.QMainWindow, view.interface.Ui_Form):
    inicia_tela = 0

    def __init__(self):
        super(self.__class__, self).__init__()
        self.setupUi(self)
        self.control = Controle()
        self.inicia_tela = 1
        thread_update = threading.Thread(target=self.update)
        thread_update.start()
        thread_atualiza_tela = threading.Thread(target=self.update_screen)
        thread_atualiza_tela.start()
        self.pushButton_v1_enviar.clicked.connect(self.start_v1)
        self.pushButton_v2_enviar.clicked.connect(self.start_v2)
        self.pushButton_v3_enviar.clicked.connect(self.start_v3)

# Update do valor das válvulas

    def start_v1(self):
        self.control.valvula1 = self.spinBox_v1.value()
        self.control.temp_valor = self.spinBox_v1.value()
        thread = threading.Thread(target=self.control.update_valve)
        thread.start()

    def start_v2(self):
        self.control.valvula2 = self.spinBox_v2.value()
        self.control.temp_valor = self.spinBox_v2.value()
        thread = threading.Thread(target=self.control.update_valve)
        self.setar_evento()
        thread.start()

    def start_v3(self):
        self.control.valvula3 = self.spinBox_v3.value()
        self.control.temp_valor = self.spinBox_v3.value()
        thread = threading.Thread(target=self.control.update_valve)
        self.setar_evento()
        thread.start()

# Update dos ícones de interface

    def update_valves(self):
        get_valve = self.control.update_screen_valve1()
        self.progressBar_v1.setValue(get_valve)
        time.sleep(0.1)
        get_valve = self.control.update_screen_valve2()
        self.progressBar_v2.setValue(get_valve)
        time.sleep(0.1)
        get_valve = self.control.update_screen_valve3()
        self.progressBar_v3.setValue(get_valve)

    def update_tanques(self):
        get_t1 = self.control.update_tanque1()
        self.progressBar_t1.setValue(get_t1)
        time.sleep(0.1)
        texto = str(get_t1)
        self.lineEdit_t1.setText(texto)
        time.sleep(0.1)
        get_t2 = self.control.update_tanque2()
        self.progressBar_t2.setValue(get_t2)
        time.sleep(0.1)
        texto = str(get_t2)
        self.lineEdit_t2.setText(texto)

    def update_mix(self):
        if self.radioButton_on.isChecked():
            texto = self.control.update_mix_on()
            self.lineEdit_mix.setText(texto)
        else:
            texto = self.control.update_mix_off()
            self.lineEdit_mix.setText(texto)

    def update_alertas(self):
        get_t1 = self.control.alerta_tanque1()
        self.lineEdit_alt1.setText(get_t1)
        time.sleep(0.1)
        get_t2 = self.control.alerta_tanque2()
        self.lineEdit_alt2.setText(get_t2)

# Método para atualização da tela, com evento        

    def update_screen(self):
        while 1:
            evento.wait()
            semaforo.acquire()
            self.update_valves()
            self.update_tanques()
            self.update_alertas()
            self.update_mix()
            self.inicia_tela = 0
            semaforo.release()

# Método para setar o evento            

    def setar_evento(self):
        evento.set()
        evento.clear()

# Método para verificar se algo foi alterado        

    def update(self):
        while 1:
            time.sleep(1)
            semaforo.acquire()
            if self.inicia_tela == 1:
                self.setar_evento()
            if self.control.update_tanque1() != 0 or self.control.update_tanque2() != 0:
                self.setar_evento()
            self.radioButton_on.clicked.connect(self.setar_evento)
            self.radioButton_off.clicked.connect(self.setar_evento)
            semaforo.release()


def main():
    app = QtGui.QApplication(sys.argv)
    app.setStyle('cleanlooks')
    form = tela()
    form.show()
    app.exec_()

if __name__ == '__main__':
    main()
