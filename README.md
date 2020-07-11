# ESP_altair
[8bit Altair simulator](http://dperks.co.uk/altair/) with IR remote control for ESP8266

Requires [IR remote routine by Peter Hinch](https://github.com/peterhinch/micropython_ir)  
I just copy the ir_rx folder (reduced to files \_\_init\_\_.py nec.py print_error.py) to the board 

Requires SSD1306.py for i2c OLED display.  
There seem to be a range of sources for the SSD1306 driver.  
I add an example in the repository.

I have used hard disc jumpers to connect the OLED display and IR sensor in a neat row along the GPIO.

|Pin|GPIO|Component|
|---|---|---|
|D3|0|OLED SDA|
|D4|2|OLED SCL|
|3V||Shared|
|GND||Shared|
|D5|14|IR data|

The Infrared codes and program controls are as follows: 

 |45 Exit|46|47 Menu|
 |---|---|---|
 |44 Test|40 Store|43 Trace|
 |07 Back|15 Run|09 Forward|
 |16 0|19 Goto|0D Clear|
 |0C 1|18 2|5E 3|
 |084|1C 5|5A 6|
 |42 7|52 Load|4A Save|

