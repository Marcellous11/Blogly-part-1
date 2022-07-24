"""Seed file to make sample data for pets db."""

from models import User, db, Post
from app import app

# Create all tables
db.drop_all()
db.create_all()

# If table isn't empty, empty it
User.query.delete()

# Add users
Mike = User(first_name="Mike", last_name="Willson")
David = User(first_name="David", last_name="Sterling")
Billy = User(first_name="Billy", last_name="Bloobers")
Chloe = User(first_name="Chole", last_name="jeffrerson")
Mitchelle = User(first_name="Mitchelle", last_name="Bukes")
Sara = User(first_name="Sara", last_name="Red")

mike_post = Post(title="Crazy weekend ", content="Wish i had some time to tell my story", users_id=3)
David_post = Post(title="This are heating up ", content="The girl i have a crush on is so into me", users_id=3)
billy_post = Post(title="Time doesn't stop", content="Ive walked the earth for 1,000 years", users_id=2)
chloe_post = Post(title="The God king", content="King leto has aked me to help him with a mission", users_id=1)
mitchelle_post = Post(title="Struggles ", content="I wish i knew how to help my boyfriend, hes just so sad", users_id=5)
sara_post = Post(title="Time Machine", content="I literally just stumbled uppon it, now im the future?", users_id=4)
billy_post = Post(title="The Mavs are up ", content="I've been waiting for this basketball game all week.", users_id=5)

# Add new objects to session, so they'll persist
db.session.add(Sara)
db.session.add(Mitchelle)
db.session.add(Chloe)
db.session.add(Billy)
db.session.add(David)
db.session.add(Mike)


# Commit--otherwise, this never gets saved!
db.session.commit()

db.session.add(sara_post)
db.session.add(billy_post)
db.session.add(mitchelle_post)
db.session.add(chloe_post)
db.session.add(billy_post)
db.session.add(David_post)
db.session.add(mike_post)

db.session.commit()

post = Post(title="rREALLY",content="DOES IT WORK", users_id=6)
db.session.add(post)
db.session.commit()