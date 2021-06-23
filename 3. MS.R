library(tidyverse)
library(MASS)

df <- read_csv("Apartments_c.csv")

model <- lm(Rent ~ ., data = df)
smodel <- stepAIC(model, direction = "both", trace = FALSE)

plot(smodel, which = 4)
cooksd <- cooks.distance(smodel)
influential <- as.numeric(names(cooksd) [cooksd > 0.01])
influential <- influential[!is.na(influential)]

new_df <- df[-influential,]
nmodel <- lm(Rent ~ ., data = new_df)
nsmodel <- stepAIC(nmodel, direction = "both", trace = FALSE)

write.csv(new_df,"Apartments_o.csv", row.names = TRUE)
(final.model <- summary(nsmodel))
