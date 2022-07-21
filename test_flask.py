from unittest import TestCase
from app import app
from models import db, User 


app.config['SQLALCHEMY_DATABASE_URL'] = 'postgresql:///user_db'
app.config['SQALCHEMY_ECHO']= False

app.config['TESTING'] = True

app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-tolobar']

class UserTestCase(TestCase):

    def setUp(self):
        User.query.delete()

        user = User(first_name='Marcellous',last_name='Curtis',image_url='https://plantbiology.ucr.edu/sites/default/files/styles/form_preview/public/blank-profile-pic.png?itok=rhVwP3MG')
        db.session.add(user)
        db.session.commit()
        self.user_id = user.id

    def tearDown(self):
        db.session.rollback()
    
    def test_user_list(self):
        with app.test_client() as client:
            resp = client.get('/')
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code,200)

    def test_user_list(self):
        with app.test_client() as client:
            resp = client.get('/4')

            self.assertEqual(resp.status_code,200)

    def test_user_list(self):
        with app.test_client() as client:
            resp = client.get('/user')

            self.assertEqual(resp.status_code,200)

    def test_user_list(self):
        with app.test_client() as client:
            resp = client.get('/user/add')

            self.assertEqual(resp.status_code,200)
