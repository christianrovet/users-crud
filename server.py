from flask import Flask, render_template, request, redirect
from mysqlconnection import connectToMySQL
app = Flask(__name__)
@app.route("/")
def index():
    mysql = connectToMySQL('first_flask')
    friends = mysql.query_db('SELECT * FROM friends;')
    print(friends)
    return render_template("index.html", all_friends = friends)

@app.route("/create_friend", methods=["POST"])
def add_friend_to_db():
    mysql = connectToMySQL('first_flask')

    query = "INSERT INTO friends (first_name, last_name, occupation, created_at, updated_at) VALUES (%(first_name)s,%(last_name)s, %(occupation)s, NOW(), NOW());"
    data = {
        "first_name": request.form["firstname"],
        "last_name": request.form["lastname"],
        "occupation": request.form["occ"]
    }
    new_friend_id = mysql.query_db(query, data)
    return redirect('/results')

@app.route('/results')
def results():
    mysql = connectToMySQL('first_flask')
    friends = mysql.query_db('SELECT * FROM friends;')
    return render_template("results.html", all_friends = friends)

@app.route('/users/<user_num>')
def user_card(user_num):
    user_q = 'SELECT id,first_name,last_name,occupation FROM friends WHERE id = %(user_num)s;'
    data = {'user_num' : user_num}
    mysql = connectToMySQL('first_flask')
    friend = mysql.query_db(user_q,data)
    return render_template("user.html", the_friend = friend)

@app.route('/edit_person/<edit_person_num>')
def edit(edit_person_num):
    edit_q = 'SELECT id,first_name,last_name,occupation FROM friends WHERE id = %(edit_person_num)s;'
    data = {'edit_person_num' : edit_person_num}
    mysql = connectToMySQL('first_flask')
    edit = mysql.query_db(edit_q,data)
    return render_template('edit.html', edit_friend = edit)

@app.route("/edit/<edit_num>", methods=["POST"])
def edit_person(edit_num):
    mysql = connectToMySQL('first_flask')
    query = "UPDATE friends SET first_name = %(first_name)s, last_name = %(last_name)s,occupation = %(occupation)s WHERE id =%(edit_num)s;"
    data = {
        "first_name": request.form["firstname"],
        "last_name": request.form["lastname"],
        "occupation": request.form["occ"],
        "edit_num": edit_num
    }
    edit_person = mysql.query_db(query,data)
    return redirect('/results')

@app.route("/delete_person/<delete_num>")
def delete(delete_num):
    mysql = connectToMySQL('first_flask')
    query = "DELETE FROM friends WHERE id=%(delete_num)s;"
    data = {
        "delete_num": delete_num
    }
    delete_person = mysql.query_db(query,data)
    return redirect('/results')

if __name__ == "__main__":
    app.run(debug=True)

