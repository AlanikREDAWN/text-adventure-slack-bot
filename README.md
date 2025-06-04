# Slack Text Adventure Bot
## What is this?

A simple framework to create text adventure games playable inside Slack.
Explore rooms, talk to characters, pick up items, use commands, and build your own story.
How to play

Use these commands in Slack:

    /go [direction] — move north, south, east, or west

    /look — see the room description again

    /talk to [npc] — talk to a character

    /pickup [item] — pick up an item

    /use [item] — use an item in your inventory

    /attack [target] — attack an enemy or target

    /inventory — see what you are carrying

How to create your own story

Write a YAML file defining:

    Rooms: locations with descriptions, exits, NPCs, and items

    NPCs: characters with dialogue and interaction options

    Items: things players can pick up and use

    Events: special messages or actions triggered by player behavior

    Flags: variables to track player progress or game state


Extending your game

Add more rooms, quests, puzzles, and interactions by editing your YAML file. Use flags and events to create complex storylines.
