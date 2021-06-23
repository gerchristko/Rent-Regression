import pandas as pd
import numpy as np
from sklearn.impute import SimpleImputer

def get_file():
    df = pd.read_csv("Apartments.csv")
    df.dropna(subset = ["Address"], inplace = True)
    
    return df

def preprocess(df):
    # Impute missing values
    col = "Distance (km) to closest public school"
    imputer = SimpleImputer(missing_values = np.nan, strategy = 'median')
    imputer.fit(df[[col]])
    df[col] = imputer.transform(df[[col]])
    imputer.fit(df[["Bond"]])
    df["Bond"] = imputer.transform(df[["Bond"]])
    # Impute missing values
    
    # Delete unecessary data
    del df["Address"], df["Suburb"], df["Code"], df["State"]
    # Delete unecessary data
     
    # Agent data preprocess
    agents = df["Agent"].tolist()
    symbols = "{}()[].,;+*/&|<>=~$…?!'"
    agents = [x.translate({ord(sym): None for sym in symbols} ).strip() for x in agents]
    agents = [x.split(" ")[0] for x in agents]
    df["Agent"] = agents
    # Agent data preprocess
    
    # One hot encoding
    df = pd.get_dummies(df)
    df.set_index("Rent", inplace = True)
    # One hot encoding
    
    return df

def output(df):
    FILENAME = "Apartments_c.csv"
    file = open(FILENAME, "w+")
    df.to_csv(FILENAME)
    file.close()
    
def main():
    df = get_file()
    df = preprocess(df)
    output(df)

main()