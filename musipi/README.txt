Music Pi Controller

The ^control.sh^ script creates a Pi music controller when connected to 5
push-to-make switches and an LED/resistor pair.

First install Wiring Pi, mpd, mpc and ncmpcpp.

Then connect the switches to Wiring Pi's pins 0 through 4, and the LED on pin
7. Connect some speakers to the Pi's audio out socket.

Then add ^/.../musipi/control.sh &^ to ^/etc/rc.local^.

Set up a playlist in mpc or ncmpcpp and off you go :-)

The buttons:

- play / pause
- previous track 
- next track
- volume up
- volume down
