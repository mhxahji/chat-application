# chat-application
Simple browser-based chat application using Python.

This project uses: Python 3.7, django 3.0.3 and django channels with Redis as message broker.

## Installation

1. Clone this repository: `git clone https://github.com/mhxahji/chat-application.git`.
2. Create a Virtual Environment with Python 3 and activate it
3. `cd` into `chat-application`.
4. Install all requirements with `pip install -r requirements.txt`.
5. Migrate database with `python manage.py migrate` (Configured for using SQLite).
6. Install and execute Redis Server.
7. Run the project with `python manage.py runserver`.

## Usage
1. Enter the site localhost:8000
2. Create an account in the link of "create new account"
3. Create rooms and chat

## For using in other devices (connected to the local network)
1. Add your local IP in ALLOWED_HOSTS in settings.py (line 28)
2. Run `python manage.py runserver 0.0.0.0:8000`
3. Open the browser in other devices (connected to the local network) and go to: `your.local.ip:8000`

## For testing
Run `python manage.py test --noinput`

## The project implement both bonus:
- Have more than one room. Users can create rooms and enter to different rooms to chat.
- Handle messages that are not understood or any exceptions raised within the bot.
  Messages beginning with `/` are considered commands. If the message has no a correct format
  (`/stock=command`), an error message is sent only to the user that tried to post the incorrect
  command. This error message is not saved in database. Also when the command has a N/D response
  from API, is shown a error message only to the user that send the command