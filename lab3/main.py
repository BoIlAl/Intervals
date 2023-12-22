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

def plot_corridor(x : [], y: [], inform, b0, b1, title, save_dst):
    y_min, y_max = [], []
    extended_x = [-0.55] + x + [0.55]
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

    return y_min, y_max

def plot_status_diagram(y, y_min, y_max, title, save_dst):
    r = []
    l = []

    for i in range(len(y)):
        r.append((ia.mid(y[i]) - ia.mid([y_min[i + 1], y_max[i + 1]])) / ia.rad(y[i]))
        l.append(ia.rad([y_min[i + 1], y_max[i + 1]]) / ia.rad(y[i]))

    plt.fill_between((0, 1), (1, 0), (-1, 0), alpha=0.5, label='internal', color = 'g')
    plt.fill_between((0, 1), (-1, -2), (-1, 0), alpha=0.5, label='external', color='y')
    plt.fill_between((0, 1), (1, 0), (1, 2), alpha=0.5, color='y')
    plt.fill_between((1, 2), (-2, -3), (2, 3), alpha=0.5, color='y')
    plt.fill_between((0, 2), (1, 3), (3, 3), alpha=0.5, label='outliers', color='r')
    plt.fill_between((0, 2), (-3, -3), (-1, -3), alpha=0.5, color='r')

    r_edge = [-3, 0, 3]

    plt.plot([1-abs(ri) for ri in r_edge], r_edge, color='k', linewidth=1)
    plt.plot([abs(ri)-1 for ri in r_edge], r_edge, color='k', linewidth=1)
    plt.plot([1, 1], [-3, 3], '--', color='b')
    plt.plot(l, r, 'o', color='b')

    for i in range(len(r)):
        plt.annotate(str(i + 1), (l[i]+0.04, r[i]+0.04))
        if(abs(r[i])>=l[i]+1):
            print('outlier ', i)
        elif(abs(r[i])< 1 - l[i]):
            print('internal ', i)
        elif(abs(r[i])==1 - l[i]):
            print('edge ', i)
        elif(abs(r[i])>1 - l[i]):
            print('external ', i)
    
    plt.legend()
    plt.xlim(0, 2)
    plt.ylim(-3, 3)
    plt.xlabel('l')
    plt.ylabel('r')
    
    plt.savefig(save_dst + title + '.png')

    plt.clf()

def analysis(x, y, name, img_save_dst):
    lr, new_y = ia.linear_regression(x, y)

    plot_regression(x, y, lr[-2], lr[-1], 'Regression ' + name, img_save_dst)

    _, _, rec = ia.find_beta(x, new_y, [10000, 20000])

    plot_information_set(rec, lr[-2], lr[-1], 'Inform ' + name, img_save_dst)

    y_min, y_max = plot_corridor(x, y, rec, lr[-2], lr[-1], 'Corridor ' + name, img_save_dst)

    plot_status_diagram(y, y_min, y_max, 'Status diagram ' + name, img_save_dst)


if __name__ == '__main__':
    img_save_dst = './report/img/'

    sp = [31, 670, 484, 831, 547,
           321, 9, 320, 300, 176]
    sp_zero = 812

    eps1 = 600
    eps2 = 125

    x = [-0.45, -0.35, -0.25, -0.15, -0.05, 0.05, 0.15, 0.25, 0.35, 0.45]

    y_1 = []
    y_2 = []

    for i in range(len(x)):
        data = dc.get_data('./rawData/' + str(x[i]) + 'V_sp' + str(sp[i]) + '.dat', './rawData/0.0V_sp' + str(sp_zero) + '.dat', sp[i], sp_zero)
        intervals = to_intervals(data, eps1)
        max_mode_ind, _, zones, _ = ia.mode(intervals)
        y_1.append([zones[max_mode_ind[0]], zones[max_mode_ind[0] + 1]])
    
    plot(y_1, x, 'X, (Y1)', img_save_dst)

    for i in range(len(x)):
        med = statistics.median(dc.get_data('./rawData/' + str(x[i]) + 'V_sp' + str(sp[i]) + '.dat', './rawData/0.0V_sp' + str(sp_zero) + '.dat', sp[i], sp_zero))
        interval = to_intervals([med], eps2)
        y_2.append(interval[0])
    
    plot(y_2, x, 'X, (Y2)', img_save_dst)

    analysis(x, y_1, 'X, (Y1)', img_save_dst)
    analysis(x, y_2, 'X, (Y2)', img_save_dst)
