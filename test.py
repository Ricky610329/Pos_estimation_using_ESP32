import icanfi

link = icanfi.multi_load('./dataset/1.csv')
print(link.keys())
for i in range(1,5):
    link[i] = icanfi.downsampling(link[i])
    link[i] = icanfi.windwoing(link[i],windowsize=230,hop=9999)

for i in range(1,5):
    print(link[i][0][18])