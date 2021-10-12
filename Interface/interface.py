# ================================================
# Serial comunication with RS-232 
# and this interface used by tkinter module 
# because, this module comes with python download
# 
# Reading sensor LM35 and blynk leds on pic16f877a
# Plus convert celsius in kelvin and fahrenheit
# 
# Close the serial port before desconnecting
# the serial circuit
#
# Comunicação serial com rs-232, e utilizando interface tkinter
# que já vem com a instalação do python 
#
# Leitura do sensor LM35 e liga/desliga leds
# LM35 é um sensor de temperatura em °C e nessa aplicação 
# está ocorrendo a conversão em kelvin e fahrenheit
# ================================================

# import serial
from tkinter import *
from tkinter import ttk
from tkinter import messagebox

# colors
colors = [
    '#fff',
    '#000',
    '#f64740',
    '#558b6e',
    '#100b00',
]

class Application:
    
    def __init__(self, root=None):
        
        # title 
        self.title = Label(root, text='Testing via Serial', bg=colors[4], font='Arial 15', fg='white').pack()

        self.config = Frame(root, bg=colors[4], relief='groove')
        self.config.place(relwidth=0.90, relheight=0.3, relx=0.02, rely=0.1)

        # Titulo da tela
        self.titleconfig = Label(self.config, text='Configuration Serial', font="Arial 12", bg=colors[4], fg='#fff')
        self.titleconfig.place(x=0, y=0)

        self.port = Label(self.config, text='Port(COM)', font='Arial 10', bg=colors[4], fg='white').place(x=5, y=30)

        self.gate = ttk.Combobox(self.config, width=10)
        self.gate["values"] = ['COM1', 'COM2', 'COM3', 'COM4', 'COM5', 'COM6', 'COM7']
        self.gate.place(x=5, y=50)
        
        self.rate = Label(self.config, text='Baud Rate', font='Arial 10', bg=colors[4], fg='white').place(x=120,y=30)
        
        self.baud = ttk.Combobox(self.config, width=10)
        self.baud["values"] = ['NONE', 50, 110, 300, 1200, 2400, 4800, 9600, 19200, 38400, 57600]
        self.baud.place(x=120, y=50)
        
        self.button_ok = Button(self.config, text='OK', width=8, command=self.ok).place(x=270, y=20)
        self.button_cancel = Button(self.config, text='CANCEL', width=8, command=self.cancel).place(x=270, y=50)

        self.led = Label(root, text='Testing Led', bg=colors[4], fg='white', font='Calibri 11')
        self.led.place(x=35, y=130)

        # Botões para ligar e desligar o led
        self.button_on = Button(root, text='ON', width=5, bg=colors[3], fg=colors[0],command=self.on)
        self.button_on.place(x=20, y=170)

        self.button_off = Button(root, text='OFF', width=5, bg=colors[2], fg=colors[0], command=self.off)
        self.button_off.place(x=80, y=170)

        self.temp_label = Label(root, text='Testing Sensor(LM35)',bg=colors[4], fg='white', font='Calibri 11')
        self.temp_label.place(x=180,y=130)
      
        # Barras de progresso para leitura dos sensores
        self.tempc = ttk.Progressbar(root, length=80, orient='vertical', maximum=150)
        self.tempc.place(x=175,y=180)

        self.tc = Label(root, text='°C', bg=colors[4], fg='white')
        self.tc.place(x=200,y=160)

        self.tempf = ttk.Progressbar(root, length=80, orient='vertical', maximum=302)
        self.tempf.place(x=235,y=180)

        self.tf = Label(root, text='°F', bg=colors[4], fg='white')
        self.tf.place(x=260,y=160)

        self.tempk = ttk.Progressbar(root, length=80, orient='vertical', maximum=423)
        self.tempk.place(x=295,y=180)

        self.tk = Label(root, text='K', bg=colors[4], fg='white')
        self.tk.place(x=320,y=160)

        # Botão para iniciar leitura do sensor 
        self.sensor_button = Button(root, text='READ', width=5, command=self.sensor)
        self.sensor_button.place(x=340,y=130)

        # Labels de temperatura embaixo das barras
        self.look_tc = Label(root, text='', bg=colors[4], fg='white')
        self.look_tc.place(x=175,y=260)

        self.look_tf = Label(root, text='', bg=colors[4], fg='white')
        self.look_tf.place(x=230,y=260)

        self.look_tk = Label(root, text='', bg=colors[4], fg='white')
        self.look_tk.place(x=292,y=260)

    # Open port and initial comunication   
    # Abrindo a porta e iniciando assim a comunicação    
    def ok(self):
        try:
            self.g = self.gate.get() # Select gate
            self.r = self.baud.get() # Select baud rate
        
            self.pic = serial.Serial(self.g, self.r)
        
            print(self.pic.isOpen())

            messagebox.showinfo("Open PORT", f"OPEN PORT {self.pic.name}")

            

        except serial.SerialException:
            print("Error to conection on port")

    # Close port  
    # Fechar a porta 
    def cancel(self):
        try:
            self.gate.delete(0, 'end')
            self.baud.delete(0 ,'end')
            self.pic.close()

            print(f'Close Port({self.pic.name})')

            messagebox.showinfo("Close port", f"CLOSE PORT {self.pic.name}")

            self.tempc['value'] = 0
            self.tempf['value'] = 0
            self.tempk['value'] = 0

            self.look_tc['text'] = ''
            self.look_tf['text'] = ''
            self.look_tk['text'] = ''

        except:
            print("The door isn't open")
         
    # Envia para o pic o carater 1 e ligar o led
    def on(self): 
        self.pic.write(b'1')

    # Envia para o pic o carater 2 e desliga o led       
    def off(self):
        self.pic.write(b'2')

    # Função que vai colocar nas barras de progresso a temperatura e converter em (°F e K)    
    def sensor(self):
        try:
            self.celsius = int(self.pic.readline().decode('ascii'))
            
            self.tempc['value'] = self.celsius

            self.fah = ((self.celsius *9)/5) + 32
            self.kel = self.celsius + 273

            self.tempf['value'] = self.fah
            self.tempk['value'] = self.kel

            self.look_tc['text'] = self.celsius
            self.look_tf['text'] = self.fah
            self.look_tk['text'] = self.kel

            print(f'Temp:{self.celsius}°C')
                      
        except serial.SerialException:
            print(f"The port({self.pic.name}) is close.Then it is impossible read the sensor")
 
        root.after(1000, self.sensor) # depois de 1000ms = 1s ela repeti a leitura como se atualizasse automatico 

root = Tk()
root.title("Test Serial")
root.configure(bg=colors[4])
root.geometry("420x300")
root.resizable(width=0, height=0) # tela tamanho constante
APP = Application(root)
root.mainloop()