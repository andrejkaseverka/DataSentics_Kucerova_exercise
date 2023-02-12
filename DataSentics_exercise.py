import pandas as pd
import sys
import csv
from collections import defaultdict

# Saving the names of the folders where to find the data
users_address = 'BX-CSV-Dump/BX-Users.csv'
books_address = 'BX-CSV-Dump/BX-Books.csv'
ratings_address = 'BX-CSV-Dump/BX-Book-Ratings.csv'

def find_people_based_on_rating(title, rating):
    # Creates list of User-ID's of people that rated concrete book with a specified rating
    users = []
    handle = open(ratings_address,'r')
    reader = csv.DictReader(handle, delimiter=';')
    for row in reader:
        if (row['ISBN'] in dict_of_ISBN[title]) and (row['Book-Rating']==str(rating)):
            users.append(row['User-ID'])
    handle.close()
    return users

# Asking the user for a book of his choice
favourite_book = input('Please, enter the exact name of your favourite book: ')

# Creating dictionary of book titles and all related ISBN's
dict_of_ISBN = defaultdict(list)
handle = open(books_address, 'r')
reader = csv.DictReader(handle, delimiter=';')
for row in reader:
    dict_of_ISBN[row['Book-Title']].append(row['ISBN'])
handle.close()

# Checking if the title is correct, if it is not, it exits the program
if favourite_book not in dict_of_ISBN:
    print('Sorry, but I do not know this book. Are you sure you typed the title correctly?')
    sys.exit()

# Preparing list of 10 book suggestions, so far with empty strings
suggestions_title = ['']*10

# Getting through the table of ratings to find people that rated the favourite book 10 (or less if
# I do not find enough book recommendations to fill the suggestions_ISBN)
rating_processing = 10
dict_of_candidates_title = {}
while (len(dict_of_candidates_title)<10) and (rating_processing>5):
    users_processing = find_people_based_on_rating(favourite_book, rating_processing)
    dict_of_candidates_ISBN = {} # Book candidates for suggestions are stored in a dictionary, key=ISBN, value=ratings
    # After processing I will need to process the dict_of_candidates_ISBN to get final numbers for titles
    # Processing the list of ratings and storing info about possible suggestions in dict_of_candidates
    handle = open(ratings_address, 'r')
    reader = csv.DictReader(handle, delimiter=';')
    for row in reader:
        if (row['ISBN'] not in dict_of_ISBN[favourite_book]) and (int(row['Book-Rating'])>5): # Do not want to recommend the same book
            relevant_rating = False
            for ID in users_processing: # Need to check if the rating is from a relevant user
                if row['User-ID']==ID:
                    relevant_rating = True
            if relevant_rating: # Need to increase the rating of this book in dict_of_candidates
                if row['ISBN'] in dict_of_candidates_ISBN:
                    dict_of_candidates_ISBN[row['ISBN']] = dict_of_candidates_ISBN[row['ISBN']] + int(row['Book-Rating'])
                else:
                    dict_of_candidates_ISBN[row['ISBN']] = int(row['Book-Rating'])
    ## Note: I am getting lot of books with the same rating in dict_of_candidates and they will be sortes randomly
    ## as I go through the dictionary; it would be better to sort them also, maybe using their average rating
    handle.close()

    # Now I need to transfer the ratings for ISBN to ratings of titles
    for title in dict_of_ISBN:
        sum_rating = 0
        for ISBN in dict_of_ISBN[title]:
            if ISBN in dict_of_candidates_ISBN:
                sum_rating += int(dict_of_candidates_ISBN[ISBN])
        if sum_rating>0:
            if title in dict_of_candidates_title:
                dict_of_candidates_title[title] = dict_of_candidates_title[title] + rating_processing*sum_rating
            else:
                dict_of_candidates_title[title] = rating_processing*sum_rating
    rating_processing -= 1

# Filling the suggestions_title according to dict_of_candidates_title
for title in dict_of_candidates_title: # Try to place the book title accordingly into suggestions_title
    placed = False
    i = 10
    while not placed:
        if i==0:
            # I got at the beginning
            suggestions_title[i] = title
            placed = True
        elif (suggestions_title[i-1]==''):
            # The list still has empty places
            i -= 1
        elif dict_of_candidates_title[title]<=dict_of_candidates_title[suggestions_title[i-1]]:
            # I found the right spot
            if i<10:
                suggestions_title[i] = title
            placed = True                               
        elif dict_of_candidates_title[title]>dict_of_candidates_title[suggestions_title[i-1]]:
            # Need to move the one on the left
            if i<10:
                suggestions_title[i] = suggestions_title[i-1]
            i -= 1

# Printing the result
print('\nI think you might like the following titles:\n')
print(*suggestions_title, sep='\n')