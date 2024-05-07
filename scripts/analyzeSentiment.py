# SENTIMENT ANALYSIS RESULTS

import pandas as pd
from textblob import TextBlob
import nltk
from nltk.tokenize import word_tokenize
import matplotlib.pyplot as plt

def process_csv(file_path, doc_threshold=0.5):
    df = pd.read_csv('GoFundMe-Data.csv')
    
    texts = df["Description"].dropna().tolist()
    
    polarity_scores = []
    subjectivity_scores = []
    
    # Analyze each piece of content for polarity and subjectivity
    for text in texts:
        analysis = TextBlob(text)
        polarity_scores.append((text, analysis.sentiment.polarity))
        subjectivity_scores.append((text, analysis.sentiment.subjectivity))
    
    # Sort the lists based on scores
    polarity_scores.sort(key=lambda x: x[1], reverse=True) # Sort by polarity, highest first
    subjectivity_scores.sort(key=lambda x: x[1], reverse=True) # Sort by subjectivity, highest first
    
    # Extract the top 5 and bottom 5 based on polarity
    top_5_polarity = polarity_scores[:5]
    bottom_5_polarity = polarity_scores[-5:]
    
    # Extract the top 5 and bottom 5 based on subjectivity
    top_5_subjectivity = subjectivity_scores[:5]
    bottom_5_subjectivity = subjectivity_scores[-5:]
    
    return {
        'Top 5 Polarity': top_5_polarity,
        'Bottom 5 Polarity': bottom_5_polarity,
        'Top 5 Subjectivity': top_5_subjectivity,
        'Bottom 5 Subjectivity': bottom_5_subjectivity
    }

results = process_csv('GoFundMe-Data.csv')
print(results)

def textToScores(txt: str, polarity=True):
    # Convert string into textblob object
    blob = TextBlob(txt)
    # Find polarity or subjectivity based on boolean input
    score = blob.sentiment.polarity if polarity else blob.sentiment.subjectivity
    # Return score text tuple for use in sorting
    return score, txt

def getScores(data):
    # Create lists to store polarity and subjectivity scores
    polScores = []
    subScores = []

    # Iterate over strings in data
    for txt in data:
        # Get polarity and subjectivity scores
        pol = textToScores(txt, True)
        sub = textToScores(txt, False)

        polScores.append(pol)
        subScores.append(sub)

    # Sort both lists (elements are tuples so sorting key is needed)
    polScores.sort(key=lambda x: x[0])
    subScores.sort(key=lambda x: x[0])

    return polScores, subScores

def plotData(polarity, subjectivity, title):
    # iterate over polarity and subjectivity
    for data, data_title in [(polarity, "Polarity"), (subjectivity, "Subjectivity")]:
        # Plot histogram
        plt.hist(data, bins=30, color='skyblue', edgecolor='black')
        # Label axes and graph + show graph
        plt.xlabel("Frequency")
        plt.ylabel(f"{title} {data_title} Scores")
        plt.title(f"Frequency of {title} {data_title} Scores")
        plt.show()
    return None

df = pd.read_csv('GoFundMe-Data.csv').dropna()

# Convert comments and questions into lists
text = list(df['Description'])

# Get sorted scores for both
pol_cs, sub_cs = getScores(text)

# Extract scores
pol_scores = [x for x, _ in pol_cs]
sub_scores = [x for x, _ in sub_cs]

# Extracting top and bottom 5 polarity and subjectivity scores:
p_extreme_cms = (pol_cs[:5], pol_cs[-5:])
s_extreme_cs = (sub_cs[:5], sub_cs[-5:])

# Plot data
plotData(pol_scores, sub_scores, "Description")