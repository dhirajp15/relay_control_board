from time import sleep
from timeit import default_timer as timer
from gpiozero import LED,Button
import subprocess
import configparser
import atexit
d_relay_on=[[5,10,15,20],[8,14,17,22]]
d_relay_off=[[8,12,17,25],[9,13,19,27]]
relay_on=list()
relay_off=list()
states = [0]*16
led = list()
RELAY_PINS = [14,15,18,23,24,25,8,7,12,16,20,21,2,3,4,17]
button = Button(27)
reset = Button(22)
power_led = LED(26)
for j in range(16):
	led.append(LED(RELAY_PINS[j]))
global t0,t1
def read_relay_timings():
    config = configparser.ConfigParser()
    config.read("relay_timings.txt")
    for i in range(16):
        relay_on.append(config.get("On_Timings", "Relay_"+str(i+1)))
        relay_off.append(config.get("Off_Timings", "Relay_"+str(i+1)))
    #print(relay_on)
    #print(relay_off)
    for i in range(16):
        relay_on[i] = list(map(int,relay_on[i].split(",")))
        relay_off[i] = list(map(int,relay_off[i].split(",")))
    #print(relay_on)
    #print(relay_off)
            
        


def relay_states(relay_no):
        global t0, res,t1
        t1 = timer()
        print(int(t1-t0))
        if int(t1-t0) in relay_on[relay_no]:
            if states[relay_no] == 0:
                led[relay_no].on()
                print(states[i])
                print(" Relay "+ str(relay_no) + " on time:\n")
                print(t1-t0)
                states[relay_no] = 1
        if int(t1-t0) in relay_off[relay_no]:
            if states[relay_no] == 1:
                led[relay_no].off()
                print(states[i])
                print(" Relay "+ str(i) + " off time:\n")
                print(t1-t0)
                states[relay_no] = 0
def run_application():
    global res,t0,t1
    res  =	subprocess.Popen("vlc song.mp3",shell= "True",stdin = subprocess.PIPE)
    sleep(3)
    t0 = timer()
    while True:
        for i in range (16):
            relay_states(i)
        if reset.is_pressed == True:
            print("restarting...")
            if res.poll() is None:
            	res.stdin.write("quit\n");
            for k in range(16):
                led[k].off()
            break;
        elif button.is_pressed == True:
            temp = timer()
            sleep(2)
            print("pausing...")
            res.stdin.write("pause\n")
            button.wait_for_press()
            sleep(2)
            res.stdin.write("pause\n")
            t0  = t0 + (timer() - temp)
            #res.stdin.write("\n")
            
read_relay_timings()
for k in range(16):
    led[k].off()
while True:
    power_led.on()
    print("press button to start")
    button.wait_for_press()
    states = [0]*16
    run_application()
        
def cleanup():
    global res
    for k in range(16):
        led[k].off()
    res.stdin.write("quit\n")
    
atexit.register(cleanup)
