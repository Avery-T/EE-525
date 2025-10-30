import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

ROUND_BY = 4

def perform_linear_regression(df, column_name):
    """
    Perform least-squares linear regression on a temperature column.
    μ_X[n] = a*n + b
    Returns slope â, intercept b̂, and fitted line ŷ[n].
    """
    # Extract annual values
    y = df[column_name].values
    years = pd.to_datetime(df['Year_Start']).dt.year
    n = np.arange(len(years))

    # Least squares estimation
    a_hat, b_hat = np.polyfit(n, y, 1)
    y_hat = a_hat * n + b_hat

    print(f"Regression for {column_name}:")
    print(f"  â (slope) = {round(a_hat, ROUND_BY)}")
    print(f"  b̂ (intercept) = {round(b_hat, ROUND_BY)}")
    if a_hat > 0:
        print("Temperatures are increasing (â > 0).")
    else:
        print("No increasing trend (â ≤ 0).")
    print()

    return a_hat, b_hat, y_hat, years, y

def plot_regression(years, y, y_hat, column_name, station_name):
    """Plot actual annual data and the fitted regression line."""
    plt.figure(figsize=(8, 5))
    plt.plot(years, y, 'o', label='Annual Data', alpha=0.7)
    plt.plot(years, y_hat, 'r-', label='Least Squares Fit')
    plt.xlabel('Year')
    plt.ylabel(column_name.replace('_', ' '))
    plt.title(f'Linear Trend for {station_name} ({column_name})')
    plt.legend()
    plt.grid(True)
    plt.tight_layout()

def plot_error_sequence(years, y, y_hat, column_name, station_name):
    """Plot the least squares error sequence and compute error variance."""
    e = y - y_hat
    error_variance = np.var(e, ddof=1)  # unbiased sample variance

    plt.figure(figsize=(8, 5))
    plt.plot(years, e, 'o-', color='purple', label='Error e[n]')
    plt.axhline(0, color='gray', linestyle='--')
    plt.xlabel('Year')
    plt.ylabel('Error (°F)')
    plt.title(f'Error Sequence for {station_name} ({column_name})\nVariance = {error_variance:.4f}')
    plt.legend()
    plt.grid(True)
    plt.tight_layout()

    print(f"Error variance for {column_name}: {round(error_variance, ROUND_BY)}\n")

def predict_next_year(a_hat, b_hat, years, column_name):
    """Predict the next year's temperature using the linear regression model."""
    n_next = len(years)
    y_pred_next = a_hat * n_next + b_hat
    year_next = years.iloc[-1] + 2
    print(f"Predicted {column_name} for {year_next}: {round(y_pred_next, ROUND_BY)} °F\n")
    return y_pred_next

def main():
    df = pd.read_csv('./data/LA_annual.csv')
    station_name = df['NAME'].iloc[0]
    
    # Annual max temperature
    a_hat_max, b_hat_max, y_hat_max, years, y_max = perform_linear_regression(df, 'Annual_Max')
    plot_regression(years, y_max, y_hat_max, 'Annual_Max', station_name)
    plot_error_sequence(years, y_max, y_hat_max, 'Annual_Max', station_name)
    predict_next_year(a_hat_max, b_hat_max, pd.Series(years), 'Annual_Max')
    
    # Annual min temperature
    a_hat_min, b_hat_min, y_hat_min, years, y_min = perform_linear_regression(df, 'Annual_Min')
    plot_regression(years, y_min, y_hat_min, 'Annual_Min', station_name)
    plot_error_sequence(years, y_min, y_hat_min, 'Annual_Min', station_name)
    predict_next_year(a_hat_min, b_hat_min, pd.Series(years), 'Annual_Min')
    
    # Average of min and max
    df['Annual_Avg'] = (df['Annual_Max'] + df['Annual_Min']) / 2
    a_hat_avg, b_hat_avg, y_hat_avg, years, y_avg = perform_linear_regression(df, 'Annual_Avg')
    plot_regression(years, y_avg, y_hat_avg, 'Annual_Avg', station_name)
    plot_error_sequence(years, y_avg, y_hat_avg, 'Annual_Avg', station_name)
    predict_next_year(a_hat_avg, b_hat_avg, pd.Series(years), 'Annual_Avg')
    
    plt.show()

main()
