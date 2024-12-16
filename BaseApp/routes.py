from flask import render_template, request, session, redirect, url_for
from sqlalchemy.exc import IntegrityError
from sqlalchemy import func
from mimetypes import guess_type
import requests
from models import User, Image
import error_codes
import file_manager
from datetime import date
import globals


REST_API_URL = f"http://{globals.getIp()}:8080/"


def register_routes(app, db):

    @app.route("/")
    def index():
        username = session.get("username")
        if username:
            user = User.query.filter_by(username=username).first()
            if user:
                return redirect(url_for("menu"))
        return render_template("index.html")

    @app.route("/error")
    def error():
        return render_template("error.html")

    @app.route("/login", methods=["POST"])
    def login():
        username = request.form.get("username")
        password = request.form.get("password")
        existing_user = User.query.filter_by(
            username=username, password=password
        ).first()

        if existing_user:
            print("user exists")
            session["username"] = username
            return redirect(url_for("menu"))
        else:
            print("user  does NOT exists")
            session.clear()
            session["error"] = error_codes.INVALID_LOGIN
            return redirect(url_for("error"))

    @app.route("/signUp", methods=["POST"])
    def signUp():
        username = request.form.get("username")
        password = request.form.get("password")

        new_user = User(username=username, password=password)
        try:
            db.session.add(new_user)
            db.session.commit()
            session["username"] = username
            return redirect(url_for("menu"))
        except IntegrityError:
            db.session.rollback()
            session["error"] = error_codes.USER_ALREADY_EXISTS
            return redirect(url_for("error"))
        except Exception as e:
            db.session.rollback()
            session["error"] = error_codes.UNKNOWN
            return redirect(url_for("error"))

    @app.route("/logout")
    def logout():
        session.clear()
        return redirect(url_for("index"))

    @app.route("/deleteUser", methods=["POST"])
    def deleteUser():
        username = session.get("username")
        print(f"Deleting User {username}")
        if not username:
            session["error"] = error_codes.INVALID_SESSION
            return redirect(url_for("error"))

        user = User.query.filter_by(username=username).first()

        if not user:
            session["error"] = error_codes.UNKNOWN
            return redirect(url_for("error"))

        images = Image.query.filter_by(creator=username).all()
        for image in images:
            db.session.delete(image)
        db.session.delete(user)
        db.session.commit()
        file_manager.delete_user_directory(username)
        return redirect(url_for("index"))

    @app.route("/menu")
    def menu():
        username = session.get("username")
        if username:
            user = User.query.filter_by(username=username).first()
            if not user:
                return redirect(url_for("index"))
        return render_template("menu.html")

    @app.route("/addImage", methods=["GET", "POST"])
    def addImage():
        if request.method == "GET":
            return render_template("add_image.html")
        elif request.method == "POST":
            title = request.form.get("title")
            description = request.form.get("description")
            keywords = request.form.get("keywords")
            author = request.form.get("author")
            creator = request.form.get("creator")
            creationDate = request.form.get("creationDate")
            uploadDate = date.today().strftime("%Y-%m-%d")
            file = request.files["image"]
            filename = file_manager.getRandomFilename(file.filename)

            ALLOWED_CONTENT_TYPES = {
                "image/png",
                "image/jpeg",
                "image/tiff",
                "image/webp",
            }
            if file.content_type not in ALLOWED_CONTENT_TYPES:
                session["error"] = error_codes.INVALID_IMAGE_FILE
                return redirect(url_for("error"))

            image = Image(
                title=title,
                description=description,
                keywords=keywords,
                author=author,
                creator=creator,
                creationDate=creationDate,
                uploadDate=uploadDate,
                filename=filename,
            )
            try:
                db.session.add(image)
                db.session.commit()
                file_manager.save_image(creator, file, filename)
                return redirect(url_for("userImages"))
            except Exception as e:
                db.session.rollback()
                session["error"] = f"Error Uploading Image: {e}"
                return redirect(url_for("error"))

    @app.route("/findImagesByCreator/<creator>")
    def findImagesByCreator(creator):
        images = Image.query.filter_by(creator=creator).all()
        images_data = [image.to_dict() for image in images]
        return render_template("image_list.html", images=images_data)

    @app.route("/userImages")
    def userImages():
        username = session.get("username")
        if not username:
            return redirect(url_for("index"))

        return redirect(url_for("findImagesByCreator", creator=username))

    @app.route("/searchImages", methods=["GET", "POST"])
    def searchImages():
        if request.method == "GET":
            return render_template("search_images.html")
        else:
            title = request.form.get("title")
            description = request.form.get("description")
            keywords = request.form.get("keywords")
            author = request.form.get("author")

            # Start with the base query
            query = Image.query

            # Apply filters conditionally
            if title:
                query = query.filter(func.lower(Image.title).like(f"%{title.lower()}%"))
            if description:
                query = query.filter(
                    func.lower(Image.description).like(f"%{description.lower()}%")
                )
            if keywords:
                query = query.filter(
                    func.lower(Image.keywords).like(f"%{keywords.lower()}%")
                )
            if author:
                query = query.filter(
                    func.lower(Image.author).like(f"%{author.lower()}%")
                )

            # Execute the query
            results = query.all()
            return render_template("image_list.html", images=results)

    @app.route("/imageFilters/<id>", methods=["GET"])
    def imageFilters(id, filter=0):
        image = Image.query.filter_by(id=int(id)).first()
        filter = request.args.get("filter", 0)
        if filter == 0:
            return render_template("image_filters.html", image=image)

        # Call the REST API to apply the filter
        try:
            # Prepare the API request (replace with your API's specifics)
            api_endpoint = f"{REST_API_URL}/filter_{filter}"

            # Convert the image to a file-like object
            imagePath = file_manager.path_for_image(image.creator, image.filename)
            mimetype, _ = guess_type(imagePath)

            with open(imagePath, "rb") as img_file:
                files = {"image": (image.filename, img_file, mimetype)}
                response = requests.post(api_endpoint, files=files)

            # Check for a successful response
            if response.status_code != 200:
                session["error"] = response.content
                return redirect(url_for("error"))

            # Get the image data from the API response
            image_data = response.content

            filename = file_manager.save_temp_image(image_data)

            # Generate the URL to access the temp image
            tmp_url = url_for("static", filename=f"temp/{filename}")

            # Render the template with the temporary image
            return render_template("image_filters.html", image=image, tempUrl=tmp_url)

        except Exception as e:
            session["error"] = f"An error occurred: {e}"
            return redirect(url_for("error"))

    @app.route("/modifyImage", methods=["GET", "POST"])
    def modifyImage():
        if request.method == "GET":
            id = int(request.args.get("id"))
            image = Image.query.filter_by(id=id).first()
            if not image:
                session["error"] = error_codes.IMAGE_NOT_FOUND
                return redirect(url_for("error"))
            return render_template("modify_image.html", image=image)
        elif request.method == "POST":
            id = int(request.form.get("id"))
            image = Image.query.filter_by(id=id).first()
            if not image:
                session["error"] = error_codes.IMAGE_NOT_FOUND
                return redirect(url_for("error"))
            if image.creator != session.get("username"):
                session["error"] = error_codes.NO_PERMISSIONS
                redirect(url_for("error"))

            image.title = request.form.get("title")
            image.description = request.form.get("description")
            image.keywords = request.form.get("keywords")
            image.author = request.form.get("author")
            image.creationDate = request.form.get("creationDate")

            try:
                db.session.commit()
                return redirect(url_for("userImages"))
            except Exception as e:
                db.session.rollback()
                session["error"] = f"Error Modifying Image: {e}"
                return redirect(url_for("error"))

    @app.route("/deleteImage", methods=["POST"])
    def deleteImage():
        id = int(request.form.get("id"))
        image = Image.query.filter_by(id=id).first()
        if not image.creator == session.get("username"):
            session["error"] = error_codes.NO_PERMISSIONS
            return redirect(url_for("error"))

        try:
            file_manager.delete_image(image.creator, image.filename)
            db.session.delete(image)
            db.session.commit()
            return redirect(url_for("userImages"))
        except Exception as e:
            session["error"] = f"Error Deleting Image: {e}"
            return redirect(url_for("error"))
