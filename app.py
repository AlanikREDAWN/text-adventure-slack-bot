import os
import yaml
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
from dotenv import load_dotenv
import threading
from flask import Flask
flask_app = Flask(__name__)
import logging
logging.basicConfig(level=logging.INFO)
# load_dotenv()

SLACK_BOT_TOKEN = os.getenv("SLACK_BOT_TOKEN")
SLACK_APP_TOKEN = os.getenv("SLACK_APP_TOKEN")


app = App(token=SLACK_BOT_TOKEN)


with open('./stories/tutorial-story.yaml', 'r') as file:
    tutorialstory = yaml.safe_load(file)



global tutorial_player_location
tutorial_player_location = None
user_locations = {}
current_adventure = None

# tutorial_player_location = tutorialstory['rooms']['great_hall']

@flask_app.route("/")
def home():
    return "Slack bot running!"

def run_flask():
    port = int(os.environ.get("PORT", 3000))
    flask_app.run(host="0.0.0.0", port=port)

@app.command("/startadventure")
def start_adventure(ack, respond, command, client, say):
    ack()
    user_id = command["user_id"]

    startBlocks = [
		{
			"type": "rich_text",
			"elements": [
				{
					"type": "rich_text_section",
					"elements": [
						{
							"type": "text",
							"text": "Welcome! What adventure would you like to start?"
						}
					]
				}
			]
		},
		{
			"type": "actions",
			"elements": [
				{
					"type": "button",
					"text": {
						"type": "plain_text",
						"text": "Tutorial Adventure",
						"emoji": true
					},
					"value": "Tutorial Adventure",
					"action_id": "start_adventure_tutorial"
				}
			]
		}
	]

    try:
        # client.chat_postMessage(channel=user_id, text=message)
        client.chat_postMessage(channel=user_id, text="Start your adventure!", blocks=startBlocks)
        
    except Exception as e:
        # response_message = f"Error sending DM: {e}"
        # print(f"Error sending DM: {e}")
        # respond("Sorry, I couldn't send you a direct message.")
        # say(f"Error sending DM: {e}")
        # respond(response_message)
        respond(f"Error sending DM: {e}")


@app.action("start_adventure_tutorial")
def start_adventure_tutorial(ack, respond, command, client, say):
    # global tutorial_player_location
    ack()
    user_id = command["user_id"]
    logging.info(f"/startadventure called by user_id: {user_id}")
    current_adventure[user_id] = "tutorial"
    
    user_locations[user_id] = tutorialstory['rooms']['great_hall']

    current_location = user_locations[user_id]

    current_room = user_locations[user_id]
    items_in_room = current_room.get("items", [])
    if items_in_room:
        bullet_list = "\n".join(f"• {item}" for item in items_in_room)
    else:
        bullet_list = "Nothing interesting here."
    npcs_in_room = current_room.get("npcs", [])
    if npcs_in_room:
        npc_list = "\n".join(f"• {npc}" for npc in npcs_in_room)
    else:
        npc_list = "No one else here."
    

    # tutorial_player_location = tutorialstory['rooms']['great_hall']
    # current_room = tutorial_player_location
    # current_room = tutorial_player_location
    
    # message = f"Rooms: {tutorialstory['rooms']}"
    blocks = [
		{
			"type": "header",
			"text": {
				"type": "plain_text",
				# "text": tutorial_player_location['name'],
                "text": current_location['name'],
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
							# "text": tutorial_player_location['description'],
                            "text": current_location['description'],
							"style": {
								"italic": True
							}
						}
					]
				}
			]
		},
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": f"*Items here:*\n{bullet_list}"
            }
        },
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": f"*NPCs here:*\n{npc_list}"
            }
        }
	]

    try:
        # client.chat_postMessage(channel=user_id, text=message)
        client.chat_postMessage(channel=user_id, text="test", blocks=blocks)
        
    except Exception as e:
        # response_message = f"Error sending DM: {e}"
        # print(f"Error sending DM: {e}")
        # respond("Sorry, I couldn't send you a direct message.")
        # say(f"Error sending DM: {e}")
        # respond(response_message)
        respond(f"Error sending DM: {e}")

    # respond(f"Rooms: {tutorialstory['rooms']}")
    # respond(f"it works")

@app.command("/go")
def go(ack, respond, command, client, say, body, logger):
    # global tutorial_player_location
    ack()
    # logger.info(body)

    if current_adventure = "tutorial":
        user_id = command["user_id"]
        user_text = command.get("text", "").strip().lower()
        
        if user_id not in user_locations:
            respond("You need to start the adventure first using `/startadventure`.")
            return

        # if tutorial_player_location is None:
        #     respond("You need to start the adventure first using `/startadventure`.")
        #     return

        current_room = user_locations[user_id]
        # items_in_room = current_room.get("items", [])
        logging.info(f"/go called by user_id: {user_id}")
        logging.info(f"Current user_locations keys: {list(user_locations.keys())}")

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
            items_in_room = loc.get("items", [])
            if items_in_room:
                bullet_list = "\n".join(f"• {item}" for item in items_in_room)
            else:
                bullet_list = "Nothing interesting here."
            
            npcs_in_room = loc.get("npcs", [])
            if npcs_in_room:
                npc_list = "\n".join(f"• {npc}" for npc in npcs_in_room)
            else:
                npc_list = "No one else here."
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
                },
                {
                "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": f"*Items here:*\n{bullet_list}"
                    }
                },
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": f"*NPCs here:*\n{npc_list}"
                    }
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
            # try:
                if current_room == tutorialstory['rooms']['great_hall']:
                    # tutorial_player_location = tutorialstory['rooms']['hallway']
                    user_locations[user_id] = tutorialstory['rooms']['hallway']
                    send_room(user_locations[user_id])
                    # send_room(tutorial_player_location)
                else:
                    respond("You can't go north from here!")
                # if tutorial_player_location == tutorialstory['rooms']['great_hall']:
                #     tutorial_player_location = tutorialstory['rooms']['hallway']
                    
                
                #     client.chat_postMessage(channel=user_id, text="test", blocks=blocks)
                #     # client.chat_postMessage(blocks)
                # else:
                #     respond("You cannot move north")

            # except Exception as e:
            #     response_message = f"Error sending DM: {e}"

                # respond(response_message)

                # print(f"Error sending DM: {e}")
                # respond("Sorry, I couldn't send you a direct message.")
                
                # say(f"Error sending DM: {e}")
                # respond(f"{command['text']}")
        elif "south" in user_text:
            # try:
                if current_room == tutorialstory['rooms']['hallway']:
                    # tutorial_player_location = tutorialstory['rooms']['great_hall']
                    # send_room(tutorial_player_location)
                    user_locations[user_id]= tutorialstory['rooms']['great_hall']
                    send_room(user_locations[user_id])
                else:
                    respond("You can't go south from here!")
                # if tutorial_player_location == tutorialstory['rooms']['hallway']:
                #     tutorial_player_location = tutorialstory['rooms']['great_hall']

                #     client.chat_postMessage(channel=user_id, text="test", blocks=blocks)
                # else:
                #     # respond("You cannot move south")
                #     client.chat_postMessage(channel=user_id, text="You cannot move south")
            # except Exception as e:
            #     response_message = f"Error sending DM: {e}"

            #     # respond(response_message)

            #     print(f"Error sending DM: {e}")
            #     respond("Sorry, I couldn't send you a direct message.")
        elif "east" in user_text:
            # try:
                if current_room == tutorialstory['rooms']['hallway']:
                    user_locations[user_id] = tutorialstory['rooms']['training_room']
                    send_room(user_locations[user_id])
                    # tutorial_player_location = tutorialstory['rooms']['training_room']
                    # send_room(tutorial_player_location)
                elif current_room == tutorialstory['rooms']['ballroom']:
                    # tutorial_player_location = tutorialstory['rooms']['hallway']
                    # send_room(tutorial_player_location)
                    user_locations[user_id] = tutorialstory['rooms']['hallway']
                    send_room(user_locations[user_id])
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

            # except Exception as e:
            #     response_message = f"Error sending DM: {e}"

            #     # respond(response_message)

            #     print(f"Error sending DM: {e}")
            #     respond("Sorry, I couldn't send you a direct message.")
        elif "west" in user_text:
            # try:
                if current_room == tutorialstory['rooms']['hallway']:
                    # tutorial_player_location = tutorialstory['rooms']['ballroom']
                    # send_room(tutorial_player_location)
                    user_locations[user_id] = tutorialstory['rooms']['ballroom']
                    send_room(user_locations[user_id])
                elif current_room == tutorialstory['rooms']['training_room']:
                    user_locations[user_id] = tutorialstory['rooms']['hallway']
                    send_room(user_locations[user_id])
                    # tutorial_player_location = tutorialstory['rooms']['hallway']
                    # send_room(tutorial_player_location)
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
            # except Exception as e:
            #     response_message = f"Error sending DM: {e}"

            #     # respond(response_message)

            #     print(f"Error sending DM: {e}")
            #     respond("Sorry, I couldn't send you a direct message.")
        else:
            respond("Please provide a direction to travel, such as `/go north`.")
    else:
        respond("error")

@app.command("/look")
def look(ack, respond, command, client, say, body, logger):
    ack()
    if current_adventure = "tutorial":
        user_id = command["user_id"]

        if user_id not in user_locations:
            respond("You need to start the adventure first using `/startadventure`.")
            return
        current_room = user_locations[user_id]
        items_in_room = current_room.get("items", [])
        if items_in_room:
            bullet_list = "\n".join(f"• {item}" for item in items_in_room)
        else:
            bullet_list = "Nothing interesting here."
        
        npcs_in_room = current_room.get("npcs", [])
        if npcs_in_room:
            npc_list = "\n".join(f"• {npc}" for npc in npcs_in_room)
        else:
            npc_list = "No one else here."

        blocks = [
            {
                "type": "header",
                "text": {
                    "type": "plain_text",
                    # "text": tutorial_player_location['name'],
                    "text": current_room['name'],
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
                                # "text": tutorial_player_location['description'],
                                "text": current_room['description'],
                                "style": {
                                    "italic": True
                                }
                            }
                        ]
                    }
                ]
            },
            {
            "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f"*Items here:*\n{bullet_list}"
                }
            },
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f"*NPCs here:*\n{npc_list}"
                }
            }
        ]
        
        try:
            # client.chat_postMessage(channel=user_id, text=message)
            client.chat_postMessage(channel=user_id, text="Look", blocks=blocks)
            
        except Exception as e:
            # response_message = f"Error sending DM: {e}"
            # print(f"Error sending DM: {e}")
            # respond("Sorry, I couldn't send you a direct message.")
            # say(f"Error sending DM: {e}")
            # respond(response_message)
            respond(f"Error sending DM: {e}")
    else:
        respond("Error")

# @app.command("/talkto")
# def talkto(ack, respond, command, client, say, body, logger):
#     ack()

#     user_id = command["user_id"]
#     user_text = command.get("text", "").strip().lower()
    
#     if user_id not in user_locations:
#         respond("You need to start the adventure first using `/startadventure`.")
#         return

#     current_room = user_locations[user_id]


#     if "glykoy" in user_text:
#         if current_room == tutorialstory['rooms']['great_hall']:
#             client.chat_postMessage(channel=user_id, text="Look", blocks=blocks)

if __name__ == "__main__":
    # SocketModeHandler(app, SLACK_APP_TOKEN).start()
    threading.Thread(target=run_flask).start()
    handler = SocketModeHandler(app, app_token=os.environ.get("SLACK_APP_TOKEN"))
    handler.start()