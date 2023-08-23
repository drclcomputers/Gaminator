from machine import Pin,SPI,PWM
import framebuf
import time
import os
import random

BL = 13
DC = 8
RST = 12
MOSI = 11
SCK = 10
CS = 9


class LCD_1inch3(framebuf.FrameBuffer):
    def __init__(self):
        self.width = 240
        self.height = 240
        
        self.cs = Pin(CS,Pin.OUT)
        self.rst = Pin(RST,Pin.OUT)
        
        self.cs(1)
        self.spi = SPI(1)
        self.spi = SPI(1,1000_000)
        self.spi = SPI(1,100000_000,polarity=0, phase=0,sck=Pin(SCK),mosi=Pin(MOSI),miso=None)
        self.dc = Pin(DC,Pin.OUT)
        self.dc(1)
        self.buffer = bytearray(self.height * self.width * 2)
        super().__init__(self.buffer, self.width, self.height, framebuf.RGB565)
        self.init_display()
        
        self.red   =   0x07E0
        self.green =   0x001f
        self.blue  =   0xf800
        self.white =   0xffff
        self.black =   000000
        
    def write_cmd(self, cmd):
        self.cs(1)
        self.dc(0)
        self.cs(0)
        self.spi.write(bytearray([cmd]))
        self.cs(1)

    def write_data(self, buf):
        self.cs(1)
        self.dc(1)
        self.cs(0)
        self.spi.write(bytearray([buf]))
        self.cs(1)

    def init_display(self):
        """Initialize dispaly"""  
        self.rst(1)
        self.rst(0)
        self.rst(1)
        
        self.write_cmd(0x36)
        self.write_data(0x70)

        self.write_cmd(0x3A) 
        self.write_data(0x05)

        self.write_cmd(0xB2)
        self.write_data(0x0C)
        self.write_data(0x0C)
        self.write_data(0x00)
        self.write_data(0x33)
        self.write_data(0x33)

        self.write_cmd(0xB7)
        self.write_data(0x35) 

        self.write_cmd(0xBB)
        self.write_data(0x19)

        self.write_cmd(0xC0)
        self.write_data(0x2C)

        self.write_cmd(0xC2)
        self.write_data(0x01)

        self.write_cmd(0xC3)
        self.write_data(0x12)   

        self.write_cmd(0xC4)
        self.write_data(0x20)

        self.write_cmd(0xC6)
        self.write_data(0x0F) 

        self.write_cmd(0xD0)
        self.write_data(0xA4)
        self.write_data(0xA1)

        self.write_cmd(0xE0)
        self.write_data(0xD0)
        self.write_data(0x04)
        self.write_data(0x0D)
        self.write_data(0x11)
        self.write_data(0x13)
        self.write_data(0x2B)
        self.write_data(0x3F)
        self.write_data(0x54)
        self.write_data(0x4C)
        self.write_data(0x18)
        self.write_data(0x0D)
        self.write_data(0x0B)
        self.write_data(0x1F)
        self.write_data(0x23)

        self.write_cmd(0xE1)
        self.write_data(0xD0)
        self.write_data(0x04)
        self.write_data(0x0C)
        self.write_data(0x11)
        self.write_data(0x13)
        self.write_data(0x2C)
        self.write_data(0x3F)
        self.write_data(0x44)
        self.write_data(0x51)
        self.write_data(0x2F)
        self.write_data(0x1F)
        self.write_data(0x1F)
        self.write_data(0x20)
        self.write_data(0x23)
        
        self.write_cmd(0x21)

        self.write_cmd(0x11)

        self.write_cmd(0x29)

    def show(self):
        self.write_cmd(0x2A)
        self.write_data(0x00)
        self.write_data(0x00)
        self.write_data(0x00)
        self.write_data(0xef)
        
        self.write_cmd(0x2B)
        self.write_data(0x00)
        self.write_data(0x00)
        self.write_data(0x00)
        self.write_data(0xEF)
        
        self.write_cmd(0x2C)
        
        self.cs(1)
        self.dc(1)
        self.cs(0)
        self.spi.write(self.buffer)
        self.cs(1)
        

xa=100
aux=0
glont=0
pozx=0
pozy=0
score=0
run=True
vieti=3
astex=[]
astey=[]

if __name__=='__main__':
    pwm = PWM(Pin(BL))
    pwm.freq(1000)
    pwm.duty_u16(32768)#max 65535

    LCD = LCD_1inch3()

    keyA = Pin(15,Pin.IN,Pin.PULL_UP)
    keyB = Pin(17,Pin.IN,Pin.PULL_UP)
    keyX = Pin(19 ,Pin.IN,Pin.PULL_UP)
    keyY= Pin(21 ,Pin.IN,Pin.PULL_UP)
    
    up = Pin(2,Pin.IN,Pin.PULL_UP)
    down = Pin(18,Pin.IN,Pin.PULL_UP)
    left = Pin(16,Pin.IN,Pin.PULL_UP)
    right = Pin(20,Pin.IN,Pin.PULL_UP)
    ctrl = Pin(3,Pin.IN,Pin.PULL_UP)
    
    while run==True:
        
        if aux<=9:
            aux+=0.5
            if aux==9:
                astex.append(random.randint(0, 219))
                astey.append(0)
                aux=0
        
        if right.value()==0:
            if xa+20<229:
                xa+=5
        if left.value()==0:
            if xa>1:
                xa-=5
        if keyX.value()==0:
            LCD.text("Exiting", 90, 100, LCD.red)
            LCD.show()
            time.sleep(1.5)
            run=False
            machine.reset()
        if keyA.value()==0:
            if glont==0:
                pozx=xa+10
                pozy=220
                glont+=1
        
        for i in range(glont):
            i=int(i)
            if glont>0:
                LCD.rect(pozx, pozy, 10, 10, LCD.red)
                pozy-=15
                if pozy<10:
                    if glont>0:
                        glont-=1
                                        
        if len(astey)!=0:
            for i in range(len(astey)):
                LCD.rect(astex[i], astey[i], 20, 20, LCD.white)
                astey[i]+=1
                if astey[0]>=220 and astex[0]<=xa and astex[0]+10>=xa+30:
                    astex.pop(0)
                    astey.pop(0)
                    break
                if astey[i]<=240 and astey[i]>=220 and astex[i]+20>=xa and astex[i]<=xa+30:
                    vieti-=1
                    astex=[]
                    astey=[]
                    xa=100
                    break
                if pozx>=astex[i] and pozx<=astex[i]+20 and pozy<=astey[i]:
                    score+=1
                    glont=0
                    astex.pop(i)
                    astey.pop(i)
                    break
                
        if vieti==0:
            LCD.fill(0)
            LCD.text("Game over!", 80, 80, LCD.red)
            LCD.text("Press B to restart, X to exit.", 2, 100, LCD.red)
            LCD.text(("Score: "+str(score)), 80, 120, LCD.red)
            LCD.show()
            run=False
            while True:
                if keyB.value()==0:
                    run=True
                    vieti=3
                    score=0
                    astex=[]
                    astey=[]
                    xa=100
                    break
                if keyX.value()==0:
                    machine.reset()
        
        LCD.rect(xa, 230, 30, 10, LCD.blue)
        LCD.fill_rect(xa, 230, 30, 10, LCD.blue)
        LCD.rect(xa+10, 220, 10, 10, LCD.blue)
        LCD.fill_rect(xa+10, 220, 10, 10, LCD.blue)
        
        LCD.text(("Score: "+str(score)), 160, 10, LCD.white)
        for i in range(vieti):
            LCD.rect(i*20, 5, 10, 10, LCD.green)
            LCD.fill_rect(i*20, 5, 10, 10, LCD.green)
        
        LCD.show()
        LCD.fill(LCD.black)
        #time.sleep(1/60)








