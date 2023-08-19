# IdeaGenie

This is a full stack Flask-based application with CRUD operations for user accounts, posts, and comments. It includes authentication via email and JWT, custom profiles, and search functionality via Whooshee.

#### Video Demo:  https://www.youtube.com/watch?v=m-PJogGYK2s&ab_channel=VincentGuzman

## Optimizations
Changing from SQLite to PostgreSQL allowed more robust and scalable database architecture.
Improving the search functionality and parameters of what is searched could definitely be improved upon. 
The front end is a bit vanilla, so adding some JS animations and transitions is definitely something I wanted to do.
I wanted to add in liking posts and favoriting posts as well. It is something I look forward to implementing in the future.
Changing from JWT and email verification to Auth0 and MFA is another improvement that needs to be made for better security and privacy concerns.

## Lessons Learned:

Where to start. This was made before ChatGPT was publicly accessible. This was my first full stack application, and it had me use all of my resourcefulness. Nearly every feature was new to me. I had a poor grasp of html and css at the time, so I Bootstrapped my way through a lot of this application. Figuring out how to make infinite scrolling, creating a responsive navbar, implementing dark and light themes based on local user OS preference and saving user preference in local storage. All of that was new to me. All of it required effort and time to implement and implement correctly. Figuring out how to secure passwords and email in my database with cryptography, using JWT to verify emails, and establishing many-to-many relationships in my database were all huge hurdles that I needed to figure out. Let's not even get into the changes needed for deploying to production initially.

Overall, this project tested the limits of my resourcefulness and ability to persevere. I learned so many things that I had taken for granted before. This project was a huge boost in my confidence and knowledge about how to read through documentation, and find solutions to problems I had.

## Local Installation:

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
The application should now be running locally on http://localhost:5000 or whichever port you have decided to use.



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

## Other Projects:
Take a look at these other projects that I have in my portfolio:

**CocktailDB:** https://github.com/vguzman812/CocktailDB

**Javi Sol:** https://github.com/vguzman812/javiSol

**Tranquil Tomato:** https://github.com/vguzman812/tranquilTomato

