import RPi.GPIO as GPIO
import time
import concurrent.futures
import random
from tkinter import *
LED1 = 11
LED2 = 13
LED3 = 15
LED4 = 16   
winning_led = random.choice([16,11,13,15])

#when becomes "isend" True
#from the user pressing a button
#the led thread stops  
#end() only exists because a tkinter button can only activate a function
isend = False
def end(status):
    global isend
    isend = status
    
def winner(attempt):
    global winning_led
    if type(attempt) is str:
        if winning_led == 16:
           return "go for orange"
        elif winning_led == 15:
           return "go for red" 
        elif winning_led == 13:
           return "go for green"
        elif winning_led == 11:
           return "go for blue"
        else:
            print("not happening") 

    print(winning_led)
    if attempt == winning_led:
        return True
    else:
        return False

#configures GPIO settings
def setup():
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(LED1, GPIO.OUT)
    GPIO.setup(LED2, GPIO.OUT)
    GPIO.setup(LED3, GPIO.OUT)
    GPIO.setup(LED4, GPIO.OUT)
    
#starts the LEDs     
def lightup():
    #list of all LEDs
    leds = [LED1, LED2, LED3, LED4]
    x = 0
    attempt = int
    
    while not isend:
        if x < 4:
            GPIO.output(leds[x], True)
            time.sleep(0.1)
            attempt = leds[x]
            GPIO.output(leds[x], False)
            time.sleep(0.1)
            x += 1
            
        elif x == 4:
            x = 1
            #sets LEDs as itself but reversed
            leds = leds[::-1]
            
    GPIO.output(attempt, True)
    time.sleep(1.5)
    GPIO.output(attempt, False)
    
    return attempt
#gui 
def button():
    global isend
    root = Tk()
    
    colorOfChoice = Label(root, text=winner("?"), fg=(winner("?").split())[-1])
    stopButton = Button(root, text="stop", command=lambda: end(True))
    if isend:
        root.destroy()
    stopButton.grid(row=0, column=2)
    colorOfChoice.grid(row=0, column=1)
    
    root.geometry("450x250")
    root.mainloop()

def winScreen(win):
    dis = Tk()
    won = Label(dis, text="YOU WIN!")
    lost = Label(dis, text="HAHAHA YOU LOSE!")
    if win:
        won.pack()
    elif not win:
        lost.pack()
        
    dis.geometry("450x450")
    destroy()
    dis.mainloop()
    
def destroy():
    GPIO.cleanup()


def main():
    with concurrent.futures.ThreadPoolExecutor() as executor:
        gui = executor.submit(button)
        lights = executor.submit(lightup)
        game = lights.result()       
    
    if winner(game):
        winScreen(True)
        
    elif not winner(game):
        winScreen(False)
        
    else:
        print("problem")
    
if __name__ == '__main__':
    try:
        setup()
        main()
        
    except KeyboardInterrupt:
        destroy()
        
        
        
        