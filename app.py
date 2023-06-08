from flask import Flask, request, jsonify
from pymongo import MongoClient

app = Flask(__name__)

client = MongoClient('mongodb://localhost:27017')
db = client['commentdb']
collection = db['comments']
@app.route('/comments', methods=['GET'])
def get_comments():
    comments = list(collection.find())
    return jsonify(comments)

@app.route('/comments', methods=['POST'])
def add_comment():
    data = request.get_json()
    comment = data['comment']
    collection.insert_one({'comment': comment})
    return jsonify({'message': 'Comment added successfully'})

@app.route('/comments/<comment_id>', methods=['DELETE'])
def delete_comment(comment_id):
    result = collection.delete_one({'_id': comment_id})
    if result.deleted_count > 0:
        return jsonify({'message': 'Comment deleted successfully'})
    else:
        return jsonify({'message': 'Comment not found'})

if __name__ == '__main__':
    app.run()
