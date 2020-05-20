from models import *

QUESTIONS_PER_PAGE = 10


class CategoryAccess:
    total_number = 0

    @classmethod
    def get_all_categories(cls):
        categories = Category.query.all()
        categories = [category.format() for category in categories]
        cls.total_number = len(categories)
        return categories

    @classmethod
    def get_all_categories_as_types(cls):
        categories = cls.get_all_categories()
        types = [category['type'] for category in categories]
        return types


class QuestionsAccess:
    total_number = 0

    @classmethod
    def _paginate_questions(cls, page_number, questions):
        n = len(questions)
        start = (page_number - 1) * QUESTIONS_PER_PAGE
        end = min(start + QUESTIONS_PER_PAGE, n)
        if start >= n:
            return []
        questions = [question.format() for question in questions]
        current_questions = questions[start:end]
        return current_questions

    @classmethod
    def get_all_questions(cls):
        questions = Question.query.order_by(Question.id).all()
        cls.total_number = len(questions)
        return questions

    @classmethod
    def get_questions_page(cls, page_number):
        questions = cls.get_all_questions()
        questions_paginated = cls._paginate_questions(page_number, questions)
        return questions_paginated

    @classmethod
    def get_question(cls, question_id):
        question = Question.query.filter(Question.id == question_id).one_or_none()
        return question

    @classmethod
    def delete_question(cls, question_id):
        question = cls.get_question(question_id)
        if question is None:
            raise ValueError('Invalid question_id')
        question.delete()

    @classmethod
    def _get_attribute_from_data(cls, data, attribute_name):
        attribute = data.get(attribute_name, None)
        return attribute

    @classmethod
    def _convert_data_to_question(cls, data):
        question = cls._get_attribute_from_data(data, 'question')
        answer = cls._get_attribute_from_data(data, 'answer')
        category = cls._get_attribute_from_data(data, 'category')
        difficulty = cls._get_attribute_from_data(data, 'difficulty')
        question = Question(question, answer, category, difficulty)
        return question

    @classmethod
    def create_question(cls, data):
        try:
            question = cls._convert_data_to_question(data)
            question.insert()
        except Exception as e:
            raise ValueError(str(e))

