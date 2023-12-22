import matplotlib.pyplot as plt
import numpy as np

from data_configurator import data_configurator as dc
from interval_analysis import interval_analysis as ia


def sum_signals(signal_1: [], signal_2: [], R):
    new = signal_1.copy()
    for interval in signal_2:
        if (R < 0):
            new.append([R * interval[1], R * interval[0]])
        else:
            new.append([R * interval[0], R * interval[1]])
       
    return new

def to_intervals(data: []):
    eps = 0.000061
    intervals = []

    for value in data:
        intervals.append([round(value - eps, 5), round(value + eps, 5)]) 
    
    return intervals

def plot_intervals(intervals: [], external, internal, title, save_dst):
    i = 0
    for interval in intervals:
        plt.plot([i, i], interval, 'b')
        i += 1

    plt.plot([0, len(intervals) - 1], [external[0], external[0]], 'y')
    plt.plot([0, len(intervals) - 1], [external[1], external[1]], 'y')
    plt.plot([0, len(intervals) - 1], [internal[0], internal[0]], 'r')
    plt.plot([0, len(intervals) - 1], [internal[1], internal[1]], 'r')

    plt.title(title)
    plt.savefig(save_dst + title + '.png')
    plt.clf()
        
def plot_mode_hist(zones, values, title, save_dst):
    plt.hist(values, bins=zones)

    plt.title(title)
    plt.savefig(save_dst + title + '.png')
    plt.clf()

def plot(x: [], y: [], title, xlabel, ylabel, save_dst):
    plt.plot(x, y)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.savefig(save_dst + title + '.png')
    plt.clf()

def print_measures(ext, int, k, max_mode, signal_size):
    jc = ia.JС(ext, int)
    print('JC = ' + str(jc))
    print('k = ' + str(k))
    print('maxmu = ' + str(max_mode))
    print('mult_measure = ' + str(ia.mult_measure(jc, k, max_mode, signal_size)))


def find_optimal_R(signal_1:[], signal_2: [], Rs: [], title, save_dst):
    jcs = []
    ks = []
    modes = []
    mm = []

    opt_JC = -1
    opt_maxmu = 0
    opt_k = 1000
    opt_MM = 0

    eps = 0.0000001

    for R_ in Rs:
        sum_signal = sum_signals(signal_1, signal_2, R_)

        ext, int, k = ia.assessments(sum_signal)
        max_mode_ind, mode_values, _, _ = ia.mode(sum_signal)

        jc = ia.JС(ext, int)
        max_mode = mode_values[max_mode_ind[0]]
        mult_m = ia.mult_measure(jc, k, max_mode, len(sum_signal))

        if jc > opt_JC:
            opt_JC = jc
            R_opt_JC = [R_, R_]
        elif jc + eps > opt_JC:
            R_opt_JC[1] = R_

        if max_mode > opt_maxmu:
            opt_maxmu = max_mode
            R_opt_maxmu = [R_, R_]
        elif max_mode == opt_maxmu:
            R_opt_maxmu[1] = R_

        if k < opt_k:
            opt_k = k
            R_opt_k = [R_, R_]
        elif k - eps < opt_k:
            R_opt_k[1] = R_
        
        if mult_m > opt_MM:
            opt_MM = mult_m
            R_opt_MM = [R_, R_]
        elif mult_m == opt_MM:
            R_opt_MM[1] = R_

        ks.append(k)
        jcs.append(jc)
        modes.append(max_mode)
        mm.append(mult_m)

    print('jc optimal = ' + str(opt_JC))
    print('R jc optimal = ' + str(R_opt_JC))
    print('maxmu optimal = ' + str(opt_maxmu))
    print('R maxmu optimal = ' + str(R_opt_maxmu))
    print('k optimal = ' + str(opt_k))
    print('R k optimal = ' + str(R_opt_k))
    print('mm optimal = ' + str(opt_MM))
    print('R mm optimal = ' + str(R_opt_MM))
    
    plot(Rs, jcs, title + ' JС', "R", "Jaccard", save_dst)
    plot(Rs, ks, title + ' k', "R", "k", save_dst)
    plot(Rs, modes, title + ' maxmu', "R", "maxmu", save_dst)
    plot(Rs, mm, title + ' mult measure', "R", "mult measure", save_dst)

def analysis(signal_1:[], signal_2: [], deltR, N, title_1, title_2, save_dst):
    ext_1, int_1, k_1 = ia.assessments(signal_1)
    ext_2, int_2, k_2 = ia.assessments(signal_2)
    max_mode_ind_1, mode_values_1, zones_1, values_1 = ia.mode(signal_1)
    max_mode_ind_2, mode_values_2, zones_2, values_2 = ia.mode(signal_2)

    plot_intervals(signal_1, ext_1, int_1, title_1, save_dst)
    plot_intervals(signal_2, ext_2, int_2, title_2, save_dst)
    plot_mode_hist(zones_1, values_1, title_1 + " mode hist", save_dst)
    plot_mode_hist(zones_2, values_2, title_2 + " mode hist", save_dst)

    print_measures(ext_1, int_1, k_1, mode_values_1[max_mode_ind_1[0]], len(signal_1))
    print_measures(ext_2, int_2, k_2, mode_values_2[max_mode_ind_2[0]], len(signal_2))

    RIn, ROut  = ia.RIn_ROut(ext_1, int_1, ext_2, int_2)
    print('R = ' + str([RIn, ROut]))
    print('mid(RIn) = ' + str(abs(RIn[1] - RIn[0])))
    print('mid(ROut) = ' + str(abs(ROut[1] - ROut[0])))

    if (ROut[1] > ROut[0]):
        R = ROut.copy()
    else:
        R = [ROut[1], ROut[0]]
            
    delt = (R[1] - R[0] + 2 * deltR)  / N
    Rs = np.arange(R[0] - deltR, R[1] + deltR, delt)
    return Rs

if __name__ == '__main__':
    img_save_dst = "./report/img/"

    data_1 = dc.get_data('./+0_5V/+0_5V_13.txt', './ZeroLine/ZeroLine_13.txt')
    data_2 = dc.get_data('./-0_5V/-0_5V_13.txt', './ZeroLine/ZeroLine_13.txt')
    signal_1 = to_intervals(data_1)
    signal_2 = to_intervals(data_2)

    Rs = analysis(signal_1, signal_2, 0.02, 100, "signal 1", "signal 2", img_save_dst)
    find_optimal_R(signal_1, signal_2, Rs, "sum signal", img_save_dst)