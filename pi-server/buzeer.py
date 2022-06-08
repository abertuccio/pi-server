from gpiozero import TonalBuzzer
from gpiozero.tones import Tone
import time

BUZZER = 4

b = TonalBuzzer(BUZZER)

b.play(Tone("D4"))
time.sleep(0.5)
b.stop()
b.play(Tone("B3"))
time.sleep(0.5)
# b.stop()
# b.play(Tone("D4"))
# time.sleep(0.5)
# b.play(Tone("C#3"))
# time.sleep(0.5)
# b.play(Tone("D3"))
# time.sleep(0.5)
# b.play(Tone("A3"))
# time.sleep(0.5)
b.stop()