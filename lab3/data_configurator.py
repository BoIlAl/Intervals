class data_configurator:
    @staticmethod
    def read_data(fileName):
        data = []
        with open(fileName) as f:
            for line in f:
                data.append(line)
        return data
    
    @staticmethod
    def shift_data(data: [], shift):
        new_data = []
        for line in data:
            split = line.split()
            if len(split) == 0:
                continue
            new_data.append(float(split[1])) 

        new_data = new_data[shift:] + new_data[:shift]
        
        return new_data
    
    @staticmethod
    def clear_data(data: [], zero_filename, shift_zero):
        zero_data = data_configurator.shift_data(data_configurator.read_data(zero_filename), shift_zero)

        new_data = []

        for i in range(len(data)):
            new_data.append(data[i] - zero_data[i])
        
        return new_data
    
    @staticmethod
    def get_data(fileName, zero_filename, shift, shift_zero):
        data = data_configurator.shift_data(data_configurator.read_data(fileName), shift)
        return data_configurator.clear_data(data, zero_filename, shift_zero)

