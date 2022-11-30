import RTI
import numpy as np
import time
#attenuation = RTI.RTI.tikhonov_regularized_least_squares_estimate(np.array([10, 10, 10, 10]),RTI.RTI.weight_matrix_generation( ))
start = time.time()
x= RTI.rti.weight_matrix_generation_v2()
print(time.time()-start)
co = RTI.rti.voxels_covariance_matrix_genertation()
print(time.time()-start)
attenuation = RTI.rti.minimum_mean_square_error_estimate(np.array([10, 400, 10, 400]),x,covariance_matrix = co)
print(time.time()-start)
RTI.rti.find_position(attenuation)
print(time.time()-start)
RTI.rti.show_heatmap(attenuation)
print(time.time()-start)