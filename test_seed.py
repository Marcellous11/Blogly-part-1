from models import User, db
from app import app

# Create all tables
db.drop_all()
db.create_all()

# If table isn't empty, empty it
User.query.delete()

# Add users
Mike = User(first_name='Mike', last_name="Willson")
David = User(first_name='David', last_name="Sterling")
Billy = User(first_name='Billy', last_name="Bloobers")

# Add new objects to session, so they'll persist
db.session.add(Mike)
db.session.add(David)
db.session.add(Billy)

# Commit--otherwise, this never gets saved!
db.session.commit()