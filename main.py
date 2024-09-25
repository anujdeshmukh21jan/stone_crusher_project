from flask import Flask,render_template,request,url_for,redirect,session
import re
import requests, json
from PIL import Image
from PIL import Image
import imagehash

app=Flask(__name__)

@app.route('/apple')
def apple():
    return render_template('apple.html')
@app.route('/banana')
def banana():
    return render_template('banana.html')
@app.route('/watermelon')
def watermelon():
    return render_template('watermelon.html')
@app.route('/grapes')
def grapes():
    return render_template('grapes.html')
@app.route('/pineapple')
def pineapple():
    return render_template('pineapple.html')
@app.route('/none')
def none():
    return render_template('none.html')

@app.route('/', methods=['GET','POST'])
def index():
    if request.method == 'POST':
        file = request.form['file']
        p=['apple.jpg','banana.jpg','watermelon.jpg','grapes.jpg','pineapple.jpg']
        ans=[]
        for i in range(0,len(p)):
            hash1 = imagehash.average_hash(Image.open('images/'+p[i]))
            hash2 = imagehash.average_hash(Image.open('images/'+file))
            diff = hash1 - hash2
            ans.append(diff)
        print(ans)
        if min(ans)<=6:
            ans1=p[ans.index(min(ans))][:-4]
        else:
            ans1='none'
        print(ans1)
        if ans1=='apple':
            print(ans1)
            return redirect(url_for('apple'))
        elif ans1=='banana':
            return redirect(url_for('banana'))
        elif ans1=='watermelon':
            return redirect(url_for('watermelon'))
        elif ans1=='grapes':
            return redirect(url_for('grapes'))
        elif ans1=='pineapple':
            return redirect(url_for('pineapple'))
        else:
            return redirect(url_for('none'))
    return render_template('index1.html')


if __name__ == "__main__":
    app.run(debug=True)
