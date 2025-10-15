import pandas as pd 
import matplotlib.pyplot as plt 
import math

ROUND_BY=3 

def compute_mean(x):
    length = x.count() # .count() counts non-NaN numbers so its safe
    sum = 0
    for i in x: 
        if not math.isnan(i):
            sum = sum + i
    mean = sum / length 
    return  round(mean, ROUND_BY)

def compute_variance(x): 
    mean = compute_mean(x)
    squared_difference_sum = 0
    length = x.count() 
    for i in x: 
        if not math.isnan(i):
            squared_difference_sum = squared_difference_sum + ( (i - mean)**2) 
        
    variance =  squared_difference_sum / (length - 1)
    
    return round(variance, ROUND_BY)


def compute_covariance(x,y):
    len_x = x.count()
    len_y = y.count()
    length = len_x
    # one could have more data than the other so use the smallest
    if(len_x > len_y ):
        length = len_y 
    
    mean_x =compute_mean(x)
    mean_y = compute_mean(y) 
    sum = 0
    
    for i in range(length): 
        if not math.isnan(x[i]) and not math.isnan(y[i]):
            sum = sum + (x[i] - mean_x + y[i] -mean_y)
    
    covarance = sum / (length -1)
    return round(covarance, ROUND_BY)
 
def print_covariance_matrix(x,y,z):
     cov_matrix = [ [compute_variance(x),compute_covariance(x,y),compute_covariance(x,z)],
                   [compute_covariance(x,y),compute_variance(y),compute_covariance(y,z)],
                   [compute_covariance(x,z),compute_covariance(y,z),compute_variance(z)]] 
     print("Covariance Matrix ") 
     print(cov_matrix)            

def plot_temp_time_series_data(df): 
    plt.figure()
    df[['TMIN','TMAX','TAVG']].plot(figsize=(10,6))
    plt.xlabel('Time')
    plt.ylabel('Temp')
    plt.legend()
    plt.title("Temprature vs Time")
    pass 

def plot_time_prcp(df): 
    plt.figure()
    df['PRCP'].plot(figsize=(10,6))
    plt.xlabel('Time')
    plt.ylabel('Precipitation')
    plt.title("Precipitation vs Time")
    plt.legend()


    
def plot_histograms(df): 
    
    tmin_mean = compute_mean(df['TMIN'])
    tmax_mean = compute_mean(df['TMAX'])
    tavg_mean = compute_mean(df['TAVG'])
    prcp_mean = compute_mean(df['PRCP'])
    
    tmin_variance = compute_variance(df['TMIN'])
    tmax_variance = compute_variance(df['TMAX'])
    tavg_variance = compute_variance(df['TAVG'])
    prcp_variance = compute_variance(df['PRCP'])
    
    fig, axes = plt.subplots(2, 2, figsize=(12, 10))
    axes = axes.flatten() 
    df['TMIN'].hist(ax=axes[0], bins=20)
    df['TMAX'].hist(ax=axes[1], bins=20)
    df['TAVG'].hist(ax=axes[2], bins=20)
    df['PRCP'].hist(ax=axes[3], bins=20)
    
  
    
    axes[0].set_title(fr'Histogram of TMIN $\sigma^2 = {tmin_variance}$, $\mu = {tmin_mean}$')
    axes[1].set_title(fr'Histogram of TMAX $\sigma^2 = {tmax_variance}$, $\mu = {tmax_mean}$')
    axes[2].set_title(fr'Histogram of TAVG $\sigma^2 = {tavg_variance}$, $\mu = {tavg_mean}$')
    axes[3].set_title(fr'Percipitation $\sigma^2 = {prcp_variance}$, $\mu = {prcp_mean}$' )
    
    for ax in axes:
        ax.set_xlabel('Value')
        ax.set_ylabel('Frequency')
    plt.tight_layout()
 

def main(): 
    
    df = pd.read_csv('./data/slo_temp_test.csv')
    df['DATE'] = pd.to_datetime(df['DATE'])
    df.set_index('DATE',inplace=True) # To use the Date as the X axis
    plot_temp_time_series_data(df)
    plot_time_prcp(df)
    plot_histograms(df)
    print_covariance_matrix(df['TMAX'],df['TAVG'],df['PRCP'])
    plt.show()   
main()
