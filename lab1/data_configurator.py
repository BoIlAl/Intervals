class data_configurator:
    @staticmethod
    def read_data(fileName):
        data = []
        with open(fileName) as f:
            for line in f:
                data.append(line)
        return data
    
    @staticmethod
    def shift_data(data: []):
        new_data = []
        i = 0
        shift = 1024
        for line in data:
            if i == 0:
                split = line.split()
                shift -= int(split[3])
                i += 1
                continue

            split = line.split()
            new_data.append(float(split[1])) 
            i += 1

        new_data = new_data[shift:] + new_data[:shift]
        
        return new_data
    
    @staticmethod
    def clear_data(data: [], zero_filename):
        zero_data = data_configurator.shift_data(data_configurator.read_data(zero_filename))

        new_data = []

        for i in range(len(data)):
            new_data.append(data[i] - zero_data[i])
        
        return new_data
    
    @staticmethod
    def get_data(fileName, zero_filename):
        data = data_configurator.shift_data(data_configurator.read_data(fileName))
        return data_configurator.clear_data(data, zero_filename)
