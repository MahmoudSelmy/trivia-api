import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random
from database_access import CategoryAccess, QuestionsAccess

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)

    cors = CORS(app, resources={r"/api/*": {"origins": "*"}})

    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization,true')
        response.headers.add('Access-Control-Allow-Methods', 'GET,PATCH,POST,DELETE,OPTIONS')
        return response

    @app.route('/categories')
    def get_all_categories():
        categories = CategoryAccess.get_all_categories()
        if len(categories) == 0:
            abort(404)

        return jsonify({
            'success': True,
            'categories': categories,
            'total_categories': len(categories)
        })

    @app.route('/questions')
    def get_questions_page():
        page_number = request.args.get('page', 1, type=int)
        questions = QuestionsAccess.get_questions_page(page_number)

        categories = CategoryAccess.get_all_categories_as_types()

        if len(questions) == 0:
            abort(404)

        return jsonify({
            'success': True,
            'total_questions': QuestionsAccess.get_total_number(),
            'questions': questions,
            'categories': categories,
            'current_category': questions[0]['category']
        })

    @app.route('/questions/<int:question_id>', methods=['DELETE'])
    def delete_question(question_id):
        try:
            QuestionsAccess.delete_question(question_id)
            return jsonify({
                'success': True
            })
        except Exception as e:
            print(e)
            abort(422)

    @app.route('/questions', methods=['POST'])
    def create_or_search_question():
        body = request.get_json()
        try:
            search_term = body.get('searchTerm', None)
            if search_term is None:
                QuestionsAccess.create_question(body)
                return jsonify({
                    'success': True
                })
            else:
                questions = QuestionsAccess.search_questions(search_term)
                return jsonify({
                    'success': True,
                    'questions': questions,
                    'total_questions': QuestionsAccess.get_total_number(),
                    'current_category': questions[0]['category']
                })

        except Exception as e:
            print(e)
            abort(422)

    '''
    @TODO: 
    Create a GET endpoint to get questions based on category. 

    TEST: In the "List" tab / main screen, clicking on one of the 
    categories in the left column will cause only questions of that 
    category to be shown. 
    '''

    @app.route('/categories/<int:category_id>/questions', methods=['GET'])
    def get_questions_from_categories(category_id):
        try:
            page_number = request.args.get('page', 1, type=int)
            questions = QuestionsAccess.get_all_category_questions(category_id, page_number)

            if len(questions) == 0:
                abort(404)

            return jsonify({
                'success': True,
                'questions': questions,
                'total_questions': QuestionsAccess.get_total_number(),
                'current_category': category_id
            })
        except Exception as e:
            print(e)
            abort(422)

    '''
    @TODO: 
    Create a POST endpoint to get questions to play the quiz. 
    This endpoint should take category and previous question parameters 
    and return a random questions within the given category, 
    if provided, and that is not one of the previous questions. 

    TEST: In the "Play" tab, after a user selects "All" or a category,
    one question at a time is displayed, the user is allowed to answer
    and shown whether they were correct or not. 
    '''

    '''
    @TODO: 
    Create error handlers for all expected errors 
    including 404 and 422. 
    '''

    return app


if __name__ == '__main__':
    app = create_app()
    app.run()
