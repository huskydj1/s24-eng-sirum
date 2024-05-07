# SCRAPING FOR LINKS WITH SERPAPI

# Import necessary libraries
from serpapi import GoogleSearch  # Import GoogleSearch from serpapi for querying Google search results
import pandas as pd   # Import Pandas library for handling CSV files
import re  # Import re library for regular expression operations

# Set variables for the Google Search API
engine = "google"  # Specify the search engine (Google)

# Prompt the user to input the number of queries to search through
while True:
    try:
        query_num = int(input("How many queries do you want to search through?: "))
        break
    except ValueError:
        print("Invalid input. Please enter a number.")

# Prompt the user to input the number of search results to retrieve
while True:
    try:
        num = int(input("How many search results do you want to retrieve?: "))
        break
    except ValueError:
        print("Invalid input. Please enter a number.")

# Provide examples of queries to the user
print("Here are some query examples: 'help paying drug', 'affordable medication'")
print("Please input your queries:")

# Initialize an empty list to store user-defined queries
queries = []
for i in range(query_num):
    answer = input("Query #" + str(i + 1) + ": ")
    print (answer)
    queries.append(answer)  # Prompt user to input each query

# SerpApi API key (replace with your actual API key)
api_key = "" #TODO: add key here

def get_links(api_key, queries):
    # List to store dictionaries of title, link, and source
    data = []  
    for query in queries:
        search_params = {
            "engine": engine,
            "q": query  + " site:gofundme.com",
            "api_key": api_key,
            "num": num  
        }

        # Perform the search using GoogleSearch from serpapi
        search = GoogleSearch(search_params)
        results = search.get_dict()

        # Extract title, link, and source from search results
        for result in results.get("organic_results", []):
            data.append({
                "Title": result.get("title"),
                "Link": result.get("link"),
                "Source": result.get("source")
            })
    return pd.DataFrame(data)

# Call the get_links function to retrieve links for specified queries
df = get_links(api_key, queries)

# Saving the DataFrame to a CSV file
filename = "GoFundMe-Weblinks.csv"
df.to_csv(filename, index=False)
