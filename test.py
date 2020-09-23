from unittest import TestCase
from app import app
from flask import session
from user import User



class FlaskTests(TestCase):

    def setUp(self):
        """Stuff to do before every test."""

    def tearDown(self):
        """Stuff to do after each test."""

    def test_homepage(self):

        """Test to confirm information is in the session and HTML is displayed"""
        with app.test_client() as client:
                resp = client.get('/')
                html = resp.get_data(as_text=True)
                self.assertEqual(resp.status_code, 200)
                self.assertIn('<h2 class="display-4 my-5">Discover Inner Peace</h2>', html)
                self.assertEqual(session.get('username'), None)

    def test_register(self):

        """Test to confirm register route and HTML is displayed"""
        with app.test_client() as client:
                resp = client.get('/register')
                html = resp.get_data(as_text=True)
                self.assertEqual(resp.status_code, 200)
                self.assertIn('<h1>Signup</h1>', html)

    def test_devotion(self):

        """Test to confirm devotion route/ HTML is displayed"""
        with app.test_client() as client:
                resp = client.get('/daily-devotion')
                html = resp.get_data(as_text=True)
                self.assertEqual(resp.status_code, 200)
                self.assertIn('<h1 class="display-4">Verse of the Day</h1>', html)
                

    def test_meditate(self):

        """Test to confirm devotion route/ HTML is displayed"""
        with app.test_client() as client:
                resp = client.get('/meditate')
                html = resp.get_data(as_text=True)
                self.assertEqual(resp.status_code, 200)
                self.assertIn('<h1>Relax and Meditate</h1>', html)

    def test_breathe(self):

        """Test to confirm devotion route/ HTML is displayed"""
        with app.test_client() as client:
                resp = client.get('/breathe')
                html = resp.get_data(as_text=True)
                self.assertEqual(resp.status_code, 200)
                self.assertIn('<h1>Breathe</h1>', html)

    def test_youtube(self):

        """Test to confirm devotion route/ HTML is displayed"""
        with app.test_client() as client:
                resp = client.get('/youtube')
                html = resp.get_data(as_text=True)
                self.assertEqual(resp.status_code, 200)
                self.assertIn('<h1 class="jumbotron-heading">Calming Music</h1>', html)