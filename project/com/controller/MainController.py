from flask import render_template

from project import app



@app.route('/admin/loadFile')
def adminLoadFile():
    return render_template("admin/viewFile.html")


@app.route('/user/loadFile')
def userLoadFile():
    return render_template("user/addFile.html")




