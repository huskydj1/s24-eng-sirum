# SIRUM: Medication Data Pipeline
## Description:

The result of a partnership between SIRUM and Harvard's Tech for Social Good, this codebase automates the manual browsing of customer testimonials/complaints with respect to inaccessible medication. For further information about our process and product, please refer to our [documentation.](https://docs.google.com/document/d/17cENcQ5N6iJk_WG745-28ZXjmQD__uuq0s-iVYZxSqI/edit?usp=sharing)

The scripts provided have been specifically designed for GoFundMe pages, as we found most success analyzing its pages when compared with Reddit, Quora, Facebook, and the National Institute of Health. However, the scripts may be tailored towards other sites by modifying `scrapePages.py`, specifically the tags passed into the `presence_of_element_located` function. 

## Setup

Due to package requirements, we encourage users to run our code using Python 3.9. Dependencies may be installed by running the following code in your terminal: 

```
pip install -r requirements.txt
```

Should also add API keys 

## Scripts

- **Scraping Links**
- **Scraping Pages**
- **Analyzing Sentiment**
- **Extracting Medication-related Terms**
- **Producing Geographic Heat-Maps**