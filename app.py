from flask import Flask, render_template ,request,  redirect
from flask_pymongo import PyMongo


app = Flask(__name__)
# app.config["MONGO_URI"] = "mongodb://localhost:27017/myDatabase"
# app.config["MONGO_URI"] = "cloud database link"
mongo = PyMongo(app)



@app.route('/', methods=['GET','POST'])
def index():
    if request.method=="POST":
        Name=request.form["name"]
        Author=request.form["author"]
        Type=request.form["check"]
        # print(Name, Author, Type)
        mongo.db.LibraryData.insert_one({
        "name":Name,
        "author":Author,
        "type": Type
        })
    # data= mongo.db.LibraryData.find({})
    data_cursor= mongo.db.LibraryData.find()
    # print(data_cursor) # this prints data is in cursor object, see here in terminal
    names = []
    authors = []
    types = []
    ids = []
    for item in data_cursor:
        names.append(item['name'])
        authors.append(item['author'])
        types.append(item['type'])
        ids.append(item['_id'])
        # print(item['_id'])
        

    data_dict = {
        "bookId":ids,
        "name": names,
        "author": authors,
        "type": types
    }
    # print(data_dict)

    return render_template("index.html", data=data_dict)



@app.route('/delete/<ObjectId:id>')
def delete(id):
    # print(id)
    mongo.db.LibraryData.delete_one({'_id': id})
    # print("Note is deleted")
    return redirect("/")
    

@app.route('/update/<ObjectId:id>' , methods=['GET','POST'])
def update(id):
    if request.method=='POST':
        name=request.form["name"]
        author=request.form["author"]
        type=request.form["check"]
        # print(name, author, type)
        # data=mongo.db.LibraryData.find_one({'_id': id})
        # print(data)
        mongo.db.LibraryData.update_one(
        {'_id': id},
        { "$set": 
         { "name": name, "author" : author, "type":type } })
        return redirect("/")
    # print(id)
    data=mongo.db.LibraryData.find_one({'_id': id})
    # print(data)
    return render_template("update.html", data=data)




if __name__=="__main__":
    app.run(debug=True)