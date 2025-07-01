import os
import yaml
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
from dotenv import load_dotenv
load_dotenv()

SLACK_BOT_TOKEN = os.getenv("SLACK_BOT_TOKEN")
SLACK_APP_TOKEN = os.getenv("SLACK_APP_TOKEN")


app = App(token=SLACK_BOT_TOKEN)

with open('./stories/tutorial-story.yaml', 'r') as file:
    tutorialstory = yaml.safe_load(file)


@app.command("/startadventure")
def repeat_text(ack, respond, command, client):

    ack()
    user_id = command["user_id"]
    message = f"Rooms: {tutorialstory['rooms']}"

    try:
        client.chat_postMessage(channel=user_id, text=message)
    except Exception as e:
        print(f"Error sending DM: {e}")
        respond("Sorry, I couldn't send you a direct message.")

    # respond(f"Rooms: {tutorialstory['rooms']}")
    # respond(f"it works")
    

# Start your app
if __name__ == "__main__":
    SocketModeHandler(app, SLACK_APP_TOKEN).start()