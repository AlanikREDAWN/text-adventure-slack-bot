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

tutorial_player_location = tutorialstory['rooms']['great_hall']

@app.command("/startadventure")
def start_adventure(ack, respond, command, client):

    ack()
    user_id = command["user_id"]
    message = f"Rooms: {tutorialstory['rooms']}"
    blocks = [
		{
			"type": "header",
			"text": {
				"type": "plain_text",
				"text": tutorial_player_location['name'],
			}
		},
		{
			"type": "rich_text",
			"elements": [
				{
					"type": "rich_text_section",
					"elements": [
						{
							"type": "text",
							"text": tutorial_player_location['description'],
							"style": {
								"italic": True
							}
						}
					]
				}
			]
		}
	]

    try:
        # client.chat_postMessage(channel=user_id, text=message)
        client.chat_postMessage(channel=user_id, text=blocks)
        
    except Exception as e:
        print(f"Error sending DM: {e}")
        respond("Sorry, I couldn't send you a direct message.")

    # respond(f"Rooms: {tutorialstory['rooms']}")
    # respond(f"it works")

@app.command("/go north")
def go_north(ack, respond, command, client):
    ack()
    user_id = command["user_id"]

    if tutorial_player_location == tutorialstory['rooms']['great_hall']:
        tutorial_player_location = tutorialstory['rooms']['hallway']
        blocks = [
            {
                "type": "header",
                "text": {
                    "type": "plain_text",
                    "text": tutorial_player_location['name'],
                }
            },
            {
                "type": "rich_text",
                "elements": [
                    {
                        "type": "rich_text_section",
                        "elements": [
                            {
                                "type": "text",
                                "text": tutorial_player_location['description'],
                                "style": {
                                    "italic": True
                                }
                            }
                        ]
                    }
                ]
            }
        ]
        try:
            client.chat_postMessage(channel=user_id, text=blocks)
            client.chat_postMessage(blocks)
        
        except Exception as e:
            print(f"Error sending DM: {e}")
            respond("Sorry, I couldn't send you a direct message.")
    else:
        pass

# Start your app
if __name__ == "__main__":
    SocketModeHandler(app, SLACK_APP_TOKEN).start()