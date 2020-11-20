import numpy as np
import scipy

def get_ridge(stft, i_center=0, search_r=10, include_r=80, ):
    # returns the indices of the ridge
    if i_center == 0:
        i_center = np.argmax(np.abs(stft[:, 0]))
    # if i_center_is_in_frequency: i_center=int(i_center*viewf_i/nyquist)
    if i_center < include_r:
        i_center = include_r

    ridgei = np.zeros(stft.shape[1])
    ridge_amp = np.zeros(stft.shape[1], dtype=complex)

    search_area = np.abs(stft[i_center - include_r:i_center + include_r])
    ridgei[0] = np.argmax(search_area[:, 0])
    for i in range(1, stft.shape[1]):
        ridgei[i] = np.argmax(search_area[:, i])
        ridge_amp[i] = stft[int(ridgei[i] + i_center - include_r), i]
    ridgei = ridgei + i_center - include_r

    return ridgei, ridge_amp


def rice_region_fit(stft, f1, f2, t1=0, t2=-1):
    # fits a rician noise to the abs of a region of an an stft.
    # returns fit parameters
    # user should select a region where only white noise or stationary signal is present

    if t2 == -1:
        t2 = stft.shape[1]

    amplitude = np.abs(stft[f1:f2, t1:t2]).flatten()
    shape, loc, sigma = scipy.stats.rice.fit(amplitude)

    return shape, loc, sigma