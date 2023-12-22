from shapely.geometry import Polygon
from scipy.optimize import linprog

class interval_analysis:
    @staticmethod
    def mode(intervals: []):
        zones = []

        for interval in intervals:
            zones.append(interval[0])
            zones.append(interval[1])

        zones = list(set(zones))

        zones.sort()

        mode_values = [0 for _ in range(len(zones) - 1)]

        values = []

        for i in range(len(zones) - 1):
            for interval in intervals:
                value = (zones[i] + zones[i + 1]) / 2
                if interval[0] <= zones[i] and interval[1] >= zones[i + 1]:
                    values.append(value)
                    mode_values[i] += 1
        
        max_values = max(mode_values)

        max_mode_ind = []

        for i in range(len(mode_values)):
            if (mode_values[i] == max_values):
                max_mode_ind.append(i)
        
        return max_mode_ind, mode_values, zones, values
    
    @staticmethod
    def __rectangle(x, y : [], border : []):
        rec = Polygon((
            (border[0], y[0] - border[0] * x),
            (border[0], y[1] - border[0] * x),
            (border[1], y[1] - border[1] * x),
            (border[1], y[0] - border[1] * x)
        ))
        return rec

    @staticmethod
    def find_beta(x: [], y: [], border: []): 
        rec = interval_analysis.__rectangle(x[0], y[0], border)
        for i in range(1, len(x)):
            rec = rec.intersection(interval_analysis.__rectangle(x[i], y[i] ,border))
        vertecies = rec.exterior.xy
        beta_0 =[min(vertecies[1]), max(vertecies[1])]    
        beta_1 =[min(vertecies[0]), max(vertecies[0])]    
        return beta_0, beta_1, rec

    @staticmethod
    def __left_part(x, y):
        n = len(x)
        lp = []
        for i in range(n):
            lp_i = [0] * (n + 2)
            lp_i[i], lp_i[n], lp_i[n + 1] = -abs(y[i][1] - y[i][0]) / 2, 1, x[i]
            lp.append(lp_i)
        for i in range(n):
            lp_i = [0] * (n + 2)
            lp_i[i], lp_i[n], lp_i[n + 1] = -abs(y[i][1] - y[i][0]) / 2, -1, -x[i]
            lp.append(lp_i)
        return lp

    @staticmethod
    def __right_part(y):
        rp = []
        for value in y:
            rp.append((value[0] + value[1]) / 2)
        for value in y:
            rp.append(-(value[0] + value[1]) / 2)
        return rp

    @staticmethod
    def linear_regression(x, y):
        target_function = [1]*len(x) + [0, 0]
        lp = interval_analysis.__left_part(x, y)
        rp = interval_analysis.__right_part(y)
        answer = linprog(c=target_function, A_ub=lp, b_ub=rp, method="highs")
        return answer.x