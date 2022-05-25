from gpiozero import TonalBuzzer
from gpiozero.tones import Tone
import time

BUZZER = 4

b = TonalBuzzer(BUZZER)

b.play(Tone("A4"))
time.sleep(0.8)
b.play(Tone("B4"))
time.sleep(0.8)
b.play(Tone("C4"))

b.stop()