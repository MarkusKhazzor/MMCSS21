import math
import numpy as np


def calculate_rollercoaster_samples_and_handles(samples: np.ndarray):

    # coefficient matrix
    np_array_control_points_coefficient_matrix = np.zeros(shape=(samples.shape[0], samples.shape[0]))  # has to be n*n dimensional

    # a handles
    for i in range(samples.shape[0]):
        # calc index
        a_i = i
        a_i_plus_one = (i+1) % samples.shape[0]
        a_i_plus_two = (i+2) % samples.shape[0]

        # calc factor for index
        np_array_control_points_coefficient_matrix[i][a_i] = 1
        np_array_control_points_coefficient_matrix[i][a_i_plus_one] = 4
        np_array_control_points_coefficient_matrix[i][a_i_plus_two] = 1

    # print(np_array_control_points_coefficient_matrix)

    np_array_pillar_points_matrix = np.zeros(shape=(samples.shape[0], 3))  # 1 vector!

    # x points
    for i in range(samples.shape[0]):
        # calc index
        x_i_plus_one = (i + 1) % samples.shape[0]
        x_i_plus_two = (i + 2) % samples.shape[0]

        # calc other known variable site
        np_array_pillar_points_matrix[i] = (4 * samples[x_i_plus_one]) + (2 * samples[x_i_plus_two])

    # solve the lgs to get a handles
    solved_a_handles = np.array(np.linalg.solve(np_array_control_points_coefficient_matrix, np_array_pillar_points_matrix))
    # print(solved_a_handles)

    # get the b handles
    solved_b_handles = np.zeros(shape=(samples.shape[0], 3))

    for i in range(samples.shape[0]):
        a_i_plus_one = (i + 1) % samples.shape[0]
        # same as a_i_plus_one
        x_i_plus_one = (i + 1) % samples.shape[0]

        solved_b_handles[i] = -solved_a_handles[a_i_plus_one] + 2 * samples[x_i_plus_one]

    p0s = np.zeros(shape=(samples.shape[0], 3))
    p3s = np.zeros(shape=(samples.shape[0], 3))

    for i in range(samples.shape[0]):
        p0s[i] = samples[i]
        x_i_plus_one = (i + 1) % samples.shape[0]
        p3s[i] = samples[x_i_plus_one]

    return p0s, solved_a_handles, solved_b_handles, p3s


def receive_bezier_curve(p0: np.ndarray, p1: np.ndarray, p2: np.ndarray, p3: np.ndarray):
    return lambda t: ((1 - t) ** 3) * p0 + 3 * ((1 - t) ** 2) * t * p1 + 3 * (1 - t) * (t ** 2) * p2 + (t ** 3) * p3


def receive_curve_first_derivative(p0: np.ndarray, p1: np.ndarray, p2: np.ndarray, p3: np.ndarray):
    return lambda t: -3 * p0 * ((1 - t) ** 2) + 3 * p1 * ((1 - t) ** 2) - 6 * p1 * (1 - t) * t + 6 * p2 * (
            1 - t) * t - 3 * p2 * (t ** 2) + 3 * p3 * (t ** 2)


def receive_curve_second_derivative(p0: np.ndarray, p1: np.ndarray, p2: np.ndarray, p3: np.ndarray):
    return lambda t: 6 * p0 * (1 - t) - 12 * p1 * (1 - t) + 6 * p1 * t + 6 * p2 * (1 - t) - 12 * p2 * t + 6 * p3 * t


def receive_curve_third_derivative(p0: np.ndarray, p1: np.ndarray, p2: np.ndarray, p3: np.ndarray):
    return lambda t: -6 * p0 + 12 * p1 + 6 * p1 - 6 * p2 - 12 * p2 + 6 * p3


def curvature_at_t(bezier_cubic_first_derivative, bezier_cubic_second_derivative):
    return lambda t: (np.cross((bezier_cubic_first_derivative(t)), (bezier_cubic_second_derivative(t)))) / np.power(np.linalg.norm(bezier_cubic_first_derivative(t)),3)


def torsion_at_t(bezier_cubic_first_derivative, bezier_cubic_second_derivative, bezier_cubic_third_derivative):
    return lambda t: (np.cross(bezier_cubic_first_derivative(t), bezier_cubic_second_derivative(t)) * bezier_cubic_third_derivative(t)) / np.power(np.linalg.norm(np.cross(bezier_cubic_first_derivative(t), bezier_cubic_second_derivative(t))), 2)


def tangent_at_t(bezier_cubic_first_derivative):
    return lambda t: bezier_cubic_first_derivative(t) / np.linalg.norm(bezier_cubic_first_derivative(t))


def binormal_vector_at_t(bezier_cubic_first_derivative, bezier_cubic_second_derivative):
    return lambda t: np.cross(bezier_cubic_first_derivative(t), bezier_cubic_second_derivative(t)) / np.linalg.norm(np.cross(bezier_cubic_first_derivative(t), bezier_cubic_second_derivative(t)))


def normal_vector_at_t(bezier_cubic_first_derivative, bezier_cubic_second_derivative):
    return lambda t: np.cross(binormal_vector_at_t(bezier_cubic_first_derivative, bezier_cubic_second_derivative)(t), tangent_at_t(bezier_cubic_first_derivative)(t))