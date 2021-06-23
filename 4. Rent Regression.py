import pandas as pd
import numpy as np
import seaborn as sns

def main():
    df = get_file()
    x_train, x_test, y_train, y_test = split(df, 0.3)
    b = model(x_train, y_train)
    predictions = fit(x_test, b)
    residuals, SSres = evaluate(predictions, y_test)
    plot_res(residuals, y_test)
    calculate_r(SSres, y_test)
    
def get_file():
    # Get input file
    df = pd.read_csv("Apartments_o.csv")
    df = df[["Rent", "Bond", "Bedroom", "Bathroom", "Heating", "Air Conditioning",
             "Dishwasher", "Gym", "Distance (km) to closest public school",
             "Agent_Besser", "Agent_Biggin", "Agent_Buxton", "Agent_Dingle",
             "Agent_Hodges", "Agent_Home", "Agent_Jellis", "Agent_Marshall",
             "Agent_Paragon", "Agent_Ray", "Agent_Sweeney",
             "Neighbourhood Largest Demographics_20-39", 
             "Neighbourhood Largest Demographics_40-59"]]
    
    return df
    # Get input file

def split(df, ratio):
    
    shuffle = df.sample(frac = 1, random_state = 0)
    ratio = int(0.7 * len(df))
    train_set = shuffle[:ratio]
    test_set = shuffle[ratio:]
    
    # Split data
    x_train = train_set.drop("Rent", axis = 1)
    y_train = train_set[["Rent"]]
    x_test = test_set.drop("Rent", axis = 1)
    y_test = test_set[["Rent"]]
    
    return x_train, x_test, y_train, y_test
    # Split data

def model(x_train, y_train):
    # Estimate regression parameter
    x_train.insert(loc = 0, column='Intercept', value = 1)
    X = x_train.to_numpy()
    Xt = X.transpose()
    XtX = np.matmul(Xt, X)
    
    y = y_train.to_numpy()
    Xty = np.matmul(Xt, y)
    
    b = np.matmul(np.linalg.inv(XtX), Xty).tolist()
    b = [x[0] for x in b]
    
    return b
    # Estimate regression parameter

def fit(x_test, b):
    # Predict test data
    predictions = []
    for i in x_test.index:
        data = x_test.loc[i].tolist()
        y_hat = np.dot(np.array(data), np.array(b[1:])) + b[0]
        predictions.append(y_hat)
        
    return predictions
    # Predict test data

def evaluate(predictions, y_test):
    # Calculating residual sum of squares
    y = y_test["Rent"].tolist()
    res = [x - y[i] for i, x in enumerate(predictions)]
    dist = (np.linalg.norm(np.array(predictions) - np.array(y))) ** 2
    print(f"The residual sum of squares of this prediction is {round(dist, 2)}")
    print(f"The variance is {round(dist/(len(y) - 22), 2)}")
    
    return res, dist
    # Calculating residual sum of squares

def plot_res(residuals, y_test):
    # Plotting residuals for normality check
    y = y_test["Rent"].tolist()
    sns.scatterplot(x = y, y = residuals)
    print("The residual seems to be centered on 0, no evidence of heteroskedasticity")
    # Plotting residuals for normality check

def calculate_r(SSres, y_test):
    # Calculate R-squared and adjusted
    y = y_test["Rent"].tolist()
    Y = np.array(y)
    SStot = np.dot(Y, Y)
    r_squared = 1 - (SSres/(SStot - (sum(y)**2)/len(y)))
    adjusted_r_squared = 1 - ((len(y) - 1) / (len(y) - 22 - 1)) * (1 - r_squared)
    print(f"R-Squared = {round(r_squared, 4)} and Adjusted R-Squared = {round(adjusted_r_squared, 4)}")
    # Calculate R-squared and adjusted
    
main()