import icanfi
import matplotlib.pyplot as plt
from pywt import waverec

test01 = icanfi.dataset()
test01.setfile('./dataset/bpm15.csv')
win = icanfi.windwoing(test01)

saw = win[3]
icanfi.downsampling(saw)
icanfi.lowpass(saw)
icanfi.remove_DC(saw)
plt.title("spec")
plt.xlabel("sec")
plt.ylabel("amplitude")
plt.plot(saw['time'],saw[12])
plt.show()