from gpiozero import TonalBuzzer
from gpiozero.tones import Tone
import time

BUZZER = 4

b = TonalBuzzer(BUZZER)

b.play(Tone("A3"))
time.sleep(0.3)
b.stop()
time.sleep(1) 
b.play(Tone("A3"))
time.sleep(0.3)
b.stop() 

b.stop()