import auth

if __name__ == '__main__':
    username = raw_input("Please give username")
    password = raw_input("Please give password")
    email = raw_input("Please give email")

    user = auth.User(username, password, email)
    auth.db.session.add(user)
    auth.db.session.commit()
