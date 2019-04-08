Chumchonmusic
======
**Install Flask** ::

  pip install Flask

**Clone the repository** ::

  git clone https://github.com/Sataapon/Chumchonmusic.git
  cd Chumchonmusic

**Run The Application**

For Linux and Mac: ::

  export FLASK_APP=flasks
  export FLASK_ENV=development
  flask run

For Windows cmd, use set instead of export: ::

  set FLASK_APP=flasks
  set FLASK_ENV=development
  flask run

For Windows PowerShell, use $env: instead of export: ::

  $env:FLASK_APP = "flasks"
  $env:FLASK_ENV = "development"
  flask run

You’ll see output similar to this: ::

  * Serving Flask app "flaskr"
  * Environment: development
  * Debug mode: on
  * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
  * Restarting with stat
  * Debugger is active!
  * Debugger PIN: 855-212-761
  
Initialize the Database File: ::

  flask init-db
