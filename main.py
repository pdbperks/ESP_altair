# main.py executes after boot.py
# this file for altair emulator
#@pdbperks 2020
#
from time import sleep 
from gc import collect
from ir_rx.print_error import print_error  # Optional print of error codes
from ir_rx.nec import NEC_8
#import ssd1306
from ssd1306 import SSD1306_I2C
from machine import Pin, freq, I2C, reset
i2c=I2C(scl=Pin(2),sda=Pin(0))
oled = SSD1306_I2C(128,64,i2c)
freq(160000000)
p = Pin(14, Pin.IN)  #pin for IR sensor

#altair variables
databyte = "00000000"
octobyte = [0,0,0]
octx = 0
memory = [0 for x in range(256)]
sampleprogram = [58,128,0,71,58,129,0,128,50,130,0]
prog = bytearray([
    0x3A,0x0C,0x0,0x47,0x3A,0x0D,0x0,0x80,
    0x32,0x0F,0x0,0x76,0x01,0x02,0x04,0x0,
    0x3A,0x0E,0x0,0x4F,0x3C,0x0D,0xC2,0x14,
    0x0,0x32,0x0F,0x0,0x76
    ])
pc = 0  #program counter
tr = False   #show acc value
zf = True   #zero flag
menu = False #menu toggle


oled.text('Octal 8bit I8080',0,0)
oled.text('Altair simulator',0,10)
oled.show()


def cleanup():
    global databyte, databyte, octobyte, octx
    octobyte = [0,0,0]
    octx = 0
    databyte = "00000000"
    dataShow()

#write databyte to data display
def dataWrite():
    global octobyte, octx, databyte
    octx =(octx+1)%3
    if octx==1: # reset octobyte
        octobyte[1] = 0 
        octobyte[2] = 0 
    p = (octobyte[0]&3)*0o100  + octobyte[1]*0o10 + octobyte[2]
    databyte = bin00(p)
    dataShow()

def dataShow():
    oled.fill_rect(0, 40, 128, 10, 0)
    oled.text('Data:',0,40)
    oled.text(databyte,50,40)
    oled.show() 


#write program counter to address display
def pcWrite():
    global octobyte, octx, databyte,  pc
    db = bin00(pc)
    oled.fill_rect(0, 30, 128, 10, 0)
    oled.text('Addr:',0,30)
    oled.text(db,50,30)
    oled.show()

def bin00(dec):
    bin0 = "00000000" #[0 for x in range(8)] "00000000"
    bin1 = bin(dec)[2:]
    #display.scroll(bin1)
    bin1L = len(bin1)
    return bin0[0:8-bin1L] + bin1

def memWrite():
    global pc, memory, databyte
    memory[pc] = int(databyte, 2)
    pcWrite()
    #dataShow()
    #cleanup()

def memRead():
    global databyte, memory, pc
    databyte = bin00(memory[pc])
    pcWrite()
    dataShow()
    
def loadTest():
    global databyte, memory, pc
    #load sample program
    for i, d in enumerate(prog):
        memory[i] = d
    oled.fill_rect(0, 56, 128, 10, 0)
    oled.text('test code loaded',0,56)
    oled.show()
    memRead()

def loadFile():
    global databyte, memory, pc, ir, cb, p
    ir.close()
    try:
        with open('data.bin','r+b') as f:
            memory = list(f.read())
        oled.fill_rect(0, 56, 128, 10, 0)
        oled.text('file loaded',0,56)
        oled.show()
        memRead()
    except OSError:
        #if no file saved then load sample program
        for i, d in enumerate(prog):
            memory[i] = d
        oled.fill_rect(0, 56, 128, 10, 0)
        oled.text('test code loaded',0,56)
        oled.show()
        memRead()
    ir = NEC_8(p, cb)
    
def saveFile():
    #return
    global memory,ir,cb,p
    ir.close()
    try:
        with open('data.bin','w+b') as f:
            f.write(bytearray(memory))
        oled.fill_rect(0, 56, 128, 10, 0)
        oled.text('saved data.bin',0,56)
        oled.show()
    except OSError:
        oled.fill_rect(0, 56, 128, 10, 0)
        oled.text('OS Error',0,56)
        oled.show()
    ir = NEC_8(p, cb)

        
def remote_callback(code):

    # Codes listed below are for the
    # Sparkfun 9 button remote
    global databyte, octx, pc, tr, menu
    if code == 0x45:
        reset()
    elif code == 0x16:
        #oled.text('0',0,10)
        octobyte[octx] = 0
        dataWrite()
    elif code == 0x0c:
        #oled.text('1',0,10)
        octobyte[octx] = 1
        dataWrite()
    elif code == 0x18:
        print('2')
        octobyte[octx] = 2
        dataWrite()
    elif code == 0x5e:
        print('3')
        octobyte[octx] = 3
        dataWrite()
    elif code == 0x08:
        print('4')
        octobyte[octx] = 4
        dataWrite()
    elif code == 0x1c:
        print('5')
        octobyte[octx] = 5
        dataWrite()
    elif code == 0x5a:
        print('6')
        octobyte[octx] = 6
        dataWrite()
    elif code == 0x42:
        print('7')
        octobyte[octx] = 7
        dataWrite()
    elif code == 0x15:
        print("Run")
        oled.fill_rect(0, 56, 128, 10, 0)
        oled.text('Program running',0,56)
        oled.show()
        sleep(2)
        run()
    elif code == 0xffffff:
        print('repeat')
    elif code == 0x43:
        tr ^= True
        oled.fill_rect(0, 56, 128, 10, 0)
        oled.text('Trace:',0,56)
        oled.text(str(tr),50,56)
        oled.show()
        #print('trace ',tr)
    elif code == 0x40: # + store
        print('+')
        memWrite()
        pc = min(pc + 1,256)
        memRead()    
    elif code == 0x09: # >> forward
        print('>>')
        pc = min(pc + 1,256)
        memRead()
    elif code == 0x07: # << pc -1
        print('<<')
        pc = max(0,pc - 1)
        memRead()
    elif code == 0x19: # - goto mem addr from data entry
        print('-')
        #dataRead()
        pc = int(databyte, 2)
        memRead()
    elif code == 0x0d:
        print('C')
        cleanup()
    elif code == 0x44: #load test demo
        print('load')
        loadTest()
    elif code == 0x52: #load
        print('8')
        loadFile()
        print('data saved as data.bin')
    elif code == 0x4a: #save
        print('9')
        saveFile()
        print('data saved as data.bin')
    elif code == 0x47:
        #print('Exit -  Menu:\nLoad Store  Save\nBack Run Forward\n0 Goto Clear\n9=trace ')
        #oled.fill(0)
        if menu == True:
            menu = False
            oled.fill_rect(0, 10, 128, 54, 0)
            oled.text('Altair simulator',0,10)
            memRead()
        elif menu == False:
	        menu = True
	        oled.fill_rect(0, 10, 128, 54, 0)
	        oled.text('Reset       Menu',0,14)
	        oled.text('Test Store Trace',0,24)
	        oled.text('Back Run Forward',0,34)
	        oled.text('0    Goto  Clear',0,44)
	        oled.text('7    Load   Save',0,54)
	        #oled.text(str(regC),108,56)
	        oled.show()
    else:
        oled.text('.not known',0,10)  # unknown code

    return
    
def run():
    acc = 0 #Accumulator
    regB = 0    #register B
    regC = 0    #register C
    rpc = 0		#temp pc for loop
    global pc, memory, zf
    print('<')
    while True:
        sleep(0.1)
        memRead( )
        rpc = pc
        if tr:
                oled.fill_rect(0, 56, 128, 10, 0)
                oled.text('A:',0,56)
                oled.text(str(acc),16,56)
                oled.text('B:',45,56)
                oled.text(str(regB),61,56)
                oled.text('C:',88,56)
                oled.text(str(regC),104,56)
                oled.show()
                sleep(1)
                #oled.fill_rect(0, 56, 128, 10, 0)
                #print('a:'+str(acc))
        # implemented 8080 operating codes
        if memory[rpc] == 0x00:    #0: #NOP
            pc = pc + 1
        if memory[rpc] == 0x07:    #7: #RLC rotate left <<
            acc = acc << 1
            pc = pc + 1
        if memory[rpc] == 0x0D:    #13: #DCR_C RegC -1
            regC = regC - 1
            zf = (regC == 0)
            pc = pc + 1            
        if memory[rpc] == 0x0F:    #15: #RLR rotate right <<
            acc = acc >> 1
            pc = pc + 1
        if memory[rpc] == 0x32:    #50:   #STA
            memory[memory[pc + 1]] = acc
            pc = pc + 3
        if memory[rpc] == 0x3A:    #58:    #LDA
            acc = memory[memory[pc + 1]]
            pc = pc + 3
        if memory[rpc] == 0x3C:    #60: #INR_A
            acc = acc + 1
            zf = (acc == 0)
            pc = pc + 1
        if memory[rpc] == 0x3D:    #61: #DCR_A
            acc = acc - 1
            zf = (acc == 0)
            pc = pc + 1
        if memory[rpc] == 0x47:    #71 : #MOV_B,A
            regB = acc
            pc = pc + 1
        if memory[rpc] == 0x4F:    #71 : #MOV_C,A
            regC = acc
            pc = pc + 1
        if memory[rpc] ==0x76: # HLT
            break
        if memory[rpc] == 0x80:    #128:  #ADD
            acc = acc + regB
            pc = pc + 1
        if memory[rpc] == 0xA0:    #61: #ANA_B
            acc = acc & regB
            zf = (acc == 0)
            pc = pc + 1
        if memory[rpc] == 0xA8:    #61: #XRA_B
            acc = acc ^ regB
            zf = (acc == 0)
            pc = pc + 1
        if memory[rpc] == 0xAF:    #61: #XRA_A
            acc = acc ^ acc
            zf = (acc == 0)
            pc = pc + 1
        if memory[rpc] == 0xB0:    #61: #ORA_B
            acc = acc | regB
            zf = (acc == 0)
            pc = pc + 1
        if memory[rpc] == 0xC3:    #195:   #JMP
            pc = memory[pc + 1]
        if memory[rpc] == 0xC2:    #194:   #JNZ
            if zf == False:
                pc = memory[pc + 1]
            else:
                pc = pc + 3
        #if button_a.is_pressed():
        #    break
    print('>')    
    
    
# User callback
def cb(data, addr, ctrl):
    if data < 0:  # NEC protocol sends repeat codes.
        sleep(0.5)
        #oled.text('Repeat code.',0,0)
    else:
        remote_callback(data)



ir = NEC_8(p, cb)  # Instantiate receiver
ir.error_function(print_error)  # Show debug information

try:
    while True:

        sleep(1)
        collect()
except KeyboardInterrupt:
    ir.close()

