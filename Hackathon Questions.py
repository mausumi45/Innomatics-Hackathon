#!/usr/bin/env python
# coding: utf-8

# In[1]:


## Import rating CSV
import pandas as pd 
import numpy as np
import matplotlib.pyplot as plt
rating = pd.read_csv(r"C:\Users\ASUS\Music\ratings.csv")
rating


# In[2]:


## unique user id 
unique_user = rating['userId'].nunique()
unique_user


# In[3]:


pip install numpy


# In[4]:


### import movie data
movie = pd.read_csv(r"C:\Users\ASUS\Music\movies.csv")
movie


# In[5]:


## maximum rated movie name
mOVIE_NAME = movie[movie['movieId'] == 356]
mOVIE_NAME


# In[6]:


rating_counts = rating.groupby('movieId').size()
rating_counts
# Find the movie with the maximum number of ratings
max_rated_movie = rating_counts.idxmax()
max_rated_movie


# In[7]:


max_ratings_count = rating_counts.max()
max_ratings_count


# In[8]:


### tAGS IMPORT
Tags = pd.read_csv(r"C:\Users\ASUS\Music\tags.csv")
Tags


# In[9]:


# # Select all the correct tags submitted by users to "Matrix, The (1999)" movie?
tags_for_movie = Tags[Tags['movieId'] == 2571]
tags_for_movie


# In[10]:


movie_id_matrix = movie[movie['title'] == "Matrix, The (1999)"]
movie_id_matrix


# In[11]:


# Select the tags
tags = tags_for_movie['tag'].unique()
tags


# In[12]:


## unique tags
Unique_tags = Tags['tag'].nunique()
Unique_tags


# In[13]:


## What is the average user rating for movie named "Terminator 2: Judgment Day (1991)"?
movie_id_terminator = movie[movie['title'] == "Terminator 2: Judgment Day (1991)"]
movie_id_terminator


# In[14]:


# Filter ratings for the movieId
movie_ratings = rating[rating['movieId'] == 589]
movie_ratings


# In[15]:


# Calculate the average rating
average_rating = movie_ratings['rating'].mean()
average_rating


# In[16]:


# How does the data distribution of user ratings for "Fight Club (1999)" movie looks like?
movie_id_fight = movie[movie['title'] == "Fight Club (1999)"]
movie_id_fight


# In[17]:


# Filter ratings for the movieId
movie_ratings_fight = rating[rating['movieId'] == 2959]
movie_ratings_fight


# In[18]:


# Plot the distribution of ratings
plt.figure(figsize=(8, 6))
plt.hist(movie_ratings_fight, bins=range(1, 7), edgecolor='black', alpha=0.7)
plt.xlabel('Rating')
plt.ylabel('Frequency')
plt.title('Distribution of User Ratings for "Fight Club (1999)"')
plt.xticks(range(1, 6))
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.show()


# In[19]:


aggregated_data = rating.groupby('movieId')['rating'].agg(['count', 'mean'])

# Rename columns for clarity
aggregated_data.columns = ['Number of Ratings', 'Average Rating']

aggregated_data


# In[20]:


# Apply inner join
merged_df = pd.merge(movie, aggregated_data, on='movieId', how='inner')

merged_df


# In[21]:


# Filter movies with more than 50 user ratings
filtered_df = merged_df[merged_df['Number of Ratings'] > 50]
filtered_df


# In[22]:


# Which movie is the most popular based on  average user ratings?
most_popular_movie = filtered_df.loc[filtered_df['Average Rating'].idxmax()]
most_popular_movie


# In[23]:


# Select all the correct options which comes under top 5 popular movies based on number of user ratings.
# Sort the filtered DataFrame by 'Number of Ratings' in descending order
sorted_df = filtered_df.sort_values(by='Number of Ratings', ascending=False)

# Select the top 5 movies based on the number of ratings
top_5_movies = sorted_df.head(5)
top_5_movies


# In[24]:


# Which Sci-Fi movie is "third most popular" based on the number of user ratings?
# Filter Sci-Fi movies
sci_fi_df = filtered_df[filtered_df['genres'].str.contains('Sci-Fi', case=False, na=False)]

# Sort the Sci-Fi movies by 'Number of Ratings' in descending order
sorted_sci_fi_df = sci_fi_df.sort_values(by='Number of Ratings', ascending=False)

# Select the third most popular Sci-Fi movie based on the number of ratings
third_most_popular_sci_fi = sorted_sci_fi_df.iloc[2]  # Index 2 corresponds to the third item
third_most_popular_sci_fi


# In[25]:


## import links 
links = pd.read_csv(r"C:\Users\ASUS\Music\links.csv")
links


# In[26]:


# Add a placeholder for IMDb ratings
links['imdbRating'] = np.nan
links


# In[27]:


pip install requests


# In[28]:


import requests
from bs4 import BeautifulSoup

def scrapper(imdbId):
    id = str(int(imdbId))
    n_zeroes = 7 - len(id)
    new_id = "0" * n_zeroes + id
    URL = f"https://www.imdb.com/title/tt{new_id}/"
    
    print(f"Scraping URL: {URL}")  # Debugging output
    
    request_header = {
        'Content-Type': 'text/html; charset=UTF-8',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/119.0',
        'Accept-Encoding': 'gzip, deflate, br'
    }
    
    response = requests.get(URL, headers=request_header)
    
    if response.status_code != 200:
        print(f"Failed to retrieve {URL}, status code: {response.status_code}")
        return np.nan
    
    soup = BeautifulSoup(response.text, 'html.parser')
    
    imdb_rating = soup.find('span', attrs={'class': 'sc-eb51e184-1 ljxVSS'})
    
    if imdb_rating:
        return imdb_rating.text
    else:
        print(f"Could not find rating for {URL}")
        return np.nan


# In[29]:


# Scrape IMDb ratings and update the DataFrame
for index, row in links.iterrows():
    links.at[index, 'imdbRating'] = scrapper(row['imdbId'])


# In[39]:


# Find the movie with the highest IMDb rating
highest_rated_movie = links.sort_values(by='imdbRating', ascending=False).iloc[0]
highest_rated_movie


# In[44]:


highest = movie[movie['movieId'] == 1196]
highest


# In[35]:


merged = pd.merge(filtered_df, links, on='movieId', how='inner')
merged


# In[36]:


# Filter Sci-Fi movies
sci_fi_df = merged[merged['genres'].str.contains('Sci-Fi', case=False, na=False)]
sci_fi_df


# In[37]:


# Scrape IMDb ratings for Sci-Fi movies
sci_fi_df['IMDB Rating'] = sci_fi_df['imdbId'].apply(scrapper)


# In[43]:


# Find the movie with the highest IMDb rating
highest_rated_sci_fi = sci_fi_df.sort_values(by='imdbRating', ascending=False).iloc[0]
highest_rated_sci_fi


# In[ ]:




