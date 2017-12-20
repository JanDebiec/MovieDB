from pytest import fixture, mark
import sys
sys.path.extend(['/home/jan/project/movie_db'])
from app import create_app, db

from config import Config

class TestConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite://'

class TestAppDb:
    def setup(self):
        print("setup method, class: TestAppDb, fixture test method")
        self.app = create_app(TestConfig)
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def teardown(self):
        print("teardown method class: TestAppDb")
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def setup_class(self):
        print("\nsetup class      class: %s, fixture test class" % self.__name__)

    def teardown_class(self):
        print("teardown class      class: %s" % self.__name__)

    def test_1(self):
        value = 2
        assert 2 == value