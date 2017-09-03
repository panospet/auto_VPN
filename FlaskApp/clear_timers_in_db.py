import auth

users = auth.User.query.all()
for user in users:
    user.timer_name = None
auth.db.session.commit()
