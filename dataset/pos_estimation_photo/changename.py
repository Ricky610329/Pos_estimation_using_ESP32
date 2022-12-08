import os

everything = os.listdir(r'./')
for i in range(1,37):
    
    os.rename(everything[i],str(i)+'.jpg')
