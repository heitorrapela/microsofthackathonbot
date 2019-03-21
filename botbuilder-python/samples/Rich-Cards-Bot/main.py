# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

"""
This sample shows how to use different types of rich cards.
"""


from aiohttp import web
from pygame import mixer # Load the required library
import webbrowser

from botbuilder.schema import (Activity, ActivityTypes,
                               AnimationCard, AudioCard, Attachment,
                               ActionTypes, CardAction,
                               CardImage, HeroCard,
                               MediaUrl, ThumbnailUrl,
                               ThumbnailCard, VideoCard,
                               ReceiptCard, SigninCard,
                               Fact, ReceiptItem)
from botbuilder.core import (BotFrameworkAdapter, BotFrameworkAdapterSettings, TurnContext,
                             ConversationState, MemoryStorage, UserState, CardFactory)
"""Import AdaptiveCard content from adjacent file"""
from adaptive_card_example import ADAPTIVE_CARD_CONTENT

APP_ID = ''
APP_PASSWORD = ''
PORT = 9000
SETTINGS = BotFrameworkAdapterSettings(APP_ID, APP_PASSWORD)
ADAPTER = BotFrameworkAdapter(SETTINGS)

# Create MemoryStorage, UserState and ConversationState
memory = MemoryStorage()
# Commented out user_state because it's not being used.
# user_state = UserState(memory)
conversation_state = ConversationState(memory)

# Register both State middleware on the adapter.
# Commented out user_state because it's not being used.
# ADAPTER.use(user_state)
ADAPTER.use(conversation_state)


# Methods to generate cards
def create_baby_check_card() -> Attachment:
    #ret = func()
    ret = 1
    if (ret < 1):
        msg = "Problem with baby"
    elif (ret > 1):
        msg = "More people wtih baby"
    else:
        msg = "Baby is ok"

    return msg


def create_check_env() -> Attachment:
    addr = "http://localhost:5522"
    webbrowser.open_new(addr)

def create_lullaby_play() -> Attachment:
    mixer.init()
    mixer.music.load('./twinkle_twinkle_little_star.mp3')
    mixer.music.play()

def create_lullaby_stop() -> Attachment:
    mixer.music.stop()

async def create_reply_activity(request_activity: Activity, text: str, attachment: Attachment = None) -> Activity:
    activity = Activity(
        type=ActivityTypes.message,
        channel_id=request_activity.channel_id,
        conversation=request_activity.conversation,
        recipient=request_activity.from_property,
        from_property=request_activity.recipient,
        text=text,
        service_url=request_activity.service_url)
    if attachment:
        activity.attachments = [attachment]
    return activity


async def handle_message(context: TurnContext) -> web.Response:
    # Access the state for the conversation between the user and the bot.
    state = await conversation_state.get(context)
    if hasattr(state, 'in_prompt'):
        if state.in_prompt:
            state.in_prompt = False
            return await card_response(context)
        else:
            state.in_prompt = True
            prompt_message = await create_reply_activity(context.activity, 'Hello, what do you want to do?\n'
                                                                           '(1) Check Image\n'
                                                                           '(2) Check Environment\n'
                                                                           '(3) Play Lullaby\n'
                                                                           '(4) Stop Lullaby\n'    )
            await context.send_activity(prompt_message)
            return web.Response(status=202)
    else:
        state.in_prompt = True
        prompt_message = await create_reply_activity(context.activity, 'Hello, what do you want to do?\n'
                                                                       '(1) Check Image\n'
                                                                       '(2) Check Environment\n'
                                                                       '(3) Play Lullaby\n'
                                                                       '(4) Stop Lullaby\n')
        await context.send_activity(prompt_message)
        return web.Response(status=202)


async def card_response(context: TurnContext) -> web.Response:
    response = context.activity.text.strip()
    choice_dict = {
        '1': [create_baby_check_card], 'Check Image': [create_baby_check_card],
        '2': [create_check_env], 'Monitor Environment': [create_check_env],
        '3': [create_lullaby_play], 'Play Lullaby': [create_lullaby_play],
        '4': [create_lullaby_stop], 'Stop Lullaby': [create_lullaby_play],
    }

    # Get the functions that will generate the card(s) for our response
    # If the stripped response from the user is not found in our choice_dict, default to None
    choice = choice_dict.get(response, None)
    # If the user's choice was not found, respond saying the bot didn't understand the user's response.
    if not choice:
        not_found = await create_reply_activity(context.activity, 'Sorry, I didn\'t understand that. :(')
        await context.send_activity(not_found)
        return web.Response(status=202)
    elif (response == '1'):
        msg = create_baby_check_card()
        response = await create_reply_activity(context.activity, msg)
        await context.send_activity(response)
    else:
        for func in choice:
            card = func()
            response = await create_reply_activity(context.activity, '', card)
            await context.send_activity(response)
        return web.Response(status=200)


async def handle_conversation_update(context: TurnContext) -> web.Response:
    if context.activity.members_added[0].id != context.activity.recipient.id:
        response = await create_reply_activity(context.activity, 'Welcome to the Super Nany Bot!')
        await context.send_activity(response)
    return web.Response(status=200)


async def unhandled_activity() -> web.Response:
    return web.Response(status=404)


async def request_handler(context: TurnContext) -> web.Response:
    if context.activity.type == 'message':
        return await handle_message(context)
    elif context.activity.type == 'conversationUpdate':
        return await handle_conversation_update(context)
    else:
        return await unhandled_activity()


async def messages(req: web.web_request) -> web.Response:
    body = await req.json()
    activity = Activity().deserialize(body)
    auth_header = req.headers['Authorization'] if 'Authorization' in req.headers else ''
    try:
        return await ADAPTER.process_activity(activity, auth_header, request_handler)
    except Exception as e:
        raise e


app = web.Application()
app.router.add_post('/', messages)

try:
    web.run_app(app, host='localhost', port=PORT)
except Exception as e:
    raise e
