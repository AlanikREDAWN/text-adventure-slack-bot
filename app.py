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

global tutorial_player_location
tutorial_player_location = tutorialstory['rooms']['great_hall']

@app.command("/startadventure")
def start_adventure(ack, respond, command, client, say):

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
        client.chat_postMessage(channel=user_id, text="test", blocks=blocks)
        
    except Exception as e:
        response_message = f"Error sending DM: {e}"
        # print(f"Error sending DM: {e}")
        # respond("Sorry, I couldn't send you a direct message.")
        # say(f"Error sending DM: {e}")
        respond(response_message)

    # respond(f"Rooms: {tutorialstory['rooms']}")
    # respond(f"it works")

@app.command("/go")
def go(ack, respond, command, client, say):
    ack()
    user_text = command.get("text", "").strip().lower()
    # user_text = command["text"]
    user_id = command["user_id"]

    if not user_text:
        respond("Please provide a direction to travel, such as `/go north`.")
        return
    elif "ping" in user_text:
        respond("pong!")
    elif "north" in user_text:
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
            if tutorial_player_location == tutorialstory['rooms']['great_hall']:
                tutorial_player_location = tutorialstory['rooms']['hallway']
                
            
                client.chat_postMessage(channel=user_id, text="test", blocks=blocks)
                # client.chat_postMessage(blocks)
            else:
                respond("You cannot move north")

        except Exception as e:
                response_message = f"Error sending DM: {e}"

                # print(f"Error sending DM: {e}")
                # respond("Sorry, I couldn't send you a direct message.")
                # respond(response_message)
                # say(f"Error sending DM: {e}")
                respond(f"{command['text']}")


if __name__ == "__main__":
    SocketModeHandler(app, SLACK_APP_TOKEN).start()