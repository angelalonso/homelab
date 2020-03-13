import enum
import itertools
import psutil
import string
import sys
import os

'''
Tasks:
    Get the current available memory and define a limit of 1/4 of that
    Build an array of possible combinations, starting by X until the size of the program reaches that limit
    Save the current state and exit
    Load that state and continue
'''


MEM_LIMIT = psutil.virtual_memory().available // 2 # these are bytes

#DICTIO = string.digits
DICTIO = string.ascii_letters + string.digits + string.punctuation

# Enum for size units
class SIZE_UNIT(enum.Enum):
   BYTES = 1
   KB = 2
   MB = 3
   GB = 4
 
 
def convert_unit(size_in_bytes, unit):
   """ Convert the size from bytes to other units like KB, MB or GB"""
   if unit == SIZE_UNIT.KB:
       return size_in_bytes // 1024
   elif unit == SIZE_UNIT.MB:
       return size_in_bytes // (1024*1024)
   elif unit == SIZE_UNIT.GB:
       return size_in_bytes // (1024*1024*1024)
   else:
       return size_in_bytes


def getUsage():
    pid = os.getpid()
    py = psutil.Process(pid)
    memoryUse = py.memory_info()[0]
    print(str(convert_unit(memoryUse, SIZE_UNIT.MB)) + "MB Mem")


def writeToDisk(data, filename):
    filehandle = open(filename, "w")
    for line in data:
        filehandle.write(line + "\n")
    filehandle.close()


def generate(initial_list, dictionary, size):
    build_list = []
    final = []
    if len(initial_list) == 0:
        for char in dictionary:
            build_list.append(str(char))
    else:
        for entry in initial_list:
            #print(psutil.virtual_memory().available)
            for char in dictionary:
                build_list.append(entry + str(char))
    if len(build_list[0]) < size:
        print("generated length: " + str(len(build_list[0])))
        build_list = generate(build_list, dictionary, size)[:]

    return build_list



if __name__ == '__main__':
    print(str(convert_unit(MEM_LIMIT, SIZE_UNIT.MB)) + " MBytes available")
    #generateCombinations(DICTIO, 2)
    DICTIO = '123456'
    #first = retrofeed([], list(DICTIO))[:]
    #second = retrofeed(first, list(DICTIO))[:]
    #third = retrofeed(second, list(DICTIO))[:]
    #fourth = retrofeed(third, list(DICTIO))[:]
    #print(fourth)

    list_out = generate([], list(DICTIO), 9)[:]
    writeToDisk(list_out, 'out.txt')
