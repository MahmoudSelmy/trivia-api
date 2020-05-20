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
- Request : http://127.0.0.1:5000/questions?page=1
- Response : [get_all_questions.json](./outputs/get_all_questions.json)

### Errors

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
       3. **int** `category`
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
        - **int** `category`
        - **int** `difficulty`
    2. **int** `total_questions`
    3. **int** `created`  id from inserted question
    4. **boolean** `success`

#### Example
- Search Questions
  - Request : 
    - URL: http://127.0.0.1:5000/questions
    - Body: {"searchTerm": "How"}
  - Response: [search_questions.json](./outputs/search_questions.json)
- Create Question
  - Request : 
    - URL: http://127.0.0.1:5000/questions
    - Body: 
        ```json
        {
            "answer": "write body and header",
            "category": 1,
            "difficulty": 0,
            "question": "How to HTML2?"
        }
        ```
  - Response: [create_new_question.json](./outputs/create_new_question.json)

#### Errors
**Search related**

If you try to search for a `question` which does not exist, it will response with an `404` error code:

```json
{
    "error": 404,
    "message": "resource not found",
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
- Request : http://127.0.0.1:5000/questions/10
- Response : [delete_question.json](./outputs/delete_question.json)

### Errors

If you try to delete a `question` which does not exist, it will throw an `400` error:

```json
{
    "error": 422,
    "message": "un_processable",
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
      - **int** `category`
      - **int** `difficulty`
  2. **boolean** `success`

#### Example
- Request : http://127.0.0.1:5000/quizzes
- Response : [get_quiz_question.json](./outputs/get_quiz_question.json)

### Errors
This endpoint has one common error:
- Not found 404 : their no question that meet the selection criteria

### 5. GET /categories

- Fetches a list of all `categories` with its `type` as values.
- Returns: A list of categories with its `type` as values
and a `success` value which indicates status of response. 

#### Example
- Request : http://127.0.0.1:5000/categories
- Response : [get_all_categories.json](./outputs/get_all_categories.json)


### 6. GET /categories/<category_id>/questions

- Fetches all `questions` from one specific category.
- Request Arguments:
  - **int** `category_id`
  - **int** `page`
- Returns: 
  1. **int** `current_category` id from inputted category
  2. List of dict of all questions with following fields:
     - **int** `id` 
     - **string** `question`
     - **string** `answer`
     - **int** `category`
     - **int** `difficulty`
  3. **int** `total_questions`
  4. **boolean** `success`

#### Example
- Request : http://127.0.0.1:5000/categories/1/questions
- Response : [get_category_questions.json](./outputs/get_category_questions.json)

### Errors
This endpoint can yield 2 common errors:
- Bad request 400 : Invalid body
- Not found 404 : their no question that meet the selection criteria