import dis
import time

def time_f(func):
        start = time.time()
        func()
        end = time.time()
        dur = end - start
        print("It took: %s "%str(dur))

def time_and_dis(func_1, func_2):
        print("Timing A ")
        time_f(func_1)

        print("\nTiming B ")
        time_f(func_2)

        print("\n Disassemble A ")
        #dis.dis(func_1)

        print("\n Disassemble B ")
        #dis.dis(func_2)

# ############## Array vs Variable ###############
def array_vs_var_a():
    var=[2]
    for i in range(100000000):
        j = i + var[0]


def array_vs_var_b():
    var = 2
    for i in range(100000000):
        j = i + var

# ############ Array vs Tuple ###################
def array_vs_tuple_a():
    var = [2, 2]
    for i in range(100000000):
        j = i + var[0]

def array_vs_tuple_b():
    var = (2, 2)
    for i in range(100000000):
        j = i + var[0]

# ########### While vs For ####################

def while_vs_for_a():

    for i in range(100000000):
        j = 1 + 2

def while_vs_for_b():
     i = 0
     while i < 100000000:
        j = 1 + 2
        i += 1

# ################# Inline vs function ###############
def test_add(a,b):
        return a+b

def inline_vs_function_a():
        a = 1
        b = 2
        for i in range(100000000):
                j = test_add(a,b)

def inline_vs_function_b():
        a = 1
        b = 2
        for i in range(100000000):
                j = a+b 
# ################# Max Element ###############
def index_max_el_a():
        l = list(range(1, 5))
        max_e = 0
        index = -1
        for i in range(1000000):
                for i in range(len(l)):
                        if l[i]>max_e:
                                max_e = l[i]
                                index = i


def index_max_el_b():
        l = list(range(1, 5))
        for i in range(1000000):
                max_e = max(l[3:])
                index = l.index(max_e)

 ############## Setting arrays ###############
def seting_array_a():
    par = 10000000
    var=[0] * (par+1)
    for i in range(par):
        var[i+1]=i


def seting_array_b():
    par = 10000000
    var=[0] 
    for i in range(par):
        var.append(i)

# ############# Setting arrays ###############
def seting_array_str_a():
    par = 100000000
    s = " " * par
    var=[0] * (par+1)
    for i in range(par):
        var[i+1]=s[i]


def seting_array_str_b():
    par = 100000000
    s = " " * par
    s = " "+s
    var=[0] * (par+1)
    for i in range(1, par+1):
        var[i]=s[i]

time_and_dis(seting_array_str_b, seting_array_str_a)
