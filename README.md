# rent-regression
This is a personal project on data scraping and regression. The goal is to predict weekly rent prices from apartment features. All of the apartments in this data is from Victoria, Australia, I try to keep it close to the CBD to minimise difference in price due to geography. I have 4 codes, which are labelled according to their order. Below is an explanation on each one.


## 1. DataScraping.py
The data is scraped from [domain.com](https://www.domain.com.au/rent/melbourne-region-vic/apartment/), a top real-estate marketplace in Australia.

For the predictors, the features are basically components from apartments (i.e. number of bedrooms, number of bathrooms). The goal is to predict rent prices using these features.

I used BeautifulSoup to scrape the data. I purposedly do not set any precautions to avoid being banned, because at the time I got banned, I have already scraped enough data. 

Note that since BeautifulSoup is an HTML parser, this code may or may not run properly in the future due to changes in website structure. To anticipate, I gave the output of the code in the directory, *Apartments.csv*. Most of the data is fetched using regular expressions. These are also subject to changes in the website.


## 2. Preprocessing.py
This code is for preprocessing, which includes imputation and representation. 
* For missing values, I used median imputation.
* For categorical variable, I kept only 2 fields and do one-hot encodings. I decide to not drop the first/last row, because I will do feature selection in the next code.
The output to this code is *Apartments_c.csv*.


## 3. MS.R
For feature selection, I used stepwise selection using AIC. After finding the optimal features, I did a residual analysis and look at the Cook's distance. I removed all the outliers, refit the model, do stepwise selection again, and obtain a final model. The output to this code is *Apartments_o.csv*.


## 4. RentRegression.py
This is the code for the regression model. I chose to do a linear regression first and then assess the residuals for evidence of non-linearities (I actually knew the result from the previous code, but let's just assume I don't). Estimating the parameters are all done manually using matrix manipulation. In this code, there will be some outputs in the console regarding a few statistical analysis. There is also a residual plot to assess normality. Overall, the model is a good linear fit.


## Recreating
First of all, I do not recommend you run *DataScraping.py*, because it will take hours to days to actually finish domain's apartment collection. I provided the output after experiencing the wait myself, I recommend you use that file instead. If you want to see the code in action, change the output file name, maybe wait for 10 apartments and stop the program. You will still get some data depending on where you stop. The other 3 codes are fine, you can run it directly.

