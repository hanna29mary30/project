from itertools import permutations
import numpy as np
import pandas as pd
from scipy.sparse import csr_matrix
from sklearn.neighbors import NearestNeighbors
import pickle

def train_model(root_path):
    rating_min = 100 #200
    per_book_rating_min = 10 #50

    book_dtype = {"ISBN": 'string', "Book-Title": 'string', "Book-Author": 'string', "Year-Of-Publication": 'string',
             "Publisher": 'string', "Image-URL-S": 'string', "Image-URL-M": 'string', "Image-URL-L": 'string'}

    books = pd.read_csv(f"{root_path}BX-Books.csv", dtype=book_dtype, sep=';', encoding="latin-1", on_bad_lines='skip')
    users = pd.read_csv(f"{root_path}BX-Users.csv", sep=';', encoding="latin-1", on_bad_lines='skip')
    ratings = pd.read_csv(f"{root_path}BX-Book-Ratings.csv", sep=';', encoding="latin-1", on_bad_lines='skip')
    books = books[['ISBN', 'Book-Title', 'Book-Author', 'Year-Of-Publication', 'Publisher']]
    books.rename(columns = {'Book-Title':'title', 'Book-Author':'author', 'Year-Of-Publication':'year', 'Publisher':'publisher'}, inplace=True)
    users.rename(columns = {'User-ID':'user_id', 'Location':'location', 'Age':'age'}, inplace=True)
    ratings.rename(columns = {'User-ID':'user_id', 'Book-Rating':'rating'}, inplace=True)

    #print(books.head())
    #print(ratings['user_id'].value_counts())

    #Step-1) Extract users and ratings of more than 200
    x = ratings['user_id'].value_counts() > rating_min
    y = x[x].index  #user_ids
    #print(y.shape)
    ratings = ratings[ratings['user_id'].isin(y)]

    #step-2) Merge ratings with books
    rating_with_books = ratings.merge(books, on='ISBN')
    #print(rating_with_books.head())

    #step-3) Extract books that have received more than 50 ratings.
    number_rating = rating_with_books.groupby('title')['rating'].count().reset_index()
    number_rating.rename(columns= {'rating':'number_of_ratings'}, inplace=True)
    final_rating = rating_with_books.merge(number_rating, on='title')
    #print(final_rating.shape)
    final_rating = final_rating[final_rating['number_of_ratings'] >= per_book_rating_min]
    final_rating.drop_duplicates(['user_id','title'], inplace=True)

    #Step-4) Create Pivot Table
    book_pivot = final_rating.pivot_table(columns='user_id', index='title', values="rating")
    book_pivot.fillna(0, inplace=True)

    #Modeling
    book_sparse = csr_matrix(book_pivot)

    # Now we will train the nearest neighbors algorithm.
    # here we need to specify an algorithm which is brute
    # means find the distance of every point to every other point


    model = NearestNeighbors(algorithm='brute')
    model.fit(book_sparse)
    modelfile = f'{root_path}model.dat'
    bookfile = f'{root_path}books.dat'
    bookpivotfile = f'{root_path}bookpivot.dat'
    save_data(modelfile, model)
    save_data(bookpivotfile, book_pivot)
    save_data(bookfile, books)


def predict_from_model(root_path, in_title):

    modelfile = f'{root_path}model.dat'
    model = load_data(modelfile)
    bookfile = f'{root_path}books.dat'
    books = load_data(bookfile)
    bookpivotfile = f'{root_path}bookpivot.dat'
    book_pivot = load_data(bookpivotfile)

    # Let’s make a prediction and see whether it is suggesting books or not

    # book_iloc = 232
    try:
        pos = book_pivot.loc[(in_title)]  # 'Lake Wobegon days')]
    except:
        print('Error...................................................')
        return []

    # print('Ha ha ha',pos.name)

    # distances, suggestions = model.kneighbors(book_pivot.iloc[book_iloc, :].values.reshape(1, -1))
    # print('##############',book_pivot.index[book_iloc],'################')
    distances, suggestions = model.kneighbors(pos.values.reshape(1, -1))
    print('##############', pos.name, '################')

    result = []
    # let us print all the suggested books.
    for i in range(len(suggestions)):
        # print('>>>>>>>>>>>',book_pivot.index[suggestions[i]])
        for b in book_pivot.index[suggestions[i]]:
            # if book_pivot.index[book_iloc] == b:
            #    continue
            # print('>>>>', b)
            df = (books.loc[books['title'] == b])
            for row in df.itertuples():
                # print(row)
                result.append(list(row))
            # print('##########')
    print('result...................', len(result))
    if len(result) == 0:
        return print('No Result')
    else:
        return result








def predict(root_path, in_title):
    rating_min = 100 #200
    per_book_rating_min = 10 #50

    books = pd.read_csv(f"{root_path}BX-Books.csv", sep=';', encoding="latin-1", error_bad_lines=False)
    users = pd.read_csv(f"{root_path}BX-Users.csv", sep=';', encoding="latin-1", error_bad_lines=False)
    ratings = pd.read_csv(f"{root_path}BX-Book-Ratings.csv", sep=';', encoding="latin-1", error_bad_lines=False)

    books = books[['ISBN', 'Book-Title', 'Book-Author', 'Year-Of-Publication', 'Publisher']]
    books.rename(columns = {'Book-Title':'title', 'Book-Author':'author', 'Year-Of-Publication':'year', 'Publisher':'publisher'}, inplace=True)
    users.rename(columns = {'User-ID':'user_id', 'Location':'location', 'Age':'age'}, inplace=True)
    ratings.rename(columns = {'User-ID':'user_id', 'Book-Rating':'rating'}, inplace=True)

    #print(books.head())
    #print(ratings['user_id'].value_counts())

    #Step-1) Extract users and ratings of more than 200
    x = ratings['user_id'].value_counts() > rating_min
    y = x[x].index  #user_ids
    #print(y.shape)
    ratings = ratings[ratings['user_id'].isin(y)]

    #step-2) Merge ratings with books
    rating_with_books = ratings.merge(books, on='ISBN')
    #print(rating_with_books.head())

    #step-3) Extract books that have received more than 50 ratings.
    number_rating = rating_with_books.groupby('title')['rating'].count().reset_index()
    number_rating.rename(columns= {'rating':'number_of_ratings'}, inplace=True)
    final_rating = rating_with_books.merge(number_rating, on='title')
    #print(final_rating.shape)
    final_rating = final_rating[final_rating['number_of_ratings'] >= per_book_rating_min]
    final_rating.drop_duplicates(['user_id','title'], inplace=True)

    #Step-4) Create Pivot Table
    book_pivot = final_rating.pivot_table(columns='user_id', index='title', values="rating")
    book_pivot.fillna(0, inplace=True)

    #Modeling
    book_sparse = csr_matrix(book_pivot)

    # Now we will train the nearest neighbors algorithm.
    # here we need to specify an algorithm which is brute
    # means find the distance of every point to every other point


    model = NearestNeighbors(algorithm='brute')
    model.fit(book_sparse)

    #Let’s make a prediction and see whether it is suggesting books or not

    #book_iloc = 232

    pos = book_pivot.loc[(in_title)]#'Lake Wobegon days')]
    #print('Ha ha ha',pos.name)


    #distances, suggestions = model.kneighbors(book_pivot.iloc[book_iloc, :].values.reshape(1, -1))
    #print('##############',book_pivot.index[book_iloc],'################')
    distances, suggestions = model.kneighbors(pos.values.reshape(1, -1))
    print('##############',pos.name,'################')

    result = []
    #let us print all the suggested books.
    for i in range(len(suggestions)):
        #print('>>>>>>>>>>>',book_pivot.index[suggestions[i]])
        for b in book_pivot.index[suggestions[i]]:
            #if book_pivot.index[book_iloc] == b:
            #    continue
            #print('>>>>', b)
            df = (books.loc[books['title'] == b])
            for row in df.itertuples():
                #print(row)
                result.append(list(row))
            #print('##########')
    #print(result)
    return result


def save_data(fname, classifier):
    with open(fname, 'wb') as picklefile:
        pickle.dump(classifier, picklefile)


def load_data(fname):
    with open(fname, 'rb') as training_model:
        model = pickle.load(training_model)
    return model


if __name__ == '__main__':

    #result_list = predict(root_path='../dataset/',in_title='Lake Wobegon days')
    #for result in result_list:
    #    print(result)
    #    print('############')

    #train_model(root_path='../dataset/')
    result_list = predict_from_model(root_path='../dataset/', in_title='Barrier Island')#'Lake Wobegon days'
    for result in result_list:
        print(result)
        print('############')