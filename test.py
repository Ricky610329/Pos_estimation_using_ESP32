import icanfi
import matplotlib.pyplot as plt


data = icanfi.load('./dataset/block.csv')
data = icanfi.into_energy(data)
icanfi.lowpass(data)
plt.plot(data['time'][500:],data[0][500:]-data[0][500])
plt.show()