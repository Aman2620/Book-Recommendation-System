from flask import Flask,render_template,request
import pickle as pk
import numpy as np

df_popular = pk.load(open('popular.pkl','rb'))
suggest_author_books = pk.load(open('author.pkl','rb'))
pt = pk.load(open('pt.pkl','rb'))
df_books = pk.load(open('books.pkl','rb'))
similarity_scores = pk.load(open('similarity_scores.pkl','rb'))

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/popular.html')
def popular():
    return render_template('popular.html',
    book_name = list(df_popular['Book-Title'].values),
    author = list(df_popular['Book-Author'].values),
    image = list(df_popular['Image-URL-M'].values),
    votes = list(df_popular['Book-Rating']),
    rating = list(df_popular['Average-Rating'].values)
    )

@app.route('/author.html')
def author():
    return render_template('author.html')

@app.route('/author_results',methods=["post"])
def author_reults():
    input_user = request.form.get('input_user')
    index = suggest_author_books.index[suggest_author_books['Book-Author']==input_user].to_list()
    data = []
    for i in index:
        item = []
        item.append(suggest_author_books.loc[i][2])
        item.append(suggest_author_books.loc[i][1])
        
        data.append(item)
    print(data)

    return render_template('author.html',data=data)

@app.route('/recommend.html')
def recommend():
    return render_template('recommend.html')

@app.route('/recommend_results',methods=["post"])
def recommend_results():
    input_user = request.form.get('input_user')
    index = np.where(pt.index==input_user)[0][0]
    similar_items = sorted(list(enumerate(similarity_scores[index])),key=lambda x:x[1],reverse=True)[1:5]
    
    data = []
    for i in similar_items:
        item = []
        temp_df = df_books[df_books['Book-Title'] == pt.index[i[0]]]
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Title'].values))
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Author'].values))
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Image-URL-M'].values))
        
        data.append(item)
    print(data)
    
    return render_template('recommend.html',data=data)

if __name__ == '__main__':
    app.run(debug = True)
