import matplotlib.pyplot as plt
import statistics

from data_configurator import data_configurator as dc
from interval_analysis import interval_analysis as ia

def to_intervals(data: [], eps):
    intervals = []

    for value in data:
        intervals.append([round(value - eps, 5), round(value + eps, 5)]) 
    
    return intervals

def plot(y: [], x : [],  title, save_dst):
    for i in range(len(y)):
        plt.plot([x[i], x[i]], y[i], 'b')

    plt.title(title)
    plt.savefig(save_dst + title + '.png')
    plt.clf()
        
def plot_regression(x : [], y: [], b0, b1, title, save_dst):
    for i in range(len(y)):
        plt.plot([x[i], x[i]], y[i], 'b')

    plt.plot([x[0], x[len(x) - 1]], [b1 * x[0] + b0, b1 * x[len(x) - 1] + b0], 'y')

    plt.title(title)
    plt.savefig(save_dst + title + '.png')
    plt.clf()

def plot_corridor(x : [], y: [], inform, b0, b1, title, save_dst):
    y_min, y_max = [], []
    extended_x = [-1.0] + x + [1.0]
    for value_x in extended_x:
        value_y = [inform.exterior.xy[1][i]+ inform.exterior.xy[0][i] * value_x for i in range(len(inform.exterior.xy[1]))]
        y_min.append(min(value_y))
        y_max.append(max(value_y))
    plt.fill_between(extended_x, y_min, y_max, alpha=0.3)
    plt.plot(extended_x, y_min, linewidth = 0.5)
    plt.plot(extended_x, y_max,  linewidth = 0.5)

    for i in range(len(y)):
        plt.plot([x[i], x[i]], y[i], 'b')

    plt.plot([x[0], x[len(x) - 1]], [b1 * x[0] + b0, b1 * x[len(x) - 1] + b0], 'y')

    plt.title(title)
    plt.savefig(save_dst + title + '.png')
    plt.clf()

def plot_information_set(rec, b0, b1, title, save_dst):
    vertecies = rec.exterior.xy

    for i in range(len(vertecies[0]) - 1):
        plt.plot([vertecies[0][i], vertecies[0][i + 1]], [vertecies[1][i], vertecies[1][i + 1]], 'y')
    
    plt.scatter(b1, b0, label="b1, b0")

    plt.xlabel('beta_1')
    plt.ylabel('beta_0')

    plt.legend()
    plt.title(title)
    plt.savefig(save_dst + title + '.png')
    plt.clf()

def analysis(x, y, name, img_save_dst):
    lr = ia.linear_regression(x, y)
    b_0_p = lr[-2] 
    b_1_p = lr[-1]

    print(b_0_p, b_1_p)

    plot_regression(x, y, b_0_p, b_1_p, 'Regression ' + name, img_save_dst)
    b0, b1, rec = ia.find_beta(x, y, [0.7, 1.0])

    print(b0, b1)

    plot_information_set(rec, b_0_p, b_1_p, 'Inform ' + name, img_save_dst)

    plot_corridor(x, y, rec, b_0_p, b_1_p, 'Corridor ' + name, img_save_dst)


if __name__ == '__main__':
    img_save_dst = './report/img/'
    eps1 = 0.03125
    eps2 = 0.03125

    x = [-0.5, -0.25, +0.25, +0.5]
    dir_names = ['-0_5', '-0_25', '+0_25', '+0_5']

    y_1 = []
    y_2 = []

    for name in dir_names:
        data = dc.get_data('./' + name + 'V/' + name + 'V_13.txt', './ZeroLine/ZeroLine_13.txt')
        intervals = to_intervals(data, eps1)
        max_mode_ind, _, zones, _ = ia.mode(intervals)
        y_1.append([zones[max_mode_ind[0]], zones[max_mode_ind[0] + 1]])
    
    plot(y_1, x, 'X, (Y1)', img_save_dst)

    for name in dir_names:
        med = statistics.median(dc.get_data('./' + name + 'V/' + name + 'V_13.txt', './ZeroLine/ZeroLine_13.txt'))
        interval = to_intervals([med], eps2)
        y_2.append(interval[0])
    
    plot(y_2, x, 'X, (Y2)', img_save_dst)

    analysis(x, y_1, 'X, (Y1)', img_save_dst)
    analysis(x, y_2, 'X, (Y2)', img_save_dst)
