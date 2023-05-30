# IdeaGenie

This is a Flask-based blog application that allows users to create, read, update, and delete blog posts. Users can register an account, log in, and perform various actions related to managing their blog posts. The application also includes features like commenting, user profiles, and basic search functionality.

## Installation:

1. Clone the repository:
    ``` commandline   
    git clone <repository_url>
    ```
2. Navigate to the project directory:
    ```   commandline
    cd blog_repo
    ```
3. Install Pipenv:
   ```commandline
   pip install pipenv
   ```

4. Create a virtual environment and install dependencies:
   ```commandline
   pipenv install --dev
   ```

5. Activate the virtual environment:
   ```commandline
   pipenv shell
   ```

6. Set up the environment variables:
   - Create a `.env` file in the project root directory.
   - Define the required environment variables in the `.env` file.

7. Initialize the database:
   ```commandline
   flask db init
   ```

8. Apply database migrations:
   ```commandline
   flask db migrate
   flask db upgrade
   ```

9. Compile the static assets:
   ```commandline
   flask compile-assets
   ```

10. Run the application:
    ```commandline
    gunicorn wsgi:app
    ```

## Usage:
- Register a new account with your email and password.
- Log in to access your dashboard.
- Create, edit, and delete your blog posts.
- Browse and search for posts created by other users.
- Leave comments on blog posts.
- Follow and unfollow other users to see their posts on your dashboard.

## Contributing:
Contributions to the project are welcome! If you find any issues or want to add new features, please open an issue or submit a pull request.

## License:
This project is licensed under the MIT License.