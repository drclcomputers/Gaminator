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
vieti=5

astex=[10, 50, 90, 130, 170]
astey=[25, 25, 25, 25, 25]

astex2=[10, 50, 90, 130, 170]
astey2=[55, 55, 55, 55, 55]

astex3=[10, 50, 90, 130, 170]
astey3=[85, 85, 85, 85, 85]

ziduri=[10, 60, 110, 160, 210]

glx=[]
gly=[]

bool1=False
bool2=False
bool3=False

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
        #controls
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
        
        #glont
        for i in range(glont):
            i=int(i)
            if glont>0:
                LCD.rect(pozx, pozy, 10, 10, LCD.red)
                pozy-=10
                if pozy<=10:
                    glont=0
                    pozx=0
                    pozy=0
                                        
        #desenat figuri + aparare proiectile
        if len(astey)!=0:
            for i in range(len(astey)):
                LCD.rect(astex[i], astey[i], 20, 20, LCD.white)
            for j in range(len(astey2)):
                LCD.rect(astex2[j], astey2[j], 20, 20, LCD.white)
            for k in range(len(astey3)):
                LCD.rect(astex3[k], astey3[k], 20, 20, LCD.white)
        
        #artilerie
        if aux<=9:
            aux+=0.4
            if aux>=9:
                if len(astex3)!=0:
                    glx.append(random.choice(astex3)+10)
                    gly.append(105)
                elif len(astex2)!=0:
                    glx.append(random.choice(astex2)+10)
                    gly.append(75)
                elif len(astex)!=0:
                    glx.append(random.choice(astex)+10)
                    gly.append(35)
                aux=0
        
        if len(glx)!=0:
            for i in range(len(glx)):
                if len(glx)!=0:
                    i-=1
                    LCD.rect(glx[i], gly[i], 10, 10, LCD.white)
                    gly[i]+=5
                    for j in range(len(ziduri)):
                        j-=1
                        if glx[i]>=ziduri[j] and glx[i]<=ziduri[j]+20 and gly[i]>=160:
                            glx.pop(i)
                            gly.pop(i)
                            break
                        elif glx[i]<xa and glx[i]>xa and gly[i]>220:
                            glx.pop(i)
                            gly.pop(i)
                            break
                        elif glx[i]>=xa and glx[i]<=xa+30 and gly[i]>=210:
                            vieti-=1
                            glx=[]
                            gly=[]
                            pozx=0
                            pozy=0
                            astex=[10, 50, 90, 130, 170]
                            astey=[25, 25, 25, 25, 25]
                            astex2=[10, 50, 90, 130, 170]
                            astey2=[55, 55, 55, 55, 55]
                            astex3=[10, 50, 90, 130, 170]
                            astey3=[85, 85, 85, 85, 85]
                            xa=100
                            break
        
        
        #no siluete
        if len(astex)==0 and len(astex2)==0 and len(astex3)==0:
            astex=[10, 50, 90, 130, 170]
            astey=[25, 25, 25, 25, 25]
            astex2=[10, 50, 90, 130, 170]
            astey2=[55, 55, 55, 55, 55]
            astex3=[10, 50, 90, 130, 170]
            astey3=[85, 85, 85, 85, 85]
            if vieti==5:
                score+=20
            elif vieti==4:
                score+=10
            elif vieti==3:
                score+=5
            elif vieti==2:
                score+=2
            elif vieti==1:
                score+=1
        
        #ziduri      
        if pozx>=10 and pozx<=30 and pozy<=160:
            glont-=1
            pozx=0
            pozy=0
        elif pozx>=60 and pozx<=80 and pozy<=160:
            glont-=1
            pozx=0
            pozy=0
        elif pozx>=110 and pozx<=130 and pozy<=160:
            glont-=1
            pozx=0
            pozy=0
        elif pozx>=160 and pozx<=180 and pozy<=160:
            glont-=1
            pozx=0
            pozy=0
        elif pozx>=210 and pozx<=230 and pozy<=160:
            glont-=1
            pozx=0
            pozy=0
        
        #lovit
        if len(astey)!=0:
            for m in range(len(astex)):
                if len(astex)!=0:
                    m-=1
                    if pozx>=astex[m] and pozx<=astex[m]+20 and pozy<=45 and pozy>=25:
                        score+=1
                        astex.pop(m)
                        astey.pop(m)
                        glont-=1
                        pozx=0
                        pozy=0
                        break
        if len(astey2)!=0:
            for n in range(len(astex2)):
                if len(astex2)!=0:
                    n-=1
                    if pozx>=astex2[n] and pozx<=astex2[n]+20 and pozy<=75 and pozy>=55:
                        score+=1
                        astex2.pop(n)
                        astey2.pop(n)
                        glont-=1
                        pozx=0
                        pozy=0
                        break
        if len(astey3)!=0:
            for p in range(len(astex3)):
                if len(astex3)!=0:
                    p-=1
                    if pozx>=astex3[p] and pozx<=astex3[p]+20 and pozy<=105 and pozy>=85:
                        score+=1
                        astex3.pop(p)
                        astey3.pop(p)
                        glont-=1
                        pozx=0
                        pozy=0
                        break
        #miscat siluete    
        for m in range(len(astex)):
            if bool1==False:
                astex[m]+=1
            else:
                astex[m]-=1
            if astex[-1]>=220:
                bool1=True
            if astex[0]<10:
                bool1=False
        for n in range(len(astex2)):
            if bool2==False:
                astex2[n]+=1
            else:
                astex2[n]-=1
            if astex2[-1]>=220:
                bool2=True
            if astex2[0]<10:
                bool2=False
        for p in range(len(astex3)):
            if bool3==False:
                astex3[p]+=1
            else:
                astex3[p]-=1
            if astex3[-1]>=220:
                bool3=True
            if astex3[0]<10:
                bool3=False
                
        #pereti        
        for i in range(len(ziduri)):
            LCD.rect(ziduri[i-1], 160, 20, 20, LCD.green)
            
        #dead        
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
                    vieti=5
                    score=0
                    astex=[10, 50, 90, 130, 170]
                    astey=[25, 25, 25, 25, 25]
                    astex2=[10, 50, 90, 130, 170]
                    astey2=[55, 55, 55, 55, 55]
                    astex3=[10, 50, 90, 130, 170]
                    astey3=[85, 85, 85, 85, 85]
                    aux=0
                    glx=[]
                    gly=[]
                    xa=100
                    break
                if keyX.value()==0:
                    machine.reset()
        
        LCD.rect(xa, 230, 30, 10, LCD.blue)
        LCD.fill_rect(xa, 230, 30, 10, LCD.blue)
        LCD.rect(xa+10, 220, 10, 10, LCD.blue)
        LCD.fill_rect(xa+10, 220, 10, 10, LCD.blue)
        
        LCD.text(("Score: "+str(score)), 160, 10, LCD.white)
        
        #vieti
        for i in range(vieti):
            LCD.rect(i*20, 5, 10, 10, LCD.green)
            LCD.fill_rect(i*20, 5, 10, 10, LCD.green)
        
        LCD.show()
        LCD.fill(LCD.black)



