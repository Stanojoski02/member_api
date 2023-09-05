from flask import Flask, g, request, jsonify
import sqlite3


def connect_db():
    sql = sqlite3.connect("members.db")
    sql.row_factory = sqlite3.Row
    return sql


def get_db():
    if not hasattr(g, "sqlite_db"):
        g.sqlite_db = connect_db()
    return g.sqlite_db


app = Flask(__name__)


@app.route('/member', methods=['GET'])
def get_members():
    db = get_db()
    members_cur = db.execute('select id, name, email from members')
    members = members_cur.fetchall()
    return_values = []
    for member in members:
        member_dict = {"id": member['id'], "name": member['name'], 'email': member['email']}
        return_values.append(member_dict)
    return jsonify({"members": return_values})


@app.route("/member/<int:member_id>", methods=["GET"])
def get_member(member_id):
    db = get_db()
    member_cur = db.execute("select * from members where id = ?", [member_id])
    member = member_cur.fetchone()
    member_dict = {'name': member['name'], "email": member['email'], 'id': member["id"]}
    return jsonify(member_dict)


@app.route("/member", methods=["POST"])
def add_member():
    db = get_db()
    new_member_data = request.get_json()
    name = new_member_data['name']
    email = new_member_data['email']
    level = new_member_data['level']
    db.execute("insert into members (name, email, level) values (?, ?, ?)", [name, email, level])
    db.commit()
    member_cur = db.execute("select id, name, email, level from members where name = ?", [name])
    member = member_cur.fetchone()
    return jsonify({"id": member['id'], "name": member['name'], "email": member['email'], })


@app.route("/member/<int:member_id>", methods=["PUT", "PATCH"])
def edit_member(member_id):
    new_member_data = request.get_json()
    name = new_member_data['name']
    email = new_member_data['email']
    db = get_db()
    db.execute('update members set name = ?, email = ? where id = ?', [name, email, member_id])
    db.commit()
    member_cur = db.execute('select * from members where id = ?', [member_id])
    member = member_cur.fetchone()
    member_dic = {"name": member['name'], 'id': member['id'], 'email': member['email']}
    return jsonify(member_dic)


@app.route("/member/<int:member_id>", methods=["DELETE"])
def delete_member(member_id):
    db = get_db()
    db.execute('delete from members where id = ?', [member_id])
    return jsonify({"message": "The member has been deleted!"})


if __name__ == "__main__":
    app.run(debug=True)
