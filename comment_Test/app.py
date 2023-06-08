from flask import Flask, render_template, request, jsonify
app = Flask(__name__)
from flask_jwt_extended import JWTManager, create_access_token, jwt_required
from pymongo import MongoClient
client = MongoClient('mongodb+srv://sparta:test@cluster0.x0xikyx.mongodb.net/?retryWrites=true&w=majority')
db = client.dbsparta
import requests

@app.route('/')
def home():
    return render_template('index.html')

@app.route("/comments", methods=["POST"])
def comment_post():
    comments_list = list(db.comments.find({}, {'_id': False}))
    count = len(comments_list) + 1
    
    commentId_receive = request.form['comment_id_give']
    commentPw_receive = request.form['comment_pw_give']
    comment_receive = request.form['comment']

    doc = {
        'num':count,
        'comment-id':commentId_receive,
        'comment-pw':commentPw_receive,
        'comment':comment_receive,
    }
    db.comments.insert_one(doc)
    
    return jsonify({'msg':'DB에 저장함!'})

@app.route("/movie", methods=["GET"])
def movie_get():
    all_movies = list(db.movies.find({},{'_id':False}))
    return jsonify({'result':all_movies})

@app.route("/comments", methods=["GET"])
def comment_get():
    all_comments = list(db.comments.find({},{'_id':False}))
    return jsonify({'result':all_comments})

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)