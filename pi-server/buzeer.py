from gpiozero import TonalBuzzer
from gpiozero.tones import Tone
import time

BUZZER = 4

b = TonalBuzzer(BUZZER)

b.play(Tone("D4"))
time.sleep(0.2)
b.play(Tone("B3"))
time.sleep(0.5)
b.play(Tone("D4"))
time.sleep(0.2)
b.play(Tone("C#4"))
time.sleep(0.5)
b.play(Tone("D4"))
time.sleep(0.2)
b.play(Tone("C#4"))
time.sleep(0.5)
b.play(Tone("A3"))
time.sleep(0.6)
b.stop()