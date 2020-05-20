import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Question, Category


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "trivia"
        self.database_path = "postgres://{}/{}".format('localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

        self.new_question = {
            "answer": "write body and header",
            "category": "Fullstack Developer",
            "difficulty": 0,
            "question": "How to HTML2?"
        }

    def tearDown(self):
        """Executed after reach test"""
        pass

    def test_get_paginated_books_valid_page(self):
        res = self.client().get('/questions?page=2')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['total_questions'] > 0)
        self.assertTrue(data['categories'])
        self.assertTrue(len(data['questions']))

    def test_get_paginated_books_invalid_page(self):
        res = self.client().get('/questions?page=10000')
        self.assertEqual(res.status_code, 404)

    def test_delete_question_valid_id(self):
        res = self.client().delete('/questions/5')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_delete_question_invalid_id(self):
        res = self.client().delete('/questions/5000')
        self.assertEqual(res.status_code, 404)

    def test_create_new_question(self):
        res = self.client().post('/questions', json=self.new_question)
        self.assertEqual(res.status_code, 200)


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
