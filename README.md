# ESP_altair
8bit Altair simulator with IR remote control for ESP8266

Requires IR remote routine by Peter Hinch
https://github.com/peterhinch/micropython_ir

Requires SSD1306.py for i2c OLED display.
There seem to be a range of sources for the SSD1306 driver
I add an example in the repository.

|45 Exit|46|47 Menu|
|44 Test|40 Store|43 Trace|
|07 Back|15 Run|09 Forward|


 <table align= left border =1, cellpadding=2, height = 380>
  <tr>
    <td>45<br>Exit</td>
    <td>46</td> 
    <td>47<br>Menu</td> 
 </tr>
  <tr>
    <td>44<br>Test</td>
    <td>40<br>Store</td> 
    <td>43<br>Trace</td>
  </tr>
<tr>
    <td>07<br>Back</td>
    <td>15<br>Run</td> 
    <td>09<br>Forward</td>
  </tr>
<tr>
    <td>16<br>0</td>
    <td>19<br>Goto</td> 
    <td>0D<br>Clear</td>
  </tr>
<tr>
    <td>0C<br>1</td>
    <td>18<br>2</td> 
    <td>5E<br>3</td>
  </tr>
<tr>
    <td>08<br>4</td>
    <td>1C<br>5</td> 
    <td>5A<br>6</td>
  </tr>
<tr>
    <td>42<br>7</td>
    <td>52<br>Load</td> 
    <td>4A<br>Save</td>
  </tr>
</table>
