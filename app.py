import os
import yaml
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
from slack_sdk import WebClient
from dotenv import load_dotenv
import threading
from flask import Flask
flask_app = Flask(__name__)
import logging
import re
import time
logging.basicConfig(level=logging.INFO)
# load_dotenv()

SLACK_BOT_TOKEN = os.getenv("SLACK_BOT_TOKEN")
SLACK_APP_TOKEN = os.getenv("SLACK_APP_TOKEN")
client = WebClient(token=SLACK_BOT_TOKEN)
# logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

app = App(token=SLACK_BOT_TOKEN)


with open('./stories/tutorial-story.yaml', 'r') as file:
    tutorialstory = yaml.safe_load(file)



global tutorial_player_location
tutorial_player_location = None
user_locations = {}
current_adventure = {}
waiting_for_response_glykoy = {}
great_hammer = {}
waiting_for_response = {}
# if user_id in waiting_for_response_glykoy and waiting_for_response_glykoy[user_id] == channel_id:
# if user_id in great_hammer and great_hammer[user_id] == True:
visited_hallway = {}
visited_training_room = {}
visited_ballroom = {}
talked_to_glykoy_1 = {}
talked_to_glykoy_2 = {}
hit_dummy = {}

notified_users = set()



def check_tutorial_conditions(user_id):
    return (
        visited_hallway.get(user_id) and
        visited_training_room.get(user_id) and
        visited_ballroom.get(user_id) and
        talked_to_glykoy_1.get(user_id) and
        talked_to_glykoy_2.get(user_id) and
        hit_dummy.get(user_id)
    )

def background_checker(channel_id):
    while True:
        logger.debug("checking...")
        for user_id in set(visited_hallway.keys()):
            logger.debug(f"Checking user: {user_id}")
            logger.debug("Conditions:",
                         visited_hallway.get(user_id),
                         visited_training_room.get(user_id),
                         visited_ballroom.get(user_id),
                         talked_to_glykoy_1.get(user_id),
                         talked_to_glykoy_2.get(user_id),
                         hit_dummy.get(user_id))
            if user_id in notified_users:
                continue
            if check_tutorial_conditions(user_id):
                client.chat_postMessage(channel=channel_id, text=f"<@{user_id}> You've completed the tutorial! 🎉")
                notified_users.add(user_id)
            time.sleep(1)




# tutorial_player_location = tutorialstory['rooms']['great_hall']

@flask_app.route("/")
def home():
    return "Slack bot running!"

def run_flask():
    port = int(os.environ.get("PORT", 8080))
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
						"emoji": True
					},
					"value": "Tutorial Adventure",
					"action_id": "start_adventure_tutorial"
				},
                {
					"type": "button",
					"text": {
						"type": "plain_text",
						"text": "Adventures with Odif",
						"emoji": True
					},
					"value": "Adventures with Odif",
					"action_id": "start_adventures_with_odif"
				},
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

@app.action("start_adventures_with_odif")
def start_adventures_with_odif(ack, respond, command, client, say, body):
    ack()
    channel_id = body["channel"]["id"]
    message_ts = body["message"]["ts"]
    updated_blocks = []
    for block in body["message"]["blocks"]:
        if block.get("type") == "actions" and any(
            element.get("action_id") == "start_adventures_with_odif"
            for element in block.get("elements", [])
        ):
            continue  
        updated_blocks.append(block)
    client.chat_update(
        channel=channel_id,
        ts=message_ts,
        blocks=updated_blocks
    )
    user_id = body["user"]["id"]
    logging.info(f"/startadventure called by user_id: {user_id}")
    current_adventure[user_id] = "adventures_with_odif"

    client.chat_postMessage(channel=user_id, text="You walk up to the door. It's a strikingly bright blue color. You are feeling slightly nervous about what responsibilities lay beyond you. What do you do next?")
    time.sleep(0.5)
    client.chat_postMessage(channel=user_id, text=f"*Options:* 'Knock on the door' or 'Turn around and leave'")

    waiting_for_response[user_id] = channel_id



@app.action("start_adventure_tutorial")
def start_adventure_tutorial(ack, respond, command, client, say, body):
    # global tutorial_player_location
    ack()
    channel_id = body["channel"]["id"]
    message_ts = body["message"]["ts"]
    updated_blocks = []
    for block in body["message"]["blocks"]:
        if block.get("type") == "actions" and any(
            element.get("action_id") == "start_adventure_tutorial"
            for element in block.get("elements", [])
        ):
            continue  
        updated_blocks.append(block)
    client.chat_update(
        channel=channel_id,
        ts=message_ts,
        blocks=updated_blocks
    )
    user_id = body["user"]["id"]
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

    user_id = command["user_id"]
    if current_adventure[user_id] == "tutorial":
        
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
                    visited_hallway[user_id] = True
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
                    visited_training_room[user_id] = True
                    send_room(user_locations[user_id])
                    # tutorial_player_location = tutorialstory['rooms']['training_room']
                    # send_room(tutorial_player_location)
                elif current_room == tutorialstory['rooms']['ballroom']:
                    # tutorial_player_location = tutorialstory['rooms']['hallway']
                    # send_room(tutorial_player_location)
                    user_locations[user_id] = tutorialstory['rooms']['hallway']
                    visited_hallway[user_id] = True
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
                    visited_ballroom[user_id] = True
                    send_room(user_locations[user_id])
                elif current_room == tutorialstory['rooms']['training_room']:
                    user_locations[user_id] = tutorialstory['rooms']['hallway']
                    visited_hallway[user_id] = True
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
    user_id = command["user_id"]
    if current_adventure[user_id] == "tutorial":
        

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

@app.command("/talkto")
def talkto(ack, respond, command, client, say, body, logger):
    ack()

    user_id = command["user_id"]
    channel_id = command["channel_id"]
    if current_adventure[user_id] == "tutorial":
        user_text = command.get("text", "").strip().lower()
        
        if user_id not in user_locations:
            respond("You need to start the adventure first using `/startadventure`.")
            return

        current_room = user_locations[user_id]


        if "glykoy" in user_text:
            if current_room == tutorialstory['rooms']['great_hall']:
                client.chat_postMessage(channel=user_id, text=f"*Glykoy:* {tutorialstory['npcs']['glykoy']['dialogue']['wake'][0]}")
                time.sleep(0.5)
                client.chat_postMessage(channel=user_id, text=f"*Glykoy:* {tutorialstory['npcs']['glykoy']['dialogue']['wake'][1]}")
                time.sleep(0.5)
                client.chat_postMessage(channel=user_id, text=f"*Interact Options:* '{tutorialstory['npcs']['glykoy']['interact_options'][0]['option']}', '{tutorialstory['npcs']['glykoy']['interact_options'][1]['option']}'")

                waiting_for_response_glykoy[user_id] = channel_id
            else:
                client.chat_postMessage(channel=user_id, text="*Glykoy* is not in this room")
        else:
            client.chat_postMessage(channel=user_id, text="Please enter a valid npc to talk to")
    else:
        respond("Error")

@app.message("")
def handle_message(message, client, logger, respond, say):
    user_id = message["user"]
    channel_id = message["channel"]
    text = message.get("text", "").lower()
    # respond("testing")
    # say(f"Echo: You said '{text}'")

    if user_id in waiting_for_response_glykoy and waiting_for_response_glykoy[user_id] == channel_id:
        

        if "where" in text.lower() and "am" in text.lower() and "i" in text.lower():
            client.chat_postMessage(channel=user_id, text=f"*Glykoy:* {tutorialstory['npcs']['glykoy']['interact_options'][0]['response']}")
            talked_to_glykoy_1[user_id] = True
            del waiting_for_response_glykoy[user_id]
        elif "where" in text.lower() and "do" in text.lower() and "i" in text.lower() and "start" in text.lower():
            client.chat_postMessage(channel=user_id, text=f"*Glykoy:* {tutorialstory['npcs']['glykoy']['interact_options'][1]['response']}")
            talked_to_glykoy_2[user_id] = True
            del waiting_for_response_glykoy[user_id]
        else:
            client.chat_postMessage(channel=user_id, text="Please enter a vaild response")
    elif user_id in waiting_for_response and waiting_for_response[user_id] == channel_id:

        if "turn" in text.lower() and "around" in text.lower() and "and" in text.lower() and "leave" in text.lower():
            client.chat_postMessage(channel=user_id, text="You decide to turn back. Upon turning around, you see that it is now raining. Hard. Real hard. Thunder and lightning and everything What do you do next?")
            time.sleep(0.5)
            client.chat_postMessage(channel=user_id, text=f"*Options:* 'Walk home in the rain' or 'Turn back around to face the door'")
        elif "knock" in text.lower() and "on" in text.lower() and "the" in text.lower() and "door" in text.lower():
            client.chat_postMessage(channel=user_id, text="You knock. The door opens. Standing in the doorway you see your best friend, Amy. Behind Amy, there is a puppy, eagerly wagging his tail.")
            time.sleep(0.5)
            client.chat_postMessage(channel=user_id, text="'Hey!', says Amy. She smiles brightly.")
            time.sleep(0.5)
            client.chat_postMessage(channel=user_id, text="'Are you ready to take care of Odif?'")
            time.sleep(0.5)
            client.chat_postMessage(channel=user_id, text=f"*Options:* 'Yes' or 'No'")
            client.chat_postMessage(channel=user_id, text="Story in progress...this is where it ends, for now")
            del waiting_for_response[user_id]

        if "walk" in text.lower() and "home" in text.lower() and "in" in text.lower() and "the" in text.lower() and "rain" in text.lower():
            client.chat_postMessage(channel=user_id, text="You decide to walk back home. On the way home, you walk right past a lightning rod as a bolt of lightning arcs towards it. You don't make it")
            del waiting_for_response[user_id]
        elif "turn" in text.lower() and "back" in text.lower() and "around" in text.lower() and "to" in text.lower() and "face" in text.lower() and "the" in text.lower() and "door" in text.lower():
            client.chat_postMessage(channel=user_id, text="You walk up to the door. It's a strikingly bright blue color. You are feeling slightly nervous about what responsibilities lay beyond you. What do you do next?")
            time.sleep(0.5)
            client.chat_postMessage(channel=user_id, text=f"*Options:* 'Knock on the door' or 'Turn around and leave'")
    else:
        pass

@app.command("/pickup")
def pickup(ack, respond, command, client, say, body, logger):
    ack()

    user_id = command["user_id"]
    channel_id = command["channel_id"]
    if current_adventure[user_id] == "tutorial":
        user_text = command.get("text", "").strip().lower()
        
        if user_id not in user_locations:
            respond("You need to start the adventure first using `/startadventure`.")
            return

        current_room = user_locations[user_id]

        if "great hammer" in user_text:
            if current_room == tutorialstory['rooms']['great_hall']:
                client.chat_postMessage(channel=user_id, text=f"You have picked up the *Great Hammer*")
                great_hammer[user_id] = True
            else:
                client.chat_postMessage(channel=user_id, text="The *Great Hammer* is not in this room")
        else:
            client.chat_postMessage(channel=user_id, text="Please enter a valid item to pickup")
    else:
        respond("Error")

@app.command("/attack")
def attack(ack, respond, command, client, say, body, logger):
    ack()

    user_id = command["user_id"]
    channel_id = command["channel_id"]
    if current_adventure[user_id] == "tutorial":
        user_text = command.get("text", "").strip().lower()
        
        if user_id not in user_locations:
            respond("You need to start the adventure first using `/startadventure`.")
            return

        current_room = user_locations[user_id]

        if "training dummy" in user_text or "dummy" in user_text:
            if current_room == tutorialstory['rooms']['training_room']:
                if user_id in great_hammer and great_hammer[user_id] == True:
                    client.chat_postMessage(channel=user_id, text=f"{tutorialstory['npcs']['dummy']['interact_options'][0]['response']}")
                    hit_dummy[user_id] = True
                else:
                    client.chat_postMessage(channel=user_id, text="What on earth are you planning on attacking with? Find a weapon first")
            else:
                client.chat_postMessage(channel=user_id, text="The *dummy* is not in this room, dummy")
        else:
            client.chat_postMessage(channel=user_id, text="Please enter a valid item to attack")
    else:
        respond("Error")

@app.command("/inventory")
def attack(ack, respond, command, client, say, body, logger):
    ack()

    user_id = command["user_id"]
    channel_id = command["channel_id"]
    if current_adventure[user_id] == "tutorial":
        user_text = command.get("text", "").strip().lower()
        
        if user_id not in user_locations:
            respond("You need to start the adventure first using `/startadventure`.")
            return

        current_room = user_locations[user_id]

        if user_id in great_hammer and great_hammer[user_id] == True:
            inventoryBlocks = [
                {
                    "type": "header",
                    "text": {
                        "type": "plain_text",
                        "text": "Inventory"
                    }
                },
                {
                    "type": "rich_text",
                    "elements": [
                        {
                            "type": "rich_text_list",
                            "style": "bullet",
                            "indent": 0,
                            "border": 0,
                            "elements": [
                                {
                                    "type": "rich_text_section",
                                    "elements": [
                                        {
                                            "type": "text",
                                            "text": "Great Hammer"
                                        }
                                    ]
                                }
                            ]
                        }
                    ]
                }
            ]
            
            client.chat_postMessage(channel=user_id, text="Inventory", blocks=inventoryBlocks)
        else:
            client.chat_postMessage(channel=user_id, text="Your inventory is empty")
    else:
        respond("Error")

if __name__ == "__main__":
    # SocketModeHandler(app, SLACK_APP_TOKEN).start()
    threading.Thread(target=run_flask).start()
    threading.Thread(target=lambda: background_checker("U07AZFQLPQ8"), daemon=True).start()
    handler = SocketModeHandler(app, app_token=os.environ.get("SLACK_APP_TOKEN"))
    handler.start()
    