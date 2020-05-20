## Full Stack Trivia API Backend

Backend api for Q&A forms.

### Base URL

Since this API is not hosted on a specific domain, it can only be accessed when
`flask` is run locally. To make requests to the API via `curl` or `postman`,
you need to use the default domain on which the flask server is running.

**_http://127.0.0.1:5000/_**

### Endpoints


# <a name="get-questions"></a>
### 1. GET /questions

- Fetches a list of dictionaries of questions in which the keys are the ids with all available fields, a list of all categories and number of total questions.
- Request Arguments: 
    - **int** `page` (optional, 10 questions per page, defaults to `1` if not given)
- Returns: 
  1. List of dict of questions with following fields:
      - **int** `id`
      - **string** `question`
      - **string** `answer`
      - **int** `category`
      - **int** `difficulty`
  2. **list** `categories`
  3. **int** `current_category`
  4. **int** `total_questions`
  5. **boolean** `success`

#### Example
```json
{
"categories": [
    "Science",
    "Art",
    "Geography",
    "History",
    "Entertainment",
    "Sports"
  ],
"current_category": 1,
"questions": [
    {
      "answer": "Apollo 13",
      "category": 5,
      "difficulty": 4,
      "id": 2,
      "question": "What movie earned Tom Hanks his third straight Oscar nomination, in 1996?"
    },
    {
      "answer": "Tom Cruise",
      "category": 5,
      "difficulty": 4,
      "id": 4,
      "question": "What actor did author Anne Rice first denounce, then praise in the role of her beloved Lestat?"
    }
  ],
  "success": true,
  "total_questions": 24
}

```
#### Errors
If you try fetch a page which does not have any questions, you will encounter an error which looks like this:
```json
{
  "error": 404,
  "message": "resource not found",
  "success": false
}
```

### 2. POST /questions
- Searches database for questions with a search term, if provided. Otherwise,
it will insert a new question into the database.
- Request Arguments: **None**
- Request Body :
  - if you want to **search**
       1. **string** `searchTerm`
  - if you want to **insert**
       1. **string** `question`
       2. **string** `answer`
       3. **string** `category`
       4. **int** `difficulty`
- Returns: 
  - if you searched:
    1. List of dict of `questions` which match the `searchTerm` with following fields:
        - **int** `id`
        - **string** `question`
        - **string** `answer`
        - **int** `category`
        - **int** `difficulty`
    2. List of dict of ``current_category`` with following fields:
        - **int** `id`
        - **string** `type`
    3. **int** `total_questions`
    4. **boolean** `success`
  - if you inserted:
    1. List of dict of all questions with following fields:
        - **int** `id` 
        - **string** `question`
        - **string** `answer`
        - **string** `category`
        - **int** `difficulty`
    2. **int** `total_questions`
    3. **int** `created`  id from inserted question
    4. **boolean** `success`

#### Example
Search Questions
```json
{
  "current_category": [
    {
      "id": 1,
      "type": "Science"
    },
    {
      "id": 2,
      "type": "Art"
    }

  ],
  "questions": [
    {
      "answer": "Jup",
      "category": 1,
      "difficulty": 1,
      "id": 24,
      "question": "Is this a test question?"
    }
  
  ],
  "success": true,
  "total_questions": 20
}

```
Create Question
```json
{
  "created": 26,
  "questions": [
    {
      "answer": "Apollo 13",
      "category": 5,
      "difficulty": 4,
      "id": 2,
      "question": "What movie earned Tom Hanks his third straight Oscar nomination, in 1996?"
    },
    {
      "answer": "Tom Cruise",
      "category": 5,
      "difficulty": 4,
      "id": 4,
      "question": "What actor did author Anne Rice first denounce, then praise in the role of her beloved Lestat?"
    }

  ],
  "success": true,
  "total_questions": 21
}

```


#### Errors
**Search related**

If you try to search for a `question` which does not exist, it will response with an `404` error code:

```json
{
  "error": 404,
  "message": "No questions that contains \"this does not exist\" found.",
  "success": false
}
```

**Insert related**

If you try to insert a new `question`, but forget to provide a required field, it will throw an `400` error:

```json
{
  "error": 400,
  "message": "Answer can not be blank",
  "success": false
}
```

### 3. DELETE /questions/<question_id>

- Deletes specific question based on given id
- Request Arguments: 
  - **int** `question_id`
- Returns: 
    - **boolean** `success`


#### Example
```json
{
  "deleted": 10,
  "success": true
}
```

### Errors

If you try to delete a `question` which does not exist, it will throw an `400` error:

```json
{
  "error": 400,
  "message": "Question with id 7 does not exist.",
  "success": false
}
```

### 4. POST /quizzes

- Plays quiz game by providing a list of already asked questions and a category to ask for a fitting, random question.
- Request Arguments: **None**
- Request Body : 
     1. **list** `previous_questions` with **int** ids from already asked questions
     1. **dict** `quiz_category` (optional) with keys:
        1.  **string** type
        2. **int** id from category
- Returns: 
  1. Exactly one `question` as **dict** with following fields:
      - **int** `id`
      - **string** `question`
      - **string** `answer`
      - **string** `category`
      - **int** `difficulty`
  2. **boolean** `success`

#### Example
```json
{
  "question": {
    "answer": "Jup",
    "category": 1,
    "difficulty": 1,
    "id": 24,
    "question": "Is this a test question?"
  },
  "success": true
}

```
### Errors

If you try to play the quiz game without a a valid JSON body, it will response with an  `400` error.

```json
{
  "error": 400,
  "message": "Please provide a JSON body with previous question Ids and optional category.",
  "success": false
}

```
### 5. GET /categories

- Fetches a list of all `categories` with its `type` as values.
- Returns: A list of categories with its `type` as values
and a `success` value which indicates status of response. 

#### Example
```json
{
  "categories": [
    "Science",
    "Art",
    "Geography",
    "History",
    "Entertainment",
    "Sports"
  ],
  "success": true
}
```
### Errors

Endpoint does not raise any specific errors.

### 6. GET /categories/<category_id>/questions

- Fetches all `questions` (paginated) from one specific category.
- Request Arguments:
  - **int** `category_id`
  - **int** `page`
- Returns: 
  1. **int** `current_category` id from inputted category
  2. List of dict of all questions with following fields:
     - **int** `id` 
     - **string** `question`
     - **string** `answer`
     - **string** `category`
     - **int** `difficulty`
  3. **int** `total_questions`
  4. **boolean** `success`

#### Example response

```json
{
  "current_category": "2",
  "questions": [
    {
      "answer": "Escher",
      "category": 2,
      "difficulty": 1,
      "id": 16,
      "question": "Which Dutch graphic artist\u2013initials M C was a creator of optical illusions?"
    },
    {
      "answer": "Mona Lisa",
      "category": 2,
      "difficulty": 3,
      "id": 17,
      "question": "La Giaconda is better known as what?"
    },
    {
      "answer": "One",
      "category": 2,
      "difficulty": 4,
      "id": 18,
      "question": "How many paintings did Van Gogh sell in his lifetime?"
    },
    {
      "answer": "Jackson Pollock",
      "category": 2,
      "difficulty": 2,
      "id": 19,
      "question": "Which American artist was a pioneer of Abstract Expressionism, and a leading exponent of action painting?"
    }
  ],
  "success": true,
  "total_questions": 4
}
```

### Errors
This endpoint can yield 2 common errors. For example, if you ask for questions of a category that does not exist it will throw an `400` error:

```json
{
  "error": 400,
  "message": "No questions with category 10 found.",
  "success": false
}
```
Additionally, if you query for a category which has questions, but not on the selected `page`, it will raise an `404` error:

```json
{
  "error": 404,
  "message": "No questions in selected page.",
  "success": false
}

```