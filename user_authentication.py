#!/usr/bin/env python

import sys
from FlaskApp.auth import User


def authenticate(username, password):

    if User.query.filter_by(username=username, password=password).first() is None:
#        print("Invalid credentials")
        return 1
    else:
#        print("User successfully logged in")
        return 0


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print "Invalid number of credentials"
    else:
        print(authenticate(str(sys.argv[1]), str(sys.argv[2])))
