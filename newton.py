from math import ceil, floor, exp, log
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
import matplotlib.animation as animation
def float_round(num, places = 0, direction = floor):
    return direction(num * (10**places)) / float(10**places)

def load_data(file_name,separator=","):
    """Loads the data from a csv

    Args:
    -----
    file_name: str
        Name of the file from which the data should be loaded
    separator: str
        Separator of data in csv
        Defaults to ','

    Returns:
    --------
    time: list(str)
    sensorA: list(float)
    sensorB: list(float)
    avg: float
        Average room temperature
    maxA: float
        Max value of sensor A
    id_max: int
        ID of max value of sensor A
    """
    with open(file_name,'r') as f:
        i = 0
        time = list()
        sensorA = list()
        sensorB = list()
        avg_sum = 0
        maxA = 0
        id_max = 0
        for line in f:
            t,sensa,sensb = line.split(",")
            sensa = float(sensa)
            sensb = float(sensb)
            time.append(t)
            sensorA.append(sensa)
            sensorB.append(sensb)
            avg_sum += sensb
            if sensa >= maxA:
                maxA = sensa
                id_max = i
            i += 1
        return time, sensorA, sensorB, (avg_sum/len(sensorB)), maxA, id_max

def calculate_constants(max,avg,T,t):
    """Calculate C and k

    Args:
    -----
    max: float
        Maximum value of the rod temperature, counted as the T0 for cooling
    avg: float
        Average room temperature
    T: float
        A temperature for k calculation
    t: str
        The time of the T passed

    Returns:
    --------
    C: float
    k: float
    """
    C = max-avg
    k = (log((T-avg)/C)/float(t))
    return C,k

def graph_based_time(name,title,time,*data):
    """Graph some data based on time

    Args:
    -----
    name: str
        Name of the Window
    title: str
        Graph's Title
    time: list()
        Time for x Axis
    *data: list(list())
        Data to be plotted on Y axis
    """
    plt.figure(num=name)
    plt.subplot(title=title)
    i = 0
    colors = ['r','b','g']
    for d in data:
        try:
            plt.plot(time,d,colors[i])
            i+=1
        except Exception as e:
            pass

def calculate_points_ideal(size,id_max,C,k,time):
    """Calculate the points to plot of the ideal change ratio

    Args:
    -----
    size: int
        Wanted number of points
    id_max: int
        Marks the startpoint for calculating the ideal plot
    C: float
        Heat Capacity constant
    k: float
        Proportionallity constant
    time: list()
        Times of the other plots

    Returns:
    --------
    list(float)
        Points to plot
    """
    i_time = 0
    newp = list()
    for x in range(0,size):
        if x == id_max:
            i_time = float(time[x])
        if x < id_max:
            newp.append(avg)
        else:
            t = float(time[x])-i_time
            e = exp((k*t))
            point = C*e + avg
            newp.append(float_round(point,4,floor))
    return newp

time, sensorA, sensorB, avg, maxA, id_max = load_data("temperaturas.csv")
C,k = calculate_constants(maxA,avg,sensorA[300],time[300])
print("Constant C is equal to: {}".format(C))
print("Constant k is equal to {}".format(k))
#Plot Copper rod temperature
graph_based_time("Temperature of Copper","Copper Temperature",time,sensorA)
#Plot Room temperature
graph_based_time("Room Temperature","Room Temperature AVG:{}".format(float_round(avg,2,floor)),time,sensorB)
#Plot comparison
graph_based_time("Comparison","Temperature of Copper MIXED",time,sensorA,sensorB)
#Get New Plot for ideal
newPlot = calculate_points_ideal(len(sensorA),id_max,C,k,time)
graph_based_time("Comparison with ideal","{}*exp({}*t)+{}".format(
    float_round(C,2,floor),float_round(k,2,floor),float_round(avg,2,floor)),
    time,sensorA,sensorB,newPlot)

#Calculate the time until Metal Rod reaches room temperature
t_for_room = 0
calc = 0
while calc != avg or ((avg-1)>calc and calc<(avg+1)):
    t = t_for_room
    e = exp((k*t))
    calc = C*e + avg
    t_for_room += 0.01
print(t_for_room)
print(calc)

#Show plots
plt.tight_layout()
plt.show()
