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
time.sleep(1)
b.play(Tone("G4"))
time.sleep(0.3)
b.play(Tone("F4"))
time.sleep(0.3)
b.play(Tone("E4"))
time.sleep(0.3)
b.play(Tone("D4"))
time.sleep(0.3)
b.play(Tone("C4"))
time.sleep(0.3)
b.play(Tone("C5"))
time.sleep(0.7)
b.stop()