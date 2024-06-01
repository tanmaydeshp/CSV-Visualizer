from flask import render_template, url_for, redirect, Blueprint, request, flash, current_app as app, jsonify, send_from_directory
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
import os 
from . import db
from .models import File
from datetime import datetime
import json 

views = Blueprint("views", __name__)

@views.route('/')
def home(): 
    return render_template('index.html', user=current_user)


@views.route('/myfiles/', methods=['GET', 'POST'])
@login_required
def myfiles():
    if request.method == "POST":
        if 'file' not in request.files:
            flash("No file part!", category="error")
        file = request.files['file']
        if file.filename == "":
            flash("No file uploaded!", category="error")
        if file: 
            filename = secure_filename(file.filename)
            path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            if path.exists(path):
                flash('A file with the same name already exists!', category='error')
            file.save(path)
            f = File(path=path, author_id = current_user.id, uploaded_at= datetime.now(), filename=filename)
            db.session.add(f)
            db.session.commit()
            flash("File uploaded successfully", category="success")
            return render_template('myfiles.html', user=current_user)
    return render_template("myfiles.html", user=current_user)

@views.route('/delete_file/', methods=['POST'])
@login_required
def delete_file() :
    filedict = request.get_json()
    fileID = filedict["fileID"] 
    file = File.query.get(int(fileID))
    if file and file.author_id == current_user.id: 
        db.session.delete(file)
        db.session.commit()
        os.remove(file.path)
        flash("File deleted successfully!", category="success")
    return jsonify({})

@views.route('/uploads/<filename>')
@login_required 
def download_file(filename):
    file = File.query.filter_by(filename=filename).first()
    if file and file.author_id == current_user.id:
        return send_from_directory(app.config['UPLOAD_FOLDER'], file.filename, as_attachment=True)


        

