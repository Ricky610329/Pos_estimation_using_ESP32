import icanfi.algorithm
import icanfi.load
import icanfi.preprocess
import icanfi.analysis
import icanfi.parameter
import icanfi.filters
import icanfi.estimate

#load
dataset = icanfi.load.dataset
load_r = icanfi.load.load_r


#analysis
analysis_time = icanfi.analysis.analysis_time
analysis_sub = icanfi.analysis.analysis_sub
frame_distance = icanfi.analysis.frame_distance

#preprocess
windwoing = icanfi.preprocess.windowing
downsampling = icanfi.preprocess.downsampling
remove_DC = icanfi.preprocess.remove_DC


#filters
lowpass = icanfi.filters.lowpass
data_fft = icanfi.filters.data_fft
wavelet = icanfi.filters.wavelet
bandpass = icanfi.filters.bandpass

#algorithm
SNR_sub = icanfi.algorithm.SNR_sub
PCA_fast_slow = icanfi.algorithm.PCA_fast_slow
do_PCA = icanfi.algorithm.do_PCA
fast_slow_classify = icanfi.algorithm.fast_slow_classify

#estimate
estimate_fft = icanfi.estimate.estimate_fft