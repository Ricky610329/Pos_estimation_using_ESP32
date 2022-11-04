import icanfi
import matplotlib.pyplot as plt
import numpy as np
from scipy import fft

grab = icanfi.dataset()
grab.setfile("./dataset/wav.csv",mod = 'a')

i = grab.data

data = icanfi.windwoing(grab)

for i in data:
    icanfi.downsampling(i)
    icanfi.lowpass(i)
    icanfi.remove_DC(i)
    datafft = icanfi.data_fft(i)
    select = icanfi.SNR_sub(datafft)
    classify = icanfi.fast_slow_classify(i,select)
    print(classify)
    #plt.plot(classify['frequency'],np.abs(classify['pca']))
    #plt.show()

'''icanfi.downsampling(i)
icanfi.lowpass(i)
icanfi.remove_DC(i)
datafft = icanfi.data_fft(i)
select = icanfi.SNR_sub(datafft)
selected_pca = icanfi.do_PCA(i,select)
print(select)
#plt.plot(fft.fftfreq(len(i['time']),0.4),np.abs(fft.fft(selected_pca['pca'])))
#plt.plot(datafft['frequency'],np.abs(datafft[14]))
plt.show()'''