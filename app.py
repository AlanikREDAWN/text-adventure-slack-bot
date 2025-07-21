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
# tutorial_player_location = tutorialstory['rooms']['great_hall']

@app.command("/startadventure")
def start_adventure(ack, respond, command, client, say):

    ack()

    tutorial_player_location = tutorialstory['rooms']['great_hall']
    current_room = tutorial_player_location
    # current_room = tutorial_player_location
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
def go(ack, respond, command, client, say, body, logger):
    ack()
    logger.info(body)
    global tutorial_player_location

    
    user_text = command.get("text", "").strip().lower()
    # user_text = command["text"]
    user_id = command["user_id"]

    if tutorial_player_location is None:
        respond("You need to start the adventure first using `/startadventure`.")
        return

    current_room = tutorial_player_location

    # blocks = [
    #     {
    #         "type": "header",
    #         "text": {
    #             "type": "plain_text",
    #             "text": tutorial_player_location['name'],
    #         }
    #     },
    #     {
    #         "type": "rich_text",
    #         "elements": [
    #             {
    #                 "type": "rich_text_section",
    #                 "elements": [
    #                     {
    #                         "type": "text",
    #                         "text": tutorial_player_location['description'],
    #                         "style": {
    #                             "italic": True
    #                         }
    #                     }
    #                 ]
    #             }
    #         ]
    #     }
    # ]

    def send_room(loc):
        blocks = [
            {
                "type": "header",
                "text": {
                    "type": "plain_text",
                    "text": loc['name'],
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
                                "text": loc['description'],
                                "style": {
                                    "italic": True
                                }
                            }
                        ]
                    }
                ]
            }
        ]
        client.chat_postMessage(channel=user_id, text="You moved!", blocks=blocks)
    

    # if not user_text:
    #     respond("Please provide a direction to travel, such as `/go north`.")
    #     return
    if "ping" in user_text:
        respond("pong!")
    elif "north" in user_text:
        # respond("test")
        try:
            if current_room == tutorialstory['rooms']['great_hall']:
                tutorial_player_location == tutorialstory['rooms']['hallway']

                send_room(tutorial_player_location)
            else:
                respond("You can't go north from here!")
            # if tutorial_player_location == tutorialstory['rooms']['great_hall']:
            #     tutorial_player_location = tutorialstory['rooms']['hallway']
                
            
            #     client.chat_postMessage(channel=user_id, text="test", blocks=blocks)
            #     # client.chat_postMessage(blocks)
            # else:
            #     respond("You cannot move north")

        except Exception as e:
            response_message = f"Error sending DM: {e}"

            # respond(response_message)

            print(f"Error sending DM: {e}")
            respond("Sorry, I couldn't send you a direct message.")
            
            # say(f"Error sending DM: {e}")
            # respond(f"{command['text']}")
    elif "south" in user_text:
        try:
            if current_room == tutorialstory['rooms']['hallway']:
                tutorial_player_location = tutorialstory['rooms']['great_hall']
                send_room(tutorial_player_location)
            else:
                respond("You can't go south from here!")
            # if tutorial_player_location == tutorialstory['rooms']['hallway']:
            #     tutorial_player_location = tutorialstory['rooms']['great_hall']

            #     client.chat_postMessage(channel=user_id, text="test", blocks=blocks)
            # else:
            #     # respond("You cannot move south")
            #     client.chat_postMessage(channel=user_id, text="You cannot move south")
        except Exception as e:
            response_message = f"Error sending DM: {e}"

            # respond(response_message)

            print(f"Error sending DM: {e}")
            respond("Sorry, I couldn't send you a direct message.")
    elif "east" in user_text:
        try:
            if current_room == tutorialstory['rooms']['hallway']:
                tutorial_player_location = tutorialstory['rooms']['training_room']
                send_room(tutorial_player_location)
            elif current_room == tutorialstory['rooms']['ballroom']:
                tutorial_player_location = tutorialstory['rooms']['hallway']
                send_room(tutorial_player_location)
            else:
                respond("You can't go east from here!")

            # if tutorial_player_location == tutorialstory['rooms']['hallway']:
            #     tutorial_player_location = tutorialstory['rooms']['training_room']

            #     client.chat_postMessage(channel=user_id, text="test", blocks=blocks)
    
            # elif tutorial_player_location == tutorialstory['rooms']['ballroom']:
            #     tutorial_player_location = tutorialstory['rooms']['hallway']

            #     client.chat_postMessage(channel=user_id, text="test", blocks=blocks)
            # else:
            #     client.chat_postMessage(channel=user_id, text="You cannot move east")

        except Exception as e:
            response_message = f"Error sending DM: {e}"

            # respond(response_message)

            print(f"Error sending DM: {e}")
            respond("Sorry, I couldn't send you a direct message.")
    elif "west" in user_text:
        try:
            if current_room == tutorialstory['rooms']['hallway']:
                tutorial_player_location = tutorialstory['rooms']['ballroom']
                send_room(tutorial_player_location)
            elif current_room == tutorialstory['rooms']['training_room']:
                tutorial_player_location = tutorialstory['rooms']['hallway']
                send_room(tutorial_player_location)
            else:
                respond("You can't go west from here!")
            # if tutorial_player_location == tutorialstory['rooms']['hallway']:
            #     tutorial_player_location = tutorialstory['rooms']['ballroom']

            #     client.chat_postMessage(channel=user_id, text="test", blocks=blocks)

            # elif tutorial_player_location == tutorialstory['rooms']['training_room']:
            #     tutorial_player_location = tutorialstory['rooms']['hallway']

            #     client.chat_postMessage(channel=user_id, text="test", blocks="blocks")
            # else:
            #     client.chat_postMessage(channel=user_id, text="You cannot move west")
        except Exception as e:
            response_message = f"Error sending DM: {e}"

            # respond(response_message)

            print(f"Error sending DM: {e}")
            respond("Sorry, I couldn't send you a direct message.")
    else:
        respond("Please provide a direction to travel, such as `/go north`.")

        


if __name__ == "__main__":
    SocketModeHandler(app, SLACK_APP_TOKEN).start()