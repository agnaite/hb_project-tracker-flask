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
    project = hackbright.get_grades_by_github(github)
    return render_template('student_info.html',
                            github=github, 
                            first=first,
                            last=last,
                            project=project)


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


@app.route('/project', methods=['GET'])
def get_project():
    """Show information about a student."""
    student_names = []
    grades = []
    usernames = []

    title = request.args.get('title')
    title, description, max_grade = hackbright.get_project_by_title(title)
    student_list = hackbright.get_grades_by_title(title)

    for student in student_list:
        first_name, last_name, github = hackbright.get_student_by_github(student[0])
        student_names.append(first_name + " " + last_name)
        usernames.append(github)
        grades.append(student[1])

    student_list = zip(student_names, grades, usernames)

    return render_template('project_info.html',
                            title=title, 
                            description=description,
                            max_grade=max_grade,
                            student_list=student_list)


@app.route('/project_search')
def get_project_form():
    """Show form for searching for a project."""

    return render_template("project_search.html")


if __name__ == "__main__":
    hackbright.connect_to_db(app)
    app.run(debug=True)
