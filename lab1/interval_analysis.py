class interval_analysis:
    @staticmethod
    def __findK(interval_1: [], interval_2: []):
        if interval_1[0] > interval_2[1]:
            return (interval_1[0] - interval_2[1]) / (interval_1[1] - interval_1[0] + interval_2[1] - interval_2[0])
        elif interval_2[0] > interval_1[1]:
            return (interval_2[0] - interval_1[1]) / (interval_1[1] - interval_1[0] + interval_2[1] - interval_2[0])
        else:
            return 0
    
    @staticmethod
    def assessments(intervals: []):
        external = intervals[0].copy()
        internal = intervals[0].copy()

        k = 0

        for i in range(len(intervals)):
            if i == 0:
                first_interval = intervals[i]
            elif i == 1:
                second_interval = intervals[i]
                k = interval_analysis.__findK(first_interval, second_interval)
            else:
                k_f = interval_analysis.__findK(first_interval, intervals[i])
                k_s = interval_analysis.__findK(second_interval, intervals[i])

                if k_s <= k_f > k:
                    k = k_f
                    second_interval = intervals[i]
                elif k_f <= k_s > k:
                    k = k_s
                    first_interval = intervals[i]

            if intervals[i][0] < external[0]:
                external[0] = intervals[i][0]
            if intervals[i][1] > external[1]:
                external[1] = intervals[i][1]
            if intervals[i][0] > internal[0]:
                internal[0] = intervals[i][0]
            if intervals[i][1] < internal[1]:
                internal[1] = intervals[i][1]

        return external, internal, k

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
    def JС(external: [], internal: []):
        return (internal[1] - internal[0]) / (external[1] - external[0])

    @staticmethod
    def mid(external: []):
        return (external[1] + external[0]) / 2

    @staticmethod
    def RIn_ROut(external_1: [], internal_1: [], external_2: [], internal_2: []):
        return [internal_1[0] / internal_2[1], internal_1[1] / internal_2[0]], [external_1[0] / external_2[1], external_1[1] / external_2[0]]

    @staticmethod
    def mult_measure(jc, k, max_mode, size):
        return (1 + jc) / 2 * max_mode / size / (1 + k)