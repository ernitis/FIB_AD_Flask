from flask import Flask, request, send_file, jsonify
from PIL import Image, ImageFilter
import io
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config["MAX_CONTENT_LENGTH"] = 16 * 1024 * 1024  # 16 MB limit

ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "gif", "bmp", "tiff", "webp"}


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


def apply_filter(request, filter):
    """
    RESTful endpoint to apply a filter to an uploaded image.
    Expects:
      - Image file with key 'image' in form-data.
      - Optional 'filter' field specifying the filter name.
    Returns:
      - Filtered image in PNG format.
    """
    # Check if 'image' is part of the request
    if "image" not in request.files:
        return jsonify({"error": "No image file provided."}), 400

    file = request.files["image"]

    # Check if a file was selected
    if file.filename == "":
        return jsonify({"error": "No file selected."}), 400

    # Validate file type
    if not allowed_file(file.filename):
        return jsonify({"error": "Unsupported file type."}), 400

    try:
        # Open the image
        img = Image.open(file.stream)

        # Choose the filter; default to BLUR if not found
        chosen_filter = filter
        filtered_img = img.filter(chosen_filter)

        # Save the filtered image to a BytesIO object
        img_io = io.BytesIO()
        filtered_img.save(img_io, "PNG")
        img_io.seek(0)

        return send_file(img_io, mimetype="image/png"), 200

    except Exception as e:
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500


@app.route("/filter_1", methods=["POST"])
def apply_filter_1():
    return apply_filter(request, ImageFilter.EDGE_ENHANCE_MORE)


@app.route("/filter_2", methods=["POST"])
def apply_filter_2():
    return apply_filter(request, ImageFilter.CONTOUR)


@app.route("/filter_3", methods=["POST"])
def apply_filter_3():
    return apply_filter(request, ImageFilter.EMBOSS)


if __name__ == "__main__":
    app.run(port=8080, debug=True)
