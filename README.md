# Experiments-Instacart-Data
Experiments to evaluate the performance of a bayesian predictor

>*Whether you shop from meticulously planned grocery lists or let whimsy guide your grazing, our unique food rituals define who we are. Instacart, a grocery ordering and delivery app, aims to make it easy to fill your refrigerator and pantry with your personal favorites and staples when you need them. After selecting products through the Instacart app, personal shoppers review your order and do the in-store shopping and delivery for you.*
>
>*Instacart’s data science team plays a big part in providing this delightful shopping experience. Currently they use transactional data to develop models that predict which products a user will buy again, try for the first time, or add to their cart next during a session. Recently, Instacart open sourced this data - see their blog post on 3 Million Instacart Orders, Open Sourced.*
>
>*In this competition, Instacart is challenging the Kaggle community to use this anonymized data on customer orders over time to predict which previously purchased products will be in a user’s next order.*


The original project, as described on Kaggle, is about using the order data (i.e. set of products purchased and meta data) of the customers to predict their next order. My goal behind this project is to explore a bayesian predicting model I have been thinking of lately. 

Specifically, I am trying to answer the following question:
**How does a *simple* bayesian model that uses only the order history of the customer perform?** 

There are a couple of things I need to explain about the above statement. 
1. The model is *simple* in the sense that it discards most of the secondary information like at what time of the day or what day of the week the order was made. I am implicitly assuming that these parameters don't play any role. Of course, that need not be true.
2. The model is bayesian, i.e. for each customer we compute a posterior distribution and the products predicted are simply a sample from this distribution.

The description of the data and the goal of the orginal project is given in detail on the project website https://www.kaggle.com/c/instacart-market-basket-analysis

Find a more detailed discussion in the Jupyter Notebook.
