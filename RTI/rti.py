import math
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

NUM_LINK = 4

# area size (m)
HEIGHT = 1.5
WIDTH = 1.5

# nodes position index
default_nodes_position_index = np.zeros(shape = (8, 2))

# 30x30
VOXEL_ROW = 50
VOXEL_COLUMN = 50
NUM_VOXEL = VOXEL_ROW * VOXEL_COLUMN
VOXEL_HEIGHT = HEIGHT/VOXEL_ROW
VOXEL_WIDTH = WIDTH/VOXEL_COLUMN
# version 1
# length_of_link = [math.sqrt(pow(HEIGHT, 2) + pow(WIDTH, 2)), HEIGHT, math.sqrt(pow(HEIGHT, 2) + pow(WIDTH, 2)), WIDTH]
# version 2
# length_of_link = [HEIGHT, HEIGHT, WIDTH, WIDTH]
default_attenuation_of_voxels = np.zeros(shape = (NUM_VOXEL, 1))

# W
default_weight = np.ones(shape = (NUM_LINK, NUM_VOXEL))

# Tikhonov regularization parameter
DEFULT_TIKHONOV = 100

# MMSE regularization parameter
DEFULT_MMSE = 0

# margin_parameter (m)
DEFULT_MARGIN = 0.03

# attenuations of 4 links(delta_r)
default_attenuations = np.array([0, 0, 0, 0])

# covariance matrix sigma
default_covariance_matrix = np.zeros(shape = (NUM_VOXEL, NUM_VOXEL))

# distance calculate
def __distance_between(position_a, position_b):
   
    distance = math.sqrt(pow(position_a[0] - position_b[0], 2) + \
        pow(position_a[1] - position_b[1], 2))
    
    return distance

def __ls_weight_value_generation(transmitter_position, receiver_position, voxel_position, margin_parameter = DEFULT_MARGIN):
    
    weight = 0
    length_of_link = __distance_between(transmitter_position, receiver_position)
    # from voxel to transmitter
    distance_v2t = __distance_between(voxel_position, transmitter_position)
    # from voxel to receiver 
    distance_v2r = __distance_between(voxel_position, receiver_position)

    if(distance_v2r + distance_v2t < length_of_link + margin_parameter):
        weight = 1/math.sqrt(length_of_link)

    return weight

def __set_sensor_position_v1():
    global default_nodes_position_index 
    default_nodes_position_index = np.array([[0, 0], [0, 15], [0, 30], [15, 30], [30, 30], [30, 15], [30, 0], [15, 0]])

def __set_sensor_position_v2():
    global default_nodes_position_index 
    default_nodes_position_index = np.array([[0, VOXEL_COLUMN/3], [0, VOXEL_COLUMN * 2/3], [VOXEL_ROW/3, VOXEL_COLUMN],\
         [VOXEL_ROW * 2/3, VOXEL_COLUMN], [VOXEL_ROW, VOXEL_COLUMN/3], [VOXEL_ROW, VOXEL_COLUMN * 2/3],\
             [VOXEL_ROW/3, 0], [VOXEL_ROW * 2/3, 0]])

# generate sigma
def voxels_covariance_matrix_genertation(distance_parameter = 2):
    voxels_covariance_matrix = default_covariance_matrix
    for i in range(NUM_VOXEL):
        for j in range(NUM_VOXEL):
            voxels_covariance_matrix[i][j] = math.exp(-1/distance_parameter * __distance_between(divmod(i, VOXEL_COLUMN),divmod(j, VOXEL_COLUMN)))

    return voxels_covariance_matrix
    
# Model in CSI_MIMO RTI
def weight_matrix_generation(version = 2):
    weight_matrix = default_weight
    for i in range(NUM_LINK):
        for j in range(NUM_VOXEL):
            x, y = divmod(j, VOXEL_COLUMN)
            # adjust the cooridinate to center
            x = (x + 0.5) * VOXEL_HEIGHT
            y = (y + 0.5) * VOXEL_WIDTH
            voxel_position = [x, y]

            if(version == 1):
            # version 1
                # link 1: (0, 0) and (30, 30)
                if(i == 0):                    
                    weight_matrix[i][j] = __ls_weight_value_generation([0, 0],\
                         [VOXEL_ROW * VOXEL_HEIGHT, VOXEL_COLUMN * VOXEL_WIDTH],\
                             voxel_position)
                   
                # link 2: (15, 0) and (15, 30)
                elif(i == 1):
                    weight_matrix[i][j] = __ls_weight_value_generation([VOXEL_ROW/2 * VOXEL_HEIGHT, 0],\
                         [VOXEL_ROW/2 * VOXEL_HEIGHT, VOXEL_COLUMN * VOXEL_WIDTH],\
                             voxel_position)

                # link 3: (30, 0) and (0, 30)
                elif(i == 2):
                    weight_matrix[i][j] = __ls_weight_value_generation([VOXEL_ROW * VOXEL_HEIGHT, 0],\
                         [0, VOXEL_COLUMN * VOXEL_WIDTH],\
                             voxel_position)

                # link 4: (0, 15) and (30, 15)
                elif(i == 3):
                    weight_matrix[i][j] = __ls_weight_value_generation([0, VOXEL_COLUMN/2 * VOXEL_WIDTH],\
                         [VOXEL_ROW * VOXEL_HEIGHT, VOXEL_COLUMN/2 * VOXEL_WIDTH],\
                             voxel_position)
                else:
                    print(str(i)+' out of range')

            else:      
            # version 2
                length_of_link = [HEIGHT, HEIGHT, WIDTH, WIDTH]
            # link 1: (0, 10) and (30, 10)
                if(i == 0):
                    weight_matrix[i][j] = __ls_weight_value_generation([0, VOXEL_COLUMN/3 * VOXEL_WIDTH],\
                         [VOXEL_ROW * VOXEL_HEIGHT, VOXEL_COLUMN/3 * VOXEL_WIDTH],\
                             voxel_position)

                # link 2: (0, 20) and (30, 20)
                elif(i == 1):
                    weight_matrix[i][j] = __ls_weight_value_generation([0, VOXEL_COLUMN * 2/3 * VOXEL_WIDTH],\
                         [VOXEL_ROW * VOXEL_HEIGHT, VOXEL_COLUMN * 2/3 * VOXEL_WIDTH],\
                             voxel_position)

                # link 3: (10, 0) and (10, 30)
                elif(i == 2):
                    weight_matrix[i][j] = __ls_weight_value_generation([VOXEL_ROW/3 * VOXEL_HEIGHT, 0],\
                         [VOXEL_ROW/3 * VOXEL_HEIGHT, VOXEL_COLUMN * VOXEL_WIDTH],\
                             voxel_position)

                # link 4: (20, 0) and (20, 30)
                elif(i == 3):
                    weight_matrix[i][j] = __ls_weight_value_generation([VOXEL_ROW * 2/3 * VOXEL_HEIGHT, 0],\
                         [VOXEL_ROW * 2/3 * VOXEL_HEIGHT, VOXEL_COLUMN * VOXEL_WIDTH],\
                             voxel_position)

                else:
                    print(str(i)+' out of range')
            '''
            if(version == 1):
            # version 1
                length_of_link = [math.sqrt(pow(HEIGHT, 2) + pow(WIDTH, 2)), HEIGHT, math.sqrt(pow(HEIGHT, 2) + pow(WIDTH, 2)), WIDTH]
                # link 1: (0, 0) and (30, 30)
                if(i == 0):
                    if( math.sqrt(pow(x,2) + pow(y,2)) + math.sqrt(pow((VOXEL_ROW * VOXEL_HEIGHT - x),2) + pow((VOXEL_COLUMN * VOXEL_WIDTH - y),2)) \
                        < length_of_link[i] + margin_parameter):
                        weight_matrix[i][j] = 1/math.sqrt(length_of_link[i])
                    else:
                        weight_matrix[i][j] = 0
                # link 2: (15, 0) and (15, 30)
                elif(i == 1):
                    if( math.sqrt(pow((VOXEL_ROW/2 * VOXEL_HEIGHT - x),2) + pow(y,2)) + \
                        math.sqrt(pow((VOXEL_ROW/2 * VOXEL_HEIGHT - x),2) + pow((VOXEL_COLUMN * VOXEL_WIDTH - y),2)) \
                        < length_of_link[i] + margin_parameter):
                        weight_matrix[i][j] = 1/math.sqrt(length_of_link[i])
                    else:
                        weight_matrix[i][j] = 0
                # link 3: (30, 0) and (0, 30)
                elif(i == 2):
                    if( math.sqrt(pow((VOXEL_ROW * VOXEL_HEIGHT - x),2) + pow(y,2)) + math.sqrt(pow(x,2) + pow((VOXEL_COLUMN * VOXEL_WIDTH - y),2)) \
                        < length_of_link[i] + margin_parameter):
                        weight_matrix[i][j] = 1/math.sqrt(length_of_link[i])
                    else:
                        weight_matrix[i][j] = 0
                # link 4: (0, 15) and (30, 15)
                elif(i == 3):
                    if( math.sqrt(pow(x,2) + pow((VOXEL_ROW/2 * VOXEL_HEIGHT - y),2)) + \
                        math.sqrt(pow((VOXEL_ROW * VOXEL_HEIGHT - x),2) + pow((VOXEL_COLUMN/2 * VOXEL_WIDTH - y),2)) \
                        < length_of_link[i] + margin_parameter):
                        weight_matrix[i][j] = 1/math.sqrt(length_of_link[i])
                    else:
                        weight_matrix[i][j] = 0
                else:
                    print(str(i)+' out of range')
            else:      
            # version 2
                length_of_link = [HEIGHT, HEIGHT, WIDTH, WIDTH]
            # link 1: (0, 10) and (30, 10)
                if(i == 0):
                    if( math.sqrt(pow(x,2) + pow((VOXEL_COLUMN/3 * VOXEL_WIDTH - y),2)) + \
                        math.sqrt(pow((VOXEL_ROW * VOXEL_HEIGHT - x),2) + pow((VOXEL_COLUMN/3 * VOXEL_WIDTH - y),2)) \
                        < length_of_link[i] + margin_parameter):
                        weight_matrix[i][j] = 1/math.sqrt(length_of_link[i])
                    else:
                        weight_matrix[i][j] = 0
                # link 2: (0, 20) and (30, 20)
                elif(i == 1):
                    if( math.sqrt(pow((x),2) + pow((VOXEL_COLUMN * 2/3 * VOXEL_WIDTH - y),2)) + \
                        math.sqrt(pow((VOXEL_ROW * VOXEL_HEIGHT - x),2) + pow((VOXEL_COLUMN * 2/3 * VOXEL_WIDTH - y),2)) \
                        < length_of_link[i] + margin_parameter):
                        weight_matrix[i][j] = 1/math.sqrt(length_of_link[i])
                    else:
                        weight_matrix[i][j] = 0
                # link 3: (10, 0) and (10, 30)
                elif(i == 2):
                    if( math.sqrt(pow((VOXEL_ROW/3 * VOXEL_HEIGHT - x),2) + pow(y,2)) + \
                        math.sqrt(pow((VOXEL_ROW/3 * VOXEL_HEIGHT - x),2) + pow((VOXEL_COLUMN * VOXEL_WIDTH - y),2)) \
                        < length_of_link[i] + margin_parameter):
                        weight_matrix[i][j] = 1/math.sqrt(length_of_link[i])
                    else:
                        weight_matrix[i][j] = 0
                # link 4: (20, 0) and (20, 30)
                elif(i == 3):
                    if( math.sqrt(pow((VOXEL_ROW * 2/3 * VOXEL_HEIGHT - x),2) + pow((y),2)) + \
                        math.sqrt(pow((VOXEL_ROW * 2/3 * VOXEL_HEIGHT - x),2) + pow((VOXEL_COLUMN * VOXEL_WIDTH - y),2)) \
                        < length_of_link[i] + margin_parameter):
                        weight_matrix[i][j] = 1/math.sqrt(length_of_link[i])
                    else:
                        weight_matrix[i][j] = 0
                else:
                    print(str(i)+' out of range')
                '''
    return weight_matrix

# Model in Sensing from the sky
def weight_matrix_generation_v2(decay_rate = 0.1, compensation_coefficient = 0.03):
    weight_matrix = default_weight
    # test
    __set_sensor_position_v2()
    nodes_position_index = default_nodes_position_index    
    
    # test
    length_of_link = HEIGHT 

    for i in range(NUM_LINK):
        for j in range(NUM_VOXEL):
            x, y = divmod(j, VOXEL_COLUMN)
            # adjust the cooridinate to center
            x = (x + 0.5) * VOXEL_HEIGHT
            y = (y + 0.5) * VOXEL_WIDTH
            voxel_position = [x, y]
            transmitter_position = [float(nodes_position_index[i][0]*VOXEL_HEIGHT), float(nodes_position_index[i][1]*VOXEL_WIDTH)]
            receiver_position = [float(nodes_position_index[i+4][0]*VOXEL_HEIGHT), float(nodes_position_index[i+4][1]*VOXEL_WIDTH)]
           
            weight_matrix[i][j] = (1/math.sqrt(length_of_link)) * math.exp((-1/decay_rate )* \
                (__distance_between(voxel_position, transmitter_position) +\
                     __distance_between(voxel_position, receiver_position) - length_of_link)) + compensation_coefficient * (__distance_between(voxel_position, receiver_position) + __distance_between(voxel_position, transmitter_position))
    
    return weight_matrix

# Tikhonov-regularized least squares esimate
def tikhonov_regularized_least_squares_estimate(attenuations = default_attenuations, weight_matrix = default_weight,\
     tikhonov_regularization_parameter = DEFULT_TIKHONOV):
    # x_delat = (W_T*W + mu*I)^-1*W_T*r_delta
    attenuation_of_voxels = np.dot(np.dot(np.linalg.inv(np.dot(weight_matrix.T,weight_matrix) +\
         tikhonov_regularization_parameter*np.identity(NUM_VOXEL)),weight_matrix.T),attenuations)
    
    return attenuation_of_voxels

# MMSE estimation
def minimum_mean_square_error_estimate(attenuations = default_attenuations, weight_matrix = default_weight,\
    noise_covariance = 1.42, covariance_matrix = default_covariance_matrix, regularization_parameter = DEFULT_MMSE):
    # test noise covariance matrix
    # noise_covariance_matrix = np.array([[1, noise_covariance, noise_covariance, noise_covariance],[noise_covariance, 1, noise_covariance, noise_covariance],\
    #   [noise_covariance, noise_covariance, 1, noise_covariance], [ noise_covariance, noise_covariance, noise_covariance, 1]])
    noise_covariance_matrix = np.identity(NUM_LINK)
    attenuation_of_voxels = np.dot(np.dot(np.dot((np.dot(np.dot(weight_matrix.T, np.linalg.inv(noise_covariance_matrix)),weight_matrix)+\
        regularization_parameter*np.linalg.inv(covariance_matrix)),weight_matrix.T), np.linalg.inv(noise_covariance_matrix)),attenuations)

    return attenuation_of_voxels

# Show the position of the target
def find_position(attenation_of_voxel):
    max_value_index = np.argmax(attenation_of_voxel)
    position = [0,0]
    position[0], position[1] = divmod(max_value_index, VOXEL_COLUMN)

    print(position)
    
    return position

# Show the heatmap of voxels' attenuation
def show_heatmap(attenuation_of_voxel):
    plt.figure(figsize=(8, 8))
    
    sns.set(font_scale=1.5)
    sns.heatmap(data = np.reshape(attenuation_of_voxel,(VOXEL_ROW, VOXEL_COLUMN)), square = True)

    plt.xlabel(' ',fontsize=22)
    plt.ylabel(' ',fontsize=22)
    plt.show()
         


        
