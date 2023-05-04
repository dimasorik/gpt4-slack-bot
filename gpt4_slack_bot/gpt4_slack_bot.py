import slack
import logging
import os
from flask import Flask
from slackeventsapi import SlackEventAdapter
import openai

from gpt4_slack_bot.openai_constants import GPT_4_MODEL, ROLE_FILED_NAME, CONTENT_FIELD_NAME, ROLE_USER, ROLE_ASSISTANT, \
    OPENAI_TOKEN_NAME

slack_signing_secret = os.environ["SLACK_SIGNING_SECRET"]
slack_token = os.environ["SLACK_TOKEN"]
openai_token = os.environ[OPENAI_TOKEN_NAME]

model = os.environ.get("GPT_MODEL", GPT_4_MODEL)

logging.basicConfig(level=logging.DEBUG)

app = Flask(__name__)

slack_event_adapter = SlackEventAdapter(slack_signing_secret, '/slack/events', app)

client = slack.WebClient(token=slack_token)

openai.api_key = openai_token

chat_map = {}  # Should be Redis or some other key-value storage


@slack_event_adapter.on('app_mention')
def message(payload):
    logging.debug('app mention')

    process_message(payload)


@slack_event_adapter.on('message')
def message(payload):
    logging.debug('private message')

    process_message(payload)


def process_message(payload):
    event = payload.get('event', {})
    channel_id = event.get('channel')
    user_id = event.get('user')
    text = event.get('text')

    chat_id = create_dialog_key(channel_id, user_id)

    reset_history_if_required(chat_id, channel_id)
    client.chat_postMessage(channel=channel_id, text="Generating response from GPT")

    append_chat(chat_id, text, ROLE_USER)

    chat_messages = chat_map.get(chat_id)
    gpt4_response_text = generate_gpt_response(chat_messages)

    append_chat(chat_id, gpt4_response_text, ROLE_ASSISTANT)

    client.chat_postMessage(channel=channel_id, text=gpt4_response_text)


def create_dialog_key(channel_id, user_id):
    return channel_id + user_id


def reset_history_if_required(chat_id, channel_id):
    chat_messages = chat_map.get(chat_id, [])
    if len(chat_messages) >= 10:
        client.chat_postMessage(channel=channel_id, text="Resting history with GPT")
        chat_map[chat_id] = []


def append_chat(chat_id, content, role):
    chat_messages = chat_map.get(chat_id, [])
    chat_messages.append({ROLE_FILED_NAME: role, CONTENT_FIELD_NAME: content})
    chat_map[chat_id] = chat_messages
    return chat_messages


def clear_history(chat_id):
    logging.debug("resetting chat")
    chat_messages = chat_map.get(chat_id, [])
    chat_messages.clear()
    chat_map[chat_id] = chat_messages
    return chat_messages


def generate_gpt_response(chat_messages):
    completion = openai.ChatCompletion.create(model=model, messages=chat_messages)
    return completion.choices[0].message[CONTENT_FIELD_NAME]


if __name__ == "__main__":
    app.run(debug=True)
