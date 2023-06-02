# IdeaGenie

This is a Flask-based blog application that allows users to create, read, update, and delete blog posts. Users can register an account, log in, and perform various actions related to managing their blog posts. The application also includes features like commenting, user profiles, and basic search functionality.
#### Video Demo:  https://www.youtube.com/watch?v=m-PJogGYK2s&ab_channel=VincentGuzman
## Installation:

1. Clone the repository:
    ``` commandline   
    git clone git@github.com:vguzman812/blog_repo.git
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
     ```commandline
      touch .env
      open .env
     ```
   - Define the required environment variables in the `.env` file. 
     - SECRET_KEY=<your_secret_key>
     - DATABASE_URL=<your_database_url>
     - MAIL_SERVER=<your_mail_server>
     - MAIL_PORT=<your_mail_port>
     - MAIL_USERNAME=<your_mail_username>
     - MAIL_PASSWORD=<your_mail_password>

7. Initialize the database:
   ```commandline
   flask db init
   ```

8. Apply database migrations:
   ```commandline
   flask db migrate -m "initial migration"
   flask db upgrade
   ```
9. Run the application:
    ```commandline
    flask run
    ```
The application should now be running locally on http://localhost:5000.



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