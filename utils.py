from clarifai_grpc.channel.clarifai_channel import ClarifaiChannel
from clarifai_grpc.grpc.api import resources_pb2, service_pb2, service_pb2_grpc
from clarifai_grpc.grpc.api.status import status_pb2, status_code_pb2
from emoji import emojize
import logging
from random import randint, choice
from telegram import ReplyKeyboardMarkup, KeyboardButton


from settings import USER_EMOJI, CLARIFAI_API_KEY


def main_keyboard():
    return ReplyKeyboardMarkup([
        ['Gimme a cat!', KeyboardButton('Take my location.', request_location=True)],
        ['Anketa'],
        ])


def choice_emoji(user_data):
    if 'emoji' not in user_data:
        emoji = choice(USER_EMOJI)
        return emojize(emoji, language='alias')
    return user_data['emoji']


def bot_guess_number(user_number):
    bot_number = randint(user_number - 10, user_number + 10)
    if user_number > bot_number:
        message = f'Your number is {user_number}. My number is {bot_number}. It is a victory.'
    elif user_number == bot_number:
        message = f'Your number is {user_number}. My number is {bot_number}. It is a tie.'
    else:
        message= f'Your number is {user_number}. My number is {bot_number}. It is a loss.'
    return message


def has_object_on_image(file_name, object_name):
    channel = ClarifaiChannel.get_grpc_channel()
    stub = service_pb2_grpc.V2Stub(channel)
    metadata = (('authorization', 'Key ' + f'{CLARIFAI_API_KEY}'),)
    
    with open(file_name, 'rb') as f:
        file_data = f.read()
        image = resources_pb2.Image(base64=file_data)
        
    request = service_pb2.PostModelOutputsRequest(
        model_id='aaa03c23b3724a16a56b629203edc62c',
        inputs=[
            resources_pb2.Input(data=resources_pb2.Data(image=image))
        ])

    response = stub.PostModelOutputs(request, metadata=metadata)
    return check_response_for_object(response, object_name)


def check_response_for_object(response, object_name):
    if response.status.code == status_code_pb2.SUCCESS:
        for concept in response.outputs[0].data.concepts:
            if concept.name == object_name and concept.value >= 0.85:
                return True
    else: 
        logging.info('Clarifai status is not OK.')
    return False


if __name__ == '__main__':
    print(has_object_on_image('images\dog.jpg', 'cat'))
