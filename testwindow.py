import icanfi
from pywt import waverec


test01 = icanfi.dataset()
test01.setfile('./dataset/bpm20.csv')
win = icanfi.windwoing(test01)
x = []
for i in win:
    icanfi.downsampling(i)
    icanfi.lowpass(i)
    icanfi.remove_DC(i)
    test_fft = icanfi.data_fft(i)
    select = icanfi.SNR_sub(test_fft)

    ssub_wavelet = icanfi.wavelet(i,select)
    #denoise = waverec(PCA_class,'db6')
    BPM = icanfi.estimate_fft(denoise,'r')
    x.append(BPM*60)
print(x)