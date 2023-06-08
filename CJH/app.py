from flask import Flask, render_template, jsonify, request

app = Flask(__name__)

comments = []  # 댓글을 저장할 리스트

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/comments", methods=["GET", "POST"])
def handle_comments():
    if request.method == "GET":
        return jsonify({"result": "success", "comments": comments})
    elif request.method == "POST":
        comment_text = request.form.get("comment")
        if comment_text:
            new_comment = {"author": "사용자ID 등록할 곳", "text": comment_text}
            comments.append(new_comment)
            return jsonify({"result": "success"})
        else:
            return jsonify({"result": "error", "message": "Invalid comment."})

if __name__ == "__main__":
    app.run()
