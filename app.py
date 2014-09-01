from PIL import Image

import random
import string
import flask
import os
import io

app = flask.Flask(__name__)
app.config["UPLOAD_FOLDER"] = "./"
app.config["ALLOWED_IMG_EXTENSIONS"] = ('.png', '.jpeg', '.jpg', '.svg', '.gif', '.bmp')

def get_filename(ext):
    res = []
    for i in range(5):
        res.append(random.choice(string.ascii_letters))
    return ''.join(res) + ext

@app.route("/view/<filename>")
@app.route("/<filename>")
def view(filename):
    return flask.render_template("view.html", filename=filename, title=filename)

@app.route("/about")
def about():
    return flask.render_template("about.html", title="About plzimg")

@app.route('/', methods=["POST"])
def post_img():
    request = flask.request
    file = request.files['file']
    if not file.filename:
        return flask.render_template("error.html", message="Please provide a file", title="Error")
    name, ext = os.path.splitext(file.filename)
    ext = ext.lower()
    if ext not in app.config['ALLOWED_IMG_EXTENSIONS']:
        return flask.render_template("error.html", message="Forbidden file extension: %s" % (ext,), title="Error")
    filename = get_filename(ext)
    data = file.read()
    with open(os.path.join(app.config['UPLOAD_FOLDER'], 'o', filename), "wb") as fd:
        fd.write(data)
    data = io.BytesIO(data)
    image = Image.open(data)
    max_width, max_height = (500, 500)
    width, height = image.size
    if width > max_width or height > max_height:
        width_ratio = max_width / width
        height_ratio = max_height / height
        ratio = min(width_ratio, height_ratio)
        height = height * ratio
        width = width * ratio
        try:
            image = image.resize((int(width), int(height)))
        except Exception as e:
            pass
    image.save(os.path.join(app.config['UPLOAD_FOLDER'], 's', filename))
    return flask.redirect(flask.url_for("view", filename=filename))

@app.route('/', methods=['GET'])
def main():
    img = flask.request.args.get("img")
    if img:
        return flask.redirect(flask.url_for("view", filename=img))
    return flask.render_template("index.html", title="Index")

if __name__ == "__main__":
    app.run(debug=False)
