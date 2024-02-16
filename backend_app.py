from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # This will enable CORS for all routes

POSTS = [
    {"id": 1, "title": "First post", "content": "This is the first post."},
    {"id": 2, "title": "Second post", "content": "This is the second post."},
]


@app.errorhandler(400)
def handle_400_error():
    return "Bad request, title or content was not provided", 400


@app.route('/api/posts/search', methods=['GET'])
def search():
    result = []
    track = {}

    title = request.args.get('title')
    content = request.args.get('content')

    if title is not None or content is not None:
        for post in POSTS:
            if title is not None and post['title'].find(title) != -1:
                result.append(post)
                track[post['id']] = True
            if content is not None and post['content'].find(content) != -1:
                if track.get(post['id']):
                    continue
                result.append(post)
                track[post['id']] = True

    return jsonify(result)


@app.route('/api/posts/<int:post_id>', methods=['DELETE', 'PUT'])
def delete(post_id):
    idx = 0
    ans = None
    for post in POSTS:
        if post_id == post['id']:
            ans = idx
            break
        idx += 1

    if ans is None:
        return "404 Not Found", 404

    if request.method == 'PUT':
        post = POSTS[ans]
        data = request.get_json()
        if data.get('title') is not None:
            post['title'] = data.get('title')
        if data.get('content') is not None:
            post['content'] = data.get('content')
        return jsonify(post)

    if request.method == 'DELETE':
        POSTS.pop(ans)
        return jsonify({
            "message": f"Post with id {post_id} has been deleted successfully."
        })


@app.route('/api/posts', methods=['GET', 'POST'])
def get_posts():
    if request.method == 'GET':
        sort_by = request.args.get('sort')
        sort_direction = request.args.get('direction')

        if sort_by is not None:
            if sort_by != 'title' or sort_by != 'content':
                return '400 Bad Response', 400
            if sort_by == 'title' or sort_by == 'content':
                if sort_direction is not None:
                    if sort_direction != 'asc' or sort_direction == 'desc':
                        return '400 Bad Response', 400
                    if sort_direction == 'desc':
                        sorted_posts_desc = sorted(POSTS, key=lambda x: x[sort_by], reverse=True)
                        return jsonify(sorted_posts_desc)
                    else:
                        sorted_posts_asc = sorted(POSTS, key=lambda x: x[sort_by])
                        return jsonify(sorted_posts_asc)
                return jsonify(sorted(POSTS, key=lambda x: x[sort_by]))
        return jsonify(POSTS)
    elif request.method == 'POST':
        new_id = POSTS[-1]['id'] + 1
        data = request.get_json()

        if data.get("title") is None or data.get('content') is None:
            response_text = ""
            if data.get('title') is None and data.get('content') is None:
                response_text = "Missing title and content"
            elif data.get('content') is None:
                response_text = "Missing content"
            elif data.get('title') is None:
                response_text = "Missing title"
            return response_text, 400

        title = data['title']
        content = data['content']

        new_post = {"id": new_id, "title": title, "content": content}

        POSTS.append(new_post)

        return jsonify(POSTS)


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5002, debug=True)
