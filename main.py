from flask import Flask, render_template, url_for, request
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import TfidfVectorizer
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from nltk import word_tokenize 
import os 
import re

cached_stop_words = stopwords.words('english')

def Tokenizer(str_input):
    words = re.sub(r"[^A-Za-z0-9\-]", " ", str_input).lower().split()
    porter_stemmer=PorterStemmer()
    words = [porter_stemmer.stem(word) for word in words]
    return words

def predicter(review):
    classifier = Pipeline([
        ('vec',TfidfVectorizer(tokenizer = Tokenizer, stop_words = cached_stop_words)),
        ('cla',MultinomialNB())
    ])
    
    file = open('dataset.txt', 'r')
    content = file.readlines()

    data = []
    target = []

    for i in content:
        x, y = i.split('+')
        data.append(x)
        target.append(y)

    classifier.fit(data,target)
    file.close()
    print(review)
    ans = int(classifier.predict(review.split('\n'))[0])
    if(ans==-1):
        print("Negative")
    else:
        print("Positive")
    return(ans)

   
star_folder = os.path.join('static', 'stars')

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = star_folder
neg = [1]*6
pos = [1]*6
img = ['static/stars/1.png']*6
@app.route('/', methods=['POST', 'GET'])
def index():
    if('submit1' in request.form):
        data = request.form['text1'] 
        result=predicter(data)
        if(result==-1):
            neg[1]+=1
        else:
            pos[1]+=1
        rating = pos[1]//neg[1]
        if(rating>5):
            rating=5
        img[1] = os.path.join(app.config['UPLOAD_FOLDER'], str(rating)+'.png')
    elif('submit2' in request.form):
        data = request.form['text2'] 
        result=predicter(data)
        if(result==-1):
            neg[2]+=1
        else:
            pos[2]+=1
        rating = pos[2]//neg[2]
        if(rating>5):
            rating=5
        img[2] = os.path.join(app.config['UPLOAD_FOLDER'], str(rating)+'.png')
        print(data)
    elif('submit3' in request.form):
        data = request.form['text3'] 
        result=predicter(data)
        if(result==-1):
            neg[3]+=1
        else:
            pos[3]+=1
        rating = pos[3]//neg[3]
        if(rating>5):
            rating=5
        img[3] = os.path.join(app.config['UPLOAD_FOLDER'], str(rating)+'.png')
    elif('submit4' in request.form):
        data = request.form['text4'] 
        result=predicter(data)
        if(result==-1):
            neg[4]+=1
        else:
            pos[4]+=1
        rating = pos[4]//neg[4]
        if(rating>5):
            rating=5
        img[4] = os.path.join(app.config['UPLOAD_FOLDER'], str(rating)+'.png')
    elif('submit5' in request.form):
        data = request.form['text5'] 
        result=predicter(data)
        if(result==-1):
            neg[5]+=1
        else:
            pos[5]+=1
        rating = pos[5]//neg[5]
        if(rating>5):
            rating=5
        img[5] = os.path.join(app.config['UPLOAD_FOLDER'], str(rating)+'.png')
    for i in range(1,6):
        print(pos[i], neg[i])
    return render_template("index.html", user_image1 = img[1], user_image2 = img[2], user_image3 = img[3], user_image4 = img[4] ,user_image5 = img[5])




if __name__ == "__main__":
    app.run(debug=False)