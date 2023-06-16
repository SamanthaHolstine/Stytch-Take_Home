from flask import Flask, render_template
from stytch import Client
import re


app = Flask(__name__)

#display all users when starting app
@app.route('/')
def main():
    resp = get_all_users()
    users = resp.split("User")

    users_filtered = filterResponse(users)

    return render_template('index.html', users=users_filtered)

#function to call POST API to get all Users
def get_all_users():
    client = Client(
        project_id="project-test-6129c9f7-90f5-4e53-a579-37e37f468dbb",
        secret="secret-test-j0r2MujiFTWND79xVwOb_ZCp6JaXQZhnv5A=",
        environment="test",
    )

    return str(client.users.search())
#function to filter out response from API call to just first name
#   last name, user_id, and email
def filterResponse(users):
    users_filtered = []
    users.pop(0)
    for u in users:
        user = []
        # first name
        user.append(re.search('first_name=\'(.*)\', middle_name', u).group(1))

        # last name
        lastname = re.search('last_name=\'(.*), user_id', u).group(1).translate({ord(i): None for i in '\')'})
        user.append(lastname)

        # user id
        user.append(re.search('user_id=\'(.*)\', trusted_me', u).group(1))

        # email
        user.append(re.search('email=\'(.*)\', verified', u).group(1))

        users_filtered.append(user)

    return users_filtered

#function to call DELETE API call and show new table with remaining users
@app.route('/delete_user/<user_id>', methods=["POST"])
def deleteuser(user_id):
    client = Client(
        project_id="project-test-6129c9f7-90f5-4e53-a579-37e37f468dbb",
        secret="secret-test-j0r2MujiFTWND79xVwOb_ZCp6JaXQZhnv5A=",
        environment="test",
    )

    resp = client.users.delete(user_id=user_id)

    users = get_all_users().split("User")
    new_users_list = filterResponse(users)
    print(new_users_list)
    return render_template('index.html', users=new_users_list)
