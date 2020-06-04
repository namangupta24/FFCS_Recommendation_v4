from flask import Flask, render_template, url_for, request
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import TfidfVectorizer
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from nltk import word_tokenize 
import os 
import re

#storing a cached copy of stopwords
cached_stop_words = set(stopwords.words('english'))

#definig directory which contain start images
star_folder = os.path.join('static', 'stars')

def Tokenizer(str_input):
    words = re.sub(r"[^A-Za-z0-9\-]", " ", str_input).lower().split() #replaces everything not in re to <space>
    porter_stemmer=PorterStemmer()
    words = [porter_stemmer.stem(word) for word in words if not word in cached_stop_words] #creates the list after stemming and stop word removal 
    return words

def predicter(review):
    #creating a pipeline which used tdidf as vectorizer and mutinomial naive bayes as classifier
    classifier = Pipeline([
        ('vec',TfidfVectorizer(tokenizer = Tokenizer)),
        ('cla',MultinomialNB())
    ])
    
    file = open('dataset.txt', 'r')
    content = file.readlines() #reading content of the dataset

    data = []
    target = []

    for i in content:
        x, y = i.split('+')
        data.append(x) # appending review to data list
        target.append(y) #appending rating to target list

    classifier.fit(data,target) #using classifier to fit the data
    file.close()
    print(review) #prints review statement (inputted as argument to function)
    ans = int(classifier.predict(review.split('\n'))[0]) #predicts the sentiment of the review and stores it as int
    if(ans==-1):
        print("Negative")
    else:
        print("Positive")
    return(ans) #return the sentiment (1 or -1)

   

app = Flask(__name__) #creating flask app
app.config['UPLOAD_FOLDER'] = star_folder
neg = [1]*6 #intializing list for negative scores
pos = [1]*6 #intializing list for positive scores
img = ['static/stars/1.png']*6 #initial image for all teachers

@app.route('/', methods=['POST', 'GET']) #handling request at '/'
def index():
    if('submit1' in request.form): #checking if input is there for form 1 
        data = request.form['text1'] #inputs data 
        result=predicter(data) # does sentiment analysis
        if(result==-1): #if result is negative then increases negative score for particular teacher  
            neg[1]+=1
        else: # else increases positive score for particular teacher
            pos[1]+=1
        rating = pos[1]//neg[1] # calculates the rating
        if(rating>5): # capping max to 5 start
            rating=5
        img[1] = os.path.join(app.config['UPLOAD_FOLDER'], str(rating)+'.png') #loading star image
    elif('submit2' in request.form): #same procedure as above
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
    elif('submit3' in request.form): #same procedure as above
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
    elif('submit4' in request.form): #same procedure as above
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
    elif('submit5' in request.form): #same procedure as above
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
        print pos[i], neg[i]
    #rendering the HTML webpage with updated start images
    return render_template("index.html", user_image1 = img[1], user_image2 = img[2], user_image3 = img[3], user_image4 = img[4] ,user_image5 = img[5])




if __name__ == "__main__":
    app.run(debug=False) #runnig the flask app