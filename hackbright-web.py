from flask import Flask, request, render_template

import hackbright

app = Flask(__name__)

@app.route("/student_search")
def get_student_form():
    """Show form for searching for a student."""

    return render_template("student_search.html") 

@app.route("/student")
def get_student():
    """Show information about a student."""

    github = request.args.get('github', 'jhacks')
    first, last, github = hackbright.get_student_by_github(github)
    return render_template('student_info.html',
                            github=github, 
                            first=first,
                            last=last)

@app.route("/student_add_form")
def student_add_form():
    return render_template('student_add.html')

@app.route("/student_add", methods=['POST'])
def student_add():
    """Add a student."""

    github = request.form.get('github')
    firstname = request.form.get('first_name')
    lastname = request.form.get('last_name')
    hackbright.make_new_student(firstname, lastname, github)     
    return render_template('student_info.html',
                            github=github, 
                            first=firstname,
                            last=lastname)

if __name__ == "__main__":
    hackbright.connect_to_db(app)
    app.run(debug=True)
