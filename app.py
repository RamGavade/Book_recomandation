from flask import Flask,render_template,request
import pickle
import numpy as np
import pandas as pd

popular_df = pickle.load(open('popular.pkl' , 'rb'))
pt = pickle.load(open('pt.pkl' , 'rb'))
books = pickle.load(open('books.pkl' , 'rb'))
similarity_score = pickle.load(open('similarity_score.pkl' , 'rb'))

app= Flask(__name__)
@app.route('/')
def index():
    return render_template('index.html',
                           book_name = list(popular_df['Book-Title'].values),
                           author=list(popular_df['Book-Author'].values),
                           image=list(popular_df['Image-URL-M'].values),
                           votes=list(popular_df['num_ratings'].values),
                           rating=list(popular_df['avg_ratings'].values)
                           )

@app.route('/recommend')
def recommend_ui():
    return render_template('recommend.html')


from flask import render_template, request
import numpy as np


@app.route('/recommend_books', methods=['POST'])
def recommend():

    user_input = request.form.get('user_input')


    if pt.index.empty:
        return "Error: No data available for recommendation."


    if user_input not in pt.index:
        return "Error: User input not found in the index."

    try:

        index = np.where(pt.index == user_input)[0][0]
    except IndexError:

        return "Error: No match found for the given input."


    similar_item = sorted(
        list(enumerate(similarity_score[index])),
        key=lambda x: x[1],
        reverse=True
    )[1:5]

    data = []
    for i in similar_item:
        item = []

        temp_df = books[books['Book-Title'] == pt.index[i[0]]]

        item.extend(temp_df.drop_duplicates('Book-Title')['Book-Title'].to_list())
        item.extend(temp_df.drop_duplicates('Book-Title')['Book-Author'].to_list())
        item.extend(temp_df.drop_duplicates('Book-Title')['Image-URL-M'].to_list())

        data.append(item)

    print(data)

    return render_template('recommend.html', data=data)


@app.route('/about')
def about_ui():
    return render_template('about.html')


if __name__ == '__main__':
    app.run(debug=True)