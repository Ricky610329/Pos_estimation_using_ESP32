import icanfi
import matplotlib.pyplot as plt


link = icanfi.multi_load('./dataset/nopeople.csv')

print(link[2].keys())
