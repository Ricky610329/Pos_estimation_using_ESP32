import icanfi

link = icanfi.multi_load('./dataset/1.csv')
print(link.keys())
for i in range(1,5):
    link[i] = icanfi.downsampling(link[i])

for i in range(1,5):
    print(link[i]['time'][0:30])