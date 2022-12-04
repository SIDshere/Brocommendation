from  flask import Flask,render_template,request
import pickle, bz2
import numpy as np

popular_df=pickle.load(bz2.open("popular.pkl","rb"))
pt=pickle.load(bz2.open("pt.pkl","rb"))
df=pickle.load(bz2.open("df.pkl","rb"))
scores=pickle.load(bz2.open("scores.pkl","rb"))
app=Flask(__name__)

@app.route("/")
def recommend_ui():
    return render_template("recommend.html")

@app.route("/recommend",methods=["post"])
def recommend():
    user_input=request.form.get("user_input")
    index=np.where(pt.index==user_input)[0][0]
    similar=sorted(list(enumerate(scores[index])),key=lambda x:x[1],reverse=True)[1:11]
    
    data=[]
    for i in similar:
        item=[]
        temp=df[df["Book-Title"]==pt.index[i[0]]]
        item.extend(list(temp.drop_duplicates("Book-Title")["Image-URL-M"]))
        item.extend(list(temp.drop_duplicates("Book-Title")["Book-Title"]))
        item.extend(list(temp.drop_duplicates("Book-Title")["Book-Author"]))
        data.append(item)
    return render_template("recommend.html",data=data)

if __name__=="__main__":
    app.run(debug=True)