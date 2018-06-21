from bson.objectid import ObjectId
import ast
import random
import os
from flask import Blueprint, request
from app.commons import build_response
from app.intents.models import Intent, LabeledSentences
from app import configuration as config

train = Blueprint('train_blueprint', __name__,
                  url_prefix='/train'
                  )

pwd = os.path.dirname(os.path.abspath(os.path.join(__file__, '..', '..')))

filename = pwd + "/" + config.training_data

def remove_empty_lines():
    if not os.path.isfile(filename):
        return
    with open(filename) as filehandle:
        lines = filehandle.readlines()

    with open(filename, 'w') as filehandle:
        lines = filter(lambda x: x.strip(), lines)
        filehandle.writelines(lines)

def shuffle_training_data():
    f = open(filename)
    entire_file = f.read()
    file_in_a_list = entire_file.split("\n")
    num_lines = len(file_in_a_list)
    random_nums = random.sample(xrange(num_lines), num_lines)
    f.close()
    o = open(filename, "w")
    # file_in_a_list = filter(lambda x: x.strip(), file_in_a_list) #todo: strip empty lines
    for i in random_nums:
        o.write(file_in_a_list[i] + "\n")
    o.close()
    remove_empty_lines()

@train.route('/<story_id>/data', methods=['POST'])
def save_training_data(story_id):
    """
    Save training data for given story
    :param story_id:
    :return:
    """
    story = Intent.objects.get(id=ObjectId(story_id))
    save_data = "null"
    try:
        training_file = open(filename, "a+")
        for example in request.json:
            if example.pop("save", "none").strip() == "true":
                training_file.write("__label__" + str(story.intentId) + " " + example.get("text").lower() + "\n")
        training_file.close()
        remove_empty_lines()
        training_file = open(filename, "r+")
        save_datalines = training_file.readlines()
        save_data = ""
        for data_line in save_datalines:
            save_data = save_data + data_line
            # save_data = save_datalines[len(save_datalines)-1]
        training_file.close()
    except Exception as e:
        return build_response.sent_plain_text("Error while opening file %s" % str(e))
    story.trainingData = request.json
    story.save()
    return build_response.sent_plain_text(save_data)


@train.route('/<story_id>/data', methods=['GET'])
def get_training_data(story_id):
    """
    retrive training data for a given story
    :param story_id:
    :return:
    """
    story = Intent.objects.get(id=ObjectId(story_id))
    return build_response.build_json(story.trainingData)