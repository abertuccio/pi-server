from gpiozero import TonalBuzzer
from gpiozero.tones import Tone
import time

BUZZER = 4

b = TonalBuzzer(BUZZER)

for x in range(8):
    b.play(Tone("A3"))
    time.sleep(0.2)
    b.stop()
    time.sleep(0.8)