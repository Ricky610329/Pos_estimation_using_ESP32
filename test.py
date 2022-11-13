import icanfi
import matplotlib.pyplot as plt


data = icanfi.load('./dataset/block.csv')

data = icanfi.into_energy(data)
data = icanfi.delta_R(data)
plt.plot(data['time'],data['r'])
plt.show()