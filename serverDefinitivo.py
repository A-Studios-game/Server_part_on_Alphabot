#!/usr/bin/python
# _*_ coding: utf-8 _*_
#server tpc

import socket as sck
import threading as thr
#sck e thr altri modi per richiamare le librerie socket e threading
import time
import RPi.GPIO as GPIO
import sqlite3 #libreria data base

lista_client = []

#classe thread

#funzione che si avvia alla creazione della classe
def __init__(self, connessione, indirizzo ,alphabot):
    thr.Thread.__init__(self)   #costruttore super (java)
    self.connessione = connessione
    self.indirizzo=indirizzo
    self.alphabot=alphabot          #per usare la classe del robot all'interno del thread
    self.running = True


class AlphaBot(object):  #classe dell'Alfabot
    
    def __init__(self, in1=13, in2=12, ena=6, in3=21, in4=20, enb=26):
        self.IN1 = in1
        self.IN2 = in2
        self.IN3 = in3
        self.IN4 = in4
        self.ENA = ena
        self.ENB = enb
        self.PA  = 20  #velocità in girare
        self.PB  = 20   #velocità per girare


        #avvio motori
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        GPIO.setup(self.IN1, GPIO.OUT)
        GPIO.setup(self.IN2, GPIO.OUT)
        GPIO.setup(self.IN3, GPIO.OUT)
        GPIO.setup(self.IN4, GPIO.OUT)
        GPIO.setup(self.ENA, GPIO.OUT)
        GPIO.setup(self.ENB, GPIO.OUT)
        self.PWMA = GPIO.PWM(self.ENA,500)
        self.PWMB = GPIO.PWM(self.ENB,500)
        self.PWMA.start(self.PA)
        self.PWMB.start(self.PB)
        self.stop()

    #metodo che muove le ruote indietro a velocità costante 
    def backward(self, speed=60):  #indietro a velocità 60
        self.PWMA.ChangeDutyCycle(speed) #attiva la fase ON in entrambi i motori in modo da far muovere l'alphabot
        self.PWMB.ChangeDutyCycle(speed)
        GPIO.output(self.IN1, GPIO.HIGH)
        GPIO.output(self.IN2, GPIO.LOW)
        GPIO.output(self.IN3, GPIO.LOW)
        GPIO.output(self.IN4, GPIO.HIGH)


    #metodo che ferma le ruote
    def stop(self):     #fermare i motori
        self.PWMA.ChangeDutyCycle(0) #attiva la fase OFF in entrambi i motori in modo da fermare l'alphabot
        self.PWMB.ChangeDutyCycle(0)
        GPIO.output(self.IN1, GPIO.LOW)
        GPIO.output(self.IN2, GPIO.LOW)
        GPIO.output(self.IN3, GPIO.LOW)
        GPIO.output(self.IN4, GPIO.LOW)

    #metodo che fa muovere entrambe le ruote in avanti
    def forward(self , speed = 60):   #avanti velocità 60
        self.PWMA.ChangeDutyCycle(speed) #attiva la fase ON in entrambi i motori in modo da far muovere l'alphabot
        self.PWMB.ChangeDutyCycle(speed)
        GPIO.output(self.IN1, GPIO.LOW)
        GPIO.output(self.IN2, GPIO.HIGH)
        GPIO.output(self.IN3, GPIO.HIGH)
        GPIO.output(self.IN4, GPIO.LOW)
        
        
    #metodo che fa muovere il robot a sinistra
    def left(self, speed = 25):     #girare a sinistra con velocità 25
        self.PWMA.ChangeDutyCycle(speed) #attiva la fase ON in entrambi i motori in modo da far muovere l'alphabot
        self.PWMB.ChangeDutyCycle(speed)
        GPIO.output(self.IN1, GPIO.LOW)
        GPIO.output(self.IN2, GPIO.HIGH)
        GPIO.output(self.IN3, GPIO.LOW)
        GPIO.output(self.IN4, GPIO.HIGH)
    
    #metodo che fa muovere il robot a destra
    def right(self, speed = 25):    #girare a destra con velocità 25
        self.PWMA.ChangeDutyCycle(speed) #attiva la fase ON in entrambi i motori in modo da far muovere l'alphabot
        self.PWMB.ChangeDutyCycle(speed)
        GPIO.output(self.IN1, GPIO.HIGH)
        GPIO.output(self.IN2, GPIO.LOW)
        GPIO.output(self.IN3, GPIO.HIGH)
        GPIO.output(self.IN4, GPIO.LOW)
        
    def set_pwm_a(self, value):
        self.PA = value
        self.PWMA.ChangeDutyCycle(self.PA)

    def set_pwm_b(self, value):
        self.PB = value
        self.PWMB.ChangeDutyCycle(self.PB)    
        
    #funzione che inizializza i motori
    def set_motor(self, left, right):
        if (right >= 0) and (right <= 100):
            GPIO.output(self.IN1, GPIO.HIGH)
            GPIO.output(self.IN2, GPIO.LOW)
            self.PWMA.ChangeDutyCycle(right)
        elif (right < 0) and (right >= -100):
            GPIO.output(self.IN1, GPIO.LOW)
            GPIO.output(self.IN2, GPIO.HIGH)
            self.PWMA.ChangeDutyCycle(0 - right)
        if (left >= 0) and (left <= 100):
            GPIO.output(self.IN3, GPIO.HIGH)
            GPIO.output(self.IN4, GPIO.LOW)
            self.PWMB.ChangeDutyCycle(left)
        elif (left < 0) and (left >= -100):
            GPIO.output(self.IN3, GPIO.LOW)
            GPIO.output(self.IN4, GPIO.HIGH)
            self.PWMB.ChangeDutyCycle(0 - left)

def main():
    s = sck.socket(sck.AF_INET, sck.SOCK_STREAM) #creazione socket
    s.bind(('0.0.0.0', 3450))       #bind del server tcp
    s.listen()
    Ab= AlphaBot()      #inizzializzo alphabot

    running = True
    print(f"in ascolto\n")
    connessione, indirizzo = s.accept()   #connessioni dei client
    print("connesso\n")

    while running:     #ciclo infinito del programma
        messaggio = (connessione.recv(4096)).decode()          #ricevo il comando
        #print("eccomi\n")
        if messaggio == 'exit':             #per chiudere il programma e scollegare il client
            running = False

            lista_client.remove()
            
        else:
            print(messaggio)
            #a seconda del messaggio ricevuto esegue una certa azione        
            if messaggio.upper().startswith("L"): #"L"=Left
                Ab.left()
                time.sleep(0.5)        #durata del movimento
                Ab.stop()
            if messaggio.upper().startswith("R"): #"R"=Right
                Ab.right()
                time.sleep(0.5)   
                Ab.stop()
            if messaggio.upper().startswith("F"): #"F"=Forward
                Ab.forward()
                time.sleep(0.5)   
                Ab.stop()
            if messaggio.upper().startswith("ESCI"): #uscita dal ciclo = stop
                Ab.stop()

    s.close() #conclusione della connessione


if __name__ == "__main__":
    main()
