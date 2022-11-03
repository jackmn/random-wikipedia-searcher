import re
import requests
import numpy as np
import pandas as pd
from bs4 import BeautifulSoup
from sklearn.feature_extraction.text import TfidfVectorizer

def get_random_wiki_page() : 
    URL = "https://en.wikipedia.org/wiki/Special:Random"
    return requests.get(url = URL)

def get_split_content(article_num):

    titles = []
    header2 = []
    header3 = []
    pValues = []

    for i in range(article_num):
        r = get_random_wiki_page()
        header = dict(r.headers)
        parsed_html = BeautifulSoup(r.text, 'html.parser')
        titles.append(parsed_html.title.string)
        
        paragraphs = parsed_html.find_all('h2')
        text_body = ""
        for paragraph in paragraphs:
            text_body += " " + paragraph.get_text(" ", strip=True)
        header2.append(text_body)
    
        paragraphs = parsed_html.find_all('h3')
        text_body = ""
        for paragraph in paragraphs:
            text_body += " " + paragraph.get_text(" ", strip=True)
        header3.append(text_body)

        paragraphs = parsed_html.find_all('p')
        text_body = ""
        for paragraph in paragraphs:
            text_body += " " + paragraph.get_text(" ", strip=True)
        pValues.append(text_body)
    return titles, header2, header3, pValues

# Functions below are part of an attempt to remove duplicates in each tag type

# def set_up_remove_duplicates(titles, h2, h3, p_vals):
#     titles_duplicates = set(titles[0].split()).intersection(set(titles[1].split()))
#     h2_duplicates = set(h2[0].split()).intersection(set(h2[1].split()))
#     h3_duplicates = set(h3[0].split()).intersection(set(h3[1].split()))
#     p_vals_duplicates = set(p_vals[0].split()).intersection(set(p_vals[1].split()))
#     filtered_title = []
#     filtered_h2 = []
#     filtered_h3 = []
#     filtered_p_vals = []

#     for strings in titles:
#         filtered_title.append(remove_duplicates(strings, list(titles_duplicates)))

#     for strings in h2:
#         filtered_h2.append(remove_duplicates(strings, list(h2_duplicates)))

#     for strings in h3:
#         filtered_h3.append(remove_duplicates(strings, list(h3_duplicates)))

#     for strings in p_vals:
#         filtered_p_vals.append(remove_duplicates(strings, list(p_vals_duplicates)))

#     return filtered_title, filtered_h2, filtered_h3, filtered_p_vals

# def remove_duplicates(main_string, remove_list):
#     output_string = ""
#     for word in main_string.split():
#         if word not in remove_list:
#             output_string += word + " " 
#     return(output_string)

def calculate_tfidf(text_arrays) :
    # It fits the data and transform it as a vector
    X = vectorizer.fit_transform(text_arrays)
    # Convert the X as transposed matrix
    X = X.T.toarray()
    # Create a DataFrame and set the vocabulary as the index
    df = pd.DataFrame(X, index=vectorizer.get_feature_names())
    return df

def rank_relevant_articles(user_search, importance_df, article_num):

    # Convert the query become a vector
    query_vector = vectorizer.transform([user_search]).toarray().reshape(importance_df.shape[0],)
    similarity = {}

    # Calculate the similarity
    for i in range(article_num):
        similarity[i] = np.dot(importance_df.loc[:, i].values, query_vector) / np.linalg.norm(importance_df.loc[:, i]) * np.linalg.norm(query_vector)

    return(similarity)

# Instantiate a TfidfVectorizer object
vectorizer = TfidfVectorizer()

input_string = input("Search Articles: ")
N = 200
all_requests = []
titles = []
header2 = []
header3 = []
pValues = []

# The comment here is my attempt at removing common words particularily in headers. It is explained further in the read.me
titles, header2, header3, pValues = get_split_content(N)
# titles, header2, header3, pValues = set_up_remove_duplicates(titles, header2, header3, pValues)
textGroups = [titles,header2,header3,pValues]

# Standard cleaning for text analysis
cleanedText = []

for sections in textGroups:
    documents_clean = []
    for doc in sections:
        # Remove Unicode
        document_test = re.sub(r'[^\x00-\x7F]+', ' ', doc)
        # Remove Mentions
        document_test = re.sub(r'@\w+', '', document_test)
        # Lowercase the document
        document_test = document_test.lower()
        # Remove punctuations
        document_test = re.sub(r'[^\w\s]','',document_test)
        # Lowercase the numbers
        document_test = re.sub(r'[0-9]', '', document_test)
        # Remove the doubled space
        document_test = re.sub(r'\s{2,}', ' ', document_test)
        documents_clean.append(document_test)
    cleanedText.append(documents_clean)

# Find most relevant
article_relevancies = []
for article_elements in range(len(cleanedText)):
    wiki_df = calculate_tfidf(cleanedText[article_elements])
    similarity_scores = rank_relevant_articles(input_string.lower(), wiki_df, N)
    article_relevancies.append(similarity_scores)

# To add weight to different sections of the text
type_weighting = [10,3,2,1]
search_list_weights = []

for article_number in range(N):
    total = article_relevancies[0][article_number]*type_weighting[0] + article_relevancies[1][article_number]*type_weighting[1] + article_relevancies[2][article_number]*type_weighting[2] + article_relevancies[3][article_number]*type_weighting[3]
    search_list_weights.append(total)

# Calculates an ordered list of the most relevant searches
most_relevant_searches = sorted(list(zip(search_list_weights, textGroups[0])), key=lambda tup: tup[0], reverse=True)

# Only returns articles with some sort of relevancy
relevant_searches = 0
for search_result in most_relevant_searches:
    if search_result[0] > 0:
        # To remove - Wikipedia from the end of titles
        article_length = len(search_result[1])
        print(search_result[1][:article_length-11])
        relevant_searches += 1

print("There were " + str(relevant_searches) + " relevant results")