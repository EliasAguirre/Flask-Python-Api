from main import db
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(10), index=True, unique=True)
    age = db.Column(db.Integer, index=True, unique=True)

    def __repr__(self):
        return '<User {}>'.format(self.name)  

def init_db():
    db.create_all()

    # Create a test user
    new_user = User('ad', 2)
    db.session.add(new_user)
    db.session.commit()


if __name__ == '__main__':
    init_db()