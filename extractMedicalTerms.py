# EXTRACTING MEDICAL TEXTS FROM DATA

import pandas as pd
from collections import Counter
from drug_named_entity_recognition import find_drugs

def process_csv_drug_ner(file_path):
    # Read the CSV file
    df = pd.read_csv(file_path)
    
    # Extracting text from the "Text" column
    texts = df["Title"].dropna().tolist() + df["Description"].dropna().tolist()
    
    drug_counts = Counter()
    drug_synonyms = {}  # To store the synonyms for each drug
    
    # Process each text for drug named entity recognition
    for text in texts:
        words = text.split()
        
        # Use the find_drugs function to detect drugs in the tokenized text
        results = find_drugs(words)
        
        for result in results:
            drug_info = result[0]
            drug_name = drug_info['name']
            synonyms = drug_info['synonyms']

            # Increment count for the drug name
            drug_counts[drug_name] += 1
            
            # Update the synonyms set for this drug
            if drug_name not in drug_synonyms:
                drug_synonyms[drug_name] = set(synonyms)
            else:
                drug_synonyms[drug_name].update(synonyms)
                
            # Also increment count for any synonyms of the drug, treating them as the same drug
            for synonym in synonyms:
                # Treat the synonym as an occurrence of the drug itself
                drug_counts[drug_name] += 1
                
    # Return the most common drugs, their counts, and their synonyms
    return drug_counts, drug_synonyms

file_path = 'GoFundMe-Data.csv'  
most_common_drugs, drug_synonyms = process_csv_drug_ner(file_path) 

# Print the most common drugs, their frequencies, and their synonyms
for drug, frequency in most_common_drugs.most_common():  # Use .most_common() here to iterate
    synonyms_list = ', '.join(drug_synonyms[drug]) if drug in drug_synonyms and drug_synonyms[drug] else 'No synonyms'
    print(f"{drug}: {frequency} (Synonyms: {synonyms_list})")