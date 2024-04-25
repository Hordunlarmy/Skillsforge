<picture> <source media="(prefers-color-scheme: dark)" srcset="https://i.imgur.com/8lgbDs0.png"> <source media="(prefers-color-scheme: light)" srcset="https://i.imgur.com/8lgbDs0.png"> <img alt="README image" src="https://i.imgur.com/8lgbDs0.png"> </picture>

# Blogging Platform API
This is a blogging platform API developed using FastAPI and SQLAlchemy. It supports creating, reading, updating, and deleting blog posts . Additionally, users can comment on posts, and there is functionality to search posts based on titles or content.

### Features
* **User Management**: Create, read, update, and delete users.
* **Post Management**: Create, read, update, and delete blog posts.
* **Comments Management**: Users can Create, Read, Update and Delete comments.
* **Search Functionality**: Search for posts by title or content.
* **Authentication Management**: users can signup and login

### Technology Stack
* **FastAPI**: As the web framework for building APIs.
* **SQLAlchemy**: For ORM.
* **SQLite**: As the database for local development.
* **Pydantic**: For data validation.

## Getting Started

### Prerequisites
- Python 3.8+
- pip

### Installation
- Clone the repository
```
git clone https://github.com/Hordunlarmy/Skillsforge
cd Skillsforge/section-2_blogAPI
```
- Set up a virtual environment (optional but recommended)
```
python3 -m venv venv
source venv/bin/activate  # On Windows use venv\Scripts\activate
```
### Install dependencies
`pip install -r requirements.txt`

### Environment Setup
Create a file named .env in the root directory and add environment-specific variables:
```
secret = "your_secret_key"
algorithm = HS256
token_expire = 10
database=sqlite:///./blog.db
```
### Running the Application
Start the server with:
`python3 main.py`
This command starts the application with live reloading enabled, which is useful during development.

### API Endpoints
* **GET /**: Homepage.
* **GET /posts/search/**: Search posts by title or content.
* **POST /signup/**: Create users.
* **POST /login/**: Authenticate users.
* **GET /users/**: Retrieve all users.
* **GET /posts/**: Retrieve all posts.
* **POST /posts/**: Create a new post.
* **GET /posts/{id}**: Retrieve a specific post.
* **PUT /posts/{id}**: Update a specific post.
* **DELETE /posts/{id}**: Delete a specific post.
* **POST /comments/**: Add a comment to a post.
* **GET /comments/{id}**: Retrieve a specific comment.
* **PUT /comments/{id}**: Update a specific comment.
* **DELETE /comments/{id}**: Delete a specific comment.

### Program Logic
The application is structured around MVC architecture, where:

* **Models** are defined using SQLAlchemy ORM. These models represent User, Post, and Comment.
* **Controllers** (or routes) are defined in FastAPI. Each route handles specific logic for processing requests and returning responses.
* **Views** are represented by Pydantic models which validate and serialize request and response data.

### Search Logic
The search functionality leverages the SQL LIKE statement to find matches in post titles and contents. It is case-insensitive and matches any part of the text.

### Comment Handling
Comments are linked to both users and posts through foreign keys in the database. When a comment is made, it's stored with references to both the post it belongs to and the user who made it.
