import auth


def add_user(username, password, email, admin_rights):
    user = auth.User(username, password, email, admin_rights)
    auth.db.session.add(user)
    auth.db.session.commit()


if __name__ == '__main__':
    username = raw_input("Please give username: ")
    password = raw_input("Please give password: ")
    email = raw_input("Please give email: ")

    user = auth.User(username, password, email, False)
    auth.db.session.add(user)
    auth.db.session.commit()
