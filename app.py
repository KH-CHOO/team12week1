from flask import Flask, render_template, request, jsonify
from pymongo import MongoClient

app = Flask(__name__)

client = MongoClient('mongodb+srv://sparta:test@cluster0.iw4krrz.mongodb.net/?retryWrites=true&w=majority')
db = client.dbsparta


@app.route('/')
def home():
    return render_template('index.html')

@app.route("/members", methods=["GET"])
def movie_get():
    all_members = list(db.members.find({},{'_id':False}))
    return jsonify({'result':all_members})

@app.route("/comments", methods=["POST"])
def comment_post():
    comments_list = list(db.comments.find({}, {'_id': False}))
    count = len(comments_list) + 1

    commentName_receive = request.form['comment_name_give']
    commentPw_receive = request.form['comment_pw_give']
    comment_receive = request.form['comment']

    doc = {
        'comment-id':count,
        'comment-name':commentName_receive,
        'comment-pw':commentPw_receive,
        'comment':comment_receive,
    }
    db.comments.insert_one(doc)
    
    return jsonify({'msg':'작성완료!'})

@app.route("/comments", methods=["GET"])
def comment_get():
    all_comments = list(db.comments.find({},{'_id':False}))
    return jsonify({'result':all_comments})

@app.route("/comments/<int:comment_id>", methods=["PUT"])
def comment_put(comment_id):
    comment = db.comments.find_one({'comment-id': comment_id})
    if comment and comment['comment-pw'] == request.form.get('comment_pw_give'):
        comment_receive = request.form.get('comment')
        db.comments.update_one({'comment-id': comment_id}, {'$set': {'comment': comment_receive}})
        return jsonify({'msg': '수정 완료!'}), 200
    else:
        return jsonify({'error': '잘못된 비밀번호입니다.'}), 404


@app.route("/comments/<int:comment_id>", methods=["DELETE"])
def comment_delete(comment_id):
    comment = db.comments.find_one({'comment-id': comment_id})
    if comment and comment['comment-pw'] == request.form.get('comment_pw_give'):
        db.comments.delete_one({'comment-id': comment_id})
        return jsonify({'msg': '삭제 완료!'}), 200
    else:
        return jsonify({'error': '잘못된 비밀번호입니다.'}), 404

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)