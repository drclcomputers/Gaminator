from machine import Pin,SPI,PWM
import framebuf
import time
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
        self.brown = 521200

        
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

run=True
aux=0
naux=0
score=0
vieti=3
xp=115
yp=100
orientare=True
glx=[]
gly=[]
glo=[]
zomx=[]
zomy=[]
zomo=[]

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
        if aux<=6:
            aux+=0.5
            if aux>=6:
                zomy.append(random.randint(25, 210))
                naux=random.randint(0, 1)
                if naux==0:
                    zomx.append(0)
                    zomo.append(False)
                else:
                    zomx.append(240)
                    zomo.append(True)
                aux=0
        
        if up.value()==0:
            if yp>=25:
                yp-=5
        if down.value()==0:
            if yp<210:
                yp+=5
        if right.value()==0:
            if xp<215:
                xp+=5
        if left.value()==0:
            if xp>5:
                xp-=5
        if keyB.value()==0:
            if orientare==True:
                orientare=False
                time.sleep(0.1)
            else:
                orientare=True
                time.sleep(0.2)
        if keyA.value()==0:
            glx.append(xp)
            gly.append(yp+10)
            glo.append(orientare)
        if keyX.value()==0:
            LCD.text("Exiting", 90, 100, LCD.red)
            LCD.show()
            time.sleep(1.5)
            run=False
            machine.reset()
            
        for i in range(len(glx)):
            i-=1
            if len(glo)!=0:  
                if glo[i]==True:
                    if len(glx)!=0:
                        if glx[i]>=240:
                            glx.pop(i)
                            gly.pop(i)
                            glo.pop(i)
                            break
                        for y in range(len(zomx)):
                            y-=1
                            if len(zomx)!=0:
                                if glx[i]>=zomx[y] and glx[i]<=zomx[y]+10 and gly[i]>=zomy[y] and gly[i]<=zomy[y]+30:
                                    score+=1
                                    glx.pop(i)
                                    gly.pop(i)
                                    glo.pop(i)
                                    zomx.pop(y)
                                    zomy.pop(y)
                                    zomo.pop(y)
                                    break
                else:
                    if len(glx)!=0:
                        if glx[i]<=0:
                            glx.pop(i)
                            gly.pop(i)
                            glo.pop(i)
                            break
                        for y in range(len(zomx)):
                            y-=1
                            if len(zomx)!=0:
                                if glx[i]>=zomx[y] and glx[i]<=zomx[y]+10 and gly[i]>=zomy[y] and gly[i]<=zomy[y]+30:
                                    score+=1
                                    glx.pop(i)
                                    gly.pop(i)
                                    glo.pop(i)
                                    zomx.pop(y)
                                    zomy.pop(y)
                                    zomo.pop(y)
                                    break
                        
            
        for i in range(len(glx)):
            i-=1
            if glo[i]==True:
                if len(glx)!=0:
                    glx[i]+=10
                    LCD.rect(glx[i], gly[i], 5, 5, LCD.red)
                    LCD.fill_rect(glx[i], gly[i], 5, 5, LCD.red)  
            else:
                if len(glx)!=0:
                    glx[i]-=10
                    LCD.rect(glx[i], gly[i], 5, 5, LCD.red)
                    LCD.fill_rect(glx[i], gly[i], 5, 5, LCD.red)  
                    
        for i in range(len(zomx)):
            i-=1
            if len(zomo)!=0:
                if zomo[i]==True:
                    zomx[i]-=5
                    if zomx[i]<=0:
                        zomx.pop(i)
                        zomy.pop(i)
                        zomo.pop(i)
                        break
                    if (zomx[i]>=xp-5 and zomx[i]<=xp+15) and ((zomy[i]>=yp and zomy[i]<=yp+30) or (yp>=zomy[i] and yp<=zomy[i]+30)):
                                vieti-=1
                                aux=0
                                naux=0
                                xp=115
                                yp=100
                                orientare=True
                                glx=[]
                                gly=[]
                                glo=[]
                                zomx=[]
                                zomy=[]
                                zomo=[]
                else:
                    zomx[i]+=5
                    if zomx[i]>=230:
                        zomx.pop(i)
                        zomy.pop(i)
                        zomo.pop(i)
                        break
                    if (zomx[i]>=xp-5 and zomx[i]<=xp+15) and ((zomy[i]>=yp and zomy[i]<=yp+30) or (yp>=zomy[i] and yp<=zomy[i]+30)):
                                vieti-=1
                                aux=0
                                naux=0
                                xp=115
                                yp=100
                                orientare=True
                                glx=[]
                                gly=[]
                                glo=[]
                                zomx=[]
                                zomy=[]
                                zomo=[]
                    
        for i in range(len(zomx)):
            i-=1
            LCD.rect(zomx[i], zomy[i], 10, 30, LCD.green)
            LCD.fill_rect(zomx[i], zomy[i], 10, 30, LCD.green)
            LCD.rect(zomx[i], zomy[i]+10, 10, 20, LCD.red)
            LCD.fill_rect(zomx[i], zomy[i]+10, 10, 20, LCD.red)
            
        
        LCD.rect(xp, yp, 10, 30, LCD.white)
        LCD.fill_rect(xp, yp, 10, 30, LCD.white)
        LCD.rect(xp, yp+10, 10, 20, LCD.blue)
        LCD.fill_rect(xp, yp+10, 10, 20, LCD.blue)
        if orientare==True:
            LCD.rect(xp, yp+10, 20, 5, LCD.red)
            LCD.fill_rect(xp, yp+10, 20, 5, LCD.red)
        else:
            LCD.rect(xp-10, yp+10, 20, 5, LCD.red)
            LCD.fill_rect(xp-10, yp+10, 20, 5, LCD.red)
            
        if vieti==0:
            LCD.fill(0)
            LCD.text("Game over!", 80, 80, LCD.red)
            LCD.text("Press A to restart, X to exit.", 2, 100, LCD.red)
            LCD.text(("Score: "+str(score)), 80, 120, LCD.red)
            LCD.show()
            run=False
            while True:
                if keyA.value()==0:
                    run=True
                    vieti=3
                    score=0
                    astex=[]
                    astey=[]
                    xa=100
                    break
                if keyX.value()==0:
                    machine.reset()
            
        LCD.text(("Score: "+str(score)), 160, 10, LCD.brown)
        for i in range(vieti):
            LCD.rect(i*20, 5, 10, 10, LCD.brown)
            LCD.fill_rect(i*20, 5, 10, 10, LCD.brown)
        
        LCD.show()
        LCD.fill(LCD.black)
        time.sleep(0.05)
        








