# Child_Tracker

This system consists of Raspberry Pi 3 model B and GSM/GPS Module (SIM 808). The tracker gets Child's position from the GSM/GPS Module, and sends it as text messages to your phone.

# Tracker 

## Hardware 

The tracker requires a  GSM/GPS Module e.g. SIM808.  I used SIM 808 Module and a Raspberry Pi 3 model B. You also need a suitable power supply for these.

## Wiring 
![Wiring](https://i.ibb.co/fq2VsZR/Wiring.png)

## Software

The Tracker.py script connects to the GSM/GPS Module, firstly to read the current position and secondly to send that position to your mobile phone.
You should autostart the script so that it runs after power-up.

The script make those processes:

1. - Trun on GPS.
1. - Read Current Location.
1. - Convert Currnt Location of Child From NMEA GGA Format to Decimel Degree.
1. - Check if Child in Red or Green Zone based on pre-defined locations.
1. - Create a message to send.
1. - Send message to your phone.


## Final Product
![FinalProduct](https://i.ibb.co/8Xd9NV9/IMG-20221229-184233.jpg)

## Output
![Output](https://i.ibb.co/zVJT4HZ/Screenshot-2023-01-07-16-26-31-75-cf3cf72bd8e53b0db7ddb0a6f2208af9.jpg)

### P.S
- Remember to disable serial login on the Pi, but keep the serial port enable, in raspi-config.
- Remember to use a SIM card with enough credit for the number of texts you expect to be sent.
