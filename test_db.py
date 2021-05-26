from app import db
from app.models import User

if __name__ == '__main__':
    db.create_all()
    u = User(username='john', email='john@example.com')
    u.set_password("Pa55wort")
    print(u)
    db.session.add(u)
    db.session.commit()

    users = User.query.all()
    for u in users:
        print(u.id, u.username)