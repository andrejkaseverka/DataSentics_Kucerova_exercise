import pandas as pd
import sys
import csv

# Saving the names of the folders where to find the data
users_address = 'BX-CSV-Dump/BX-Users.csv'
books_address = 'BX-CSV-Dump/BX-Books.csv'
ratings_address = 'BX-CSV-Dump/BX-Book-Ratings.csv'

def find_people_based_on_rating(ISBN, rating):
    # Creates list of User-ID's of people that rated concrete book with a specified rating
    users = []
    handle = open(ratings_address,'r')
    reader = csv.DictReader(handle, delimiter=';')
    for row in reader:
        if (row['ISBN']==ISBN) and (row['Book-Rating']==str(rating)):
            users.append(row['User-ID'])
    handle.close()
    return users

# Asking the user for a book of his choice
favourite_book = input('Please, enter the exact name of your favourite book: ')

# Searching for the ISBN of favourite book
favourite_ISBN = ''
handle = open(books_address, 'r')
reader = csv.DictReader(handle, delimiter=';')
for row in reader:
    if row['Book-Title']==str(favourite_book):
        favourite_ISBN = row['ISBN']
        break
handle.close()

# Checking if the title is correct, if it is not, it exits the program
if favourite_ISBN=='':
    print('Sorry, but I do not know this book. Are you sure you typed the title correctly?')
    sys.exit()

# Preparing list of 10 book suggestions, so far with empty strings
suggestions_ISBN = ['']*10
suggestions_titles = ['']*10

# Getting through the table of ratings to find people that rated the favourite book 10 (or less if
# I do not find enough book recommendations to fill the suggestions_ISBN)
rating_processing = 10
while (suggestions_ISBN[9]=='') and (rating_processing>5):
    users_processing = find_people_based_on_rating(favourite_ISBN, rating_processing)
    dict_of_candidates = {} # Book candidates for suggestions are stored in a dictionary, key=ISBN, value=ratings
    # Processing the list of ratings and storing info about possible suggestions in dict_of_candidates
    handle = open(ratings_address, 'r')
    reader = csv.DictReader(handle, delimiter=';')
    for row in reader:
        if (row['ISBN'] != favourite_ISBN) and (int(row['Book-Rating'])>5): # Do not want to recommend the same book
            relevant_rating = False
            for ID in users_processing: # Need to check if the rating is from a relevant user
                if row['User-ID']==ID:
                    relevant_rating = True
            if relevant_rating: # Need to increase the rating of this book in dict_of_candidates
                if row['ISBN'] in dict_of_candidates:
                    dict_of_candidates[row['ISBN']] = dict_of_candidates[row['ISBN']] + int(row['Book-Rating'])
                else:
                    dict_of_candidates[row['ISBN']] = int(row['Book-Rating'])
    ## Note: I am getting lot of books with the same rating in dict_of_candidates and they will be sortes randomly
    ## as I go through the dictionary; it would be better to sort them also, maybe using their average rating
    handle.close()
    # Filling the suggestions_ISBN according to dict_of_candidates
    for ISBN in dict_of_candidates: # Try to place the book ISBN accordingly into suggestions_ISBN
        placed = False
        i = 10
        while not placed:
            if i==0:
                # I got at the beginning
                suggestions_ISBN[i] = ISBN
                placed = True
            elif (suggestions_ISBN[i-1]==''):
                # The list still has empty places
                i -= 1
            elif dict_of_candidates[ISBN]<=dict_of_candidates[suggestions_ISBN[i-1]]:
                # I found the right spot
                if i<10:
                    suggestions_ISBN[i] = ISBN
                placed = True                               
            elif dict_of_candidates[ISBN]>dict_of_candidates[suggestions_ISBN[i-1]]:
                # Need to move the one on the left
                if i<10:
                    suggestions_ISBN[i] = suggestions_ISBN[i-1]
                i -= 1
    rating_processing -= 1

# Filling the names of the suggested books in suggestions_titles
handle = open(books_address, 'r')
reader = csv.DictReader(handle, delimiter=';')
for row in reader:
    for i in range(10):
        if row['ISBN']==suggestions_ISBN[i]:
            suggestions_titles[i] = row['Book-Title']
handle.close()

# Printing the result
print('\nI think you might like the following titles:\n')
print(*suggestions_titles, sep='\n')



