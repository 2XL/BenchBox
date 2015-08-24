#!/bin/python

import numpy

def read_file_data(filepath):

    cpu_values = []
    
    with open(filepath) as f:
        i = 1
        values_in_second = []
        for line in f:
            cpu_value = float(line)
            values_in_second.append(cpu_value)
            
            if (i%10 == 0):
                mean_second = numpy.mean(values_in_second)
                cpu_values.append(mean_second)
                # start another second...
                i = 0
                values_in_second = []
            i += 1
        
    return cpu_values

    
def calculate_mean(results):
    file_sizes = results.keys()
    file_sizes.sort()
    means = dict()
    for size in file_sizes:
        times = results.get(size)
        mean = sum(times)/len(times)
        means[size] = mean
    
    return means
        
def print_results_to_file(values, filename):
    with open(filename, 'w') as f:
        for value in values:
            f.write(str(value)+"\n")
        

#for provider in ["dropbox", "box", "gdrive"]:
#    for test in ["normal", "shared"]:
#        print provider
#        results = read_file_data("./data_5days/"+provider+"/"+test+"/metadata.log")
#        print_results_to_file(results, provider+"_"+test+"_5days.dat")
        
cpu_values = read_file_data("./data/dropbox_cpu.dat")
print_results_to_file(cpu_values, "dropbox_cpu_1sec_mean.dat")

cpu_values = read_file_data("./data/box_cpu_long.dat")
print_results_to_file(cpu_values, "box_cpu_long_1sec_mean.dat")

cpu_values = read_file_data("./data/box_cpu.dat")
print_results_to_file(cpu_values, "box_cpu_1sec_mean.dat")

cpu_values = read_file_data("./data/gdrive_cpu.dat")
print_results_to_file(cpu_values, "gdrive_cpu_1sec_mean.dat")

cpu_values = read_file_data("./data/onedrive_cpu.dat")
print_results_to_file(cpu_values, "onedrive_cpu_1sec_mean.dat")
