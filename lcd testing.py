from RPLCD import i2c

# Import sleep library
from time import sleep

# constants to initialise the LCD
lcdmode = 'i2c'
cols = 20
rows = 4
charmap = 'A00'
i2c_expander = 'PCF8574'

# Generally 27 is the address;Find yours using: i2cdetect -y 1 
address = 0x27 
port = 1 # 0 on an older Raspberry Pi

# Initialise the LCD
lcd = i2c.CharLCD(i2c_expander, address, port=port, charmap=charmap,
                  cols=cols, rows=rows)

# Write a string on first line and move to next line
lcd.backlight_enabled = True 
lcd.write_string('Hello world')
'''
lcd.crlf()
lcd.write_string('IoT proj')
lcd.crlf()
lcd.write_string('rkp')
sleep(10)
# Switch off backlight
lcd.backlight_enabled = True 
# Clear the LCD screen
lcd.close(clear=True)
'''