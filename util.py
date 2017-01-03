import numpy as np
from scipy import signal
import scipy.io as sio


def load_data():
    """Get the data from disk.

    Returns
    -------
    mat1_sino : numpy.ndarray
        projection of material 1
    mat2_sino : numpy.ndarray
        projection of material 2
    """
    data_mat = sio.loadmat('E:/Data/spectral_ct/aux_corr_in_real_ct_image.mat')
    data = data_mat['decomposedBasisProjectionsmmObj']
    data = data.swapaxes(0, 2)
    return data


def estimate_cov(I1, I2):
    """Estiamte the covariance of I1 and I2."""
    assert I1.shape == I2.shape

    H, W = I1.shape

    M = np.array([[1, -2, 1],
                  [-2, 4., -2],
                  [1, -2, 1]])

    sigma = np.sum(signal.convolve2d(I1, M) * signal.convolve2d(I2, M))
    sigma /= (W * H - 1)

    return sigma / 36.0  # unknown factor, too lazy to solve


def cov_matrix(data):
    """Estimate the covariance matrix from data.

    Parameters
    ----------
    data : kxnxm `numpy.ndarray`
        Estimates the covariance along the first dimension.

    Returns
    -------
    cov_mat : kxk `numpy.ndarray`
        Covariance matrix.
    """
    n = len(data)

    cov_mat = np.zeros([n, n])
    for i in range(n):
        for j in range(n):
            cov_mat[i, j] = estimate_cov(data[i], data[j])

    return cov_mat


if __name__ == '__main__':
    # Example
    I1 = np.random.randn(50, 50)
    I2 = 3 * np.random.randn(50, 50)
    corr_variable = (I1 + I2)

    print(estimate_cov(I1, I1))  # should be 1
    print(estimate_cov(I1, I2))  # should be 0
    print(estimate_cov(I2, I1))  # should be 0
    print(estimate_cov(I2, I2))  # should be 9
    print(estimate_cov(I1, corr_variable))  # should be 1
