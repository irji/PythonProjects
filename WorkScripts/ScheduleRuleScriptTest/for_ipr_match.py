import scipy.optimize as optimization
import matplotlib.pyplot as plt
import numpy as np

input_values = np.genfromtxt("FC_LA501_IPR.txt", names=True)
calculated_values = np.genfromtxt("test.txt", names=True)

# for flname in file_names:
#     data = np.genfromtxt(flname, names=True)
#     print(data['BHP'])
#     print(type(data))
#     print(type(target_x_data))


target_x_data = input_values["GAS"]
target_y_data = input_values["BHP"]
calculated_y_data = calculated_values["BHP"]

initial_res_press = target_y_data[0]
# initial_res_press = 2264.1

def func(x, a, f):
    matched_bhp = np.sqrt(initial_res_press ** 2 - a * x - f * x ** 2)
    return matched_bhp


def match():
    fig, ax = plt.subplots(figsize=(15, 7))

    ax.plot(target_x_data, target_y_data, marker='o', markersize=3, label='Измеренная IPR', linewidth=0.0)
    ax.plot(target_x_data, calculated_y_data, label='Расчетная IPR')
    ax.set_xlabel('Q (MMscf/day)', fontsize=18)
    ax.set_ylabel('BHP (psi)', fontsize=18)
    ax.set_title('IPR (до настройки)', fontsize=18)
    ax.grid()
    ax.legend()
    plt.savefig('BeforeMatch.png')

    x0 = ([0.1, 0.1])
    popt, pcov = optimization.curve_fit(func, target_x_data, target_y_data, p0=x0)

    print("Были подобраны значения: A = %5.3f, F = %5.3f" % tuple(popt))

    fig, ax = plt.subplots(figsize=(15, 7))
    ax.plot(target_x_data, target_y_data, marker='o', markersize=10, label='Измеренная IPR', linewidth=0.0)
    ax.plot(target_x_data, calculated_y_data, label='Расчетная IPR')
    ax.plot(target_x_data, func(target_x_data, *popt), label='Настроенная IPR: A=%5.3f, F=%5.3f' % tuple(popt))
    ax.set_xlabel('Q (MMscf/day)', fontsize=18)
    ax.set_ylabel('BHP (psi)', fontsize=18)
    ax.set_title('IPR (после настройки)', fontsize=18)
    ax.grid()
    ax.legend()
    plt.savefig('AfterMatch.png')


match()