# Slack bot to connect with openAI GPT model
Slack Bot that is using AI GPT-4 version from the [OpenAI](https://openai.com/) company.
The bot is reacting on the private messages and on the mentions in the group channel

In order to use it - you will 2 things:
1. Create slack bot. Details [here](https://api.slack.com/tutorials/tracks/create-bot-to-welcome-users)
2. Get GPT-4 API token from OpenAI. Details [here](https://help.openai.com/en/articles/7102672-how-can-i-access-gpt-4).

## Developer's instructions
This project is using [python-poetry](https://python-poetry.org/) as a PYTHON PACKAGING AND DEPENDENCY MANAGEMENT.
### Prerequisites
1. Python >= 3.11 version
2. [Poetry](https://python-poetry.org/) >= 1.4.0 version
### Running project locally
1. Checkout && cd to the project's folder
2. Install dependencies `poetry install`
3. Export env variables `export SLACK_TOKEN=token && export SLACK_SIGNING_SECRET=token && export OPENAI_TOKEN=toen`
4. Run `poetry run python gpt4_slack_bot/gpt4_slack_bot.py`
5. Run [ngrok](https://ngrok.com/) server to make your env available for the slack events `ngrok http 5000`
### Building and running docker image
1. Set the tokens inside `docker-compose.yaml`
2. Run docker-compose `docker-compose up`

## Functionality
The current features of the bot:
1. Pass the complete text chat to the OpenAI's GPT-4  and forwarding reply to it

### Bot commands

