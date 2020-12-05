from flask import Flask, jsonify, request
from flask import render_template

import nltk
import torch
import torch.nn.functional as F
from pytorch_transformers import BertTokenizer
import sys
sys.path.append('ts_bert/src/')
from ts_bert.src.opts import parse_opt
from ts_bert.src.models.model_builder import ExtSummarizer, AbsSummarizer
from ts_bert.src.models import data_loader
from ts_bert.src.models.trainer_ext import test_trainer_ext
from ts_bert.src.models.predictor import test_predictor

use_gpu = True

ns_model=None
be_trainer=None
pn_model=None
ba_predictor=None


def load_model():
    """Load the pre-trained model, you can use your model just as easily.
    """
    global ns_model
    global be_trainer
    global pn_model
    global ba_predictor

    be_args = parse_opt('ts_bert/src/cfgs/bertext_onetext.yml')
    ba_args = parse_opt('ts_bert/src/cfgs/bertabs_onetext.yml')
    device = "cpu" if be_args.visible_gpus == '-1' else "cuda"
    device_id = 0 if device == "cuda" else -1

    be_checkpoint = torch.load(be_args.test_from, map_location=lambda storage, loc: storage)
    be_model = ExtSummarizer(be_args, device, be_checkpoint)
    be_model.eval()

    be_trainer = test_trainer_ext(be_args, device_id, be_model, None)

    ba_checkpoint = torch.load(ba_args.test_from, map_location=lambda storage, loc: storage)
    ba_model = AbsSummarizer(ba_args, device, ba_checkpoint)
    ba_model.eval()

    tokenizer = BertTokenizer.from_pretrained('bert-base-uncased', do_lower_case=True, cache_dir=ba_args.temp_dir)
    symbols = {'BOS': tokenizer.vocab['[unused0]'], 'EOS': tokenizer.vocab['[unused1]'],
               'PAD': tokenizer.vocab['[PAD]'], 'EOQ': tokenizer.vocab['[unused2]']}
    ba_predictor = test_predictor(ba_args, tokenizer, symbols, ba_model)



def preprocess_text_ext(text):
    sen_tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')
    sentences = sen_tokenizer.tokenize(text)
    text = " [CLS] [SEP] ".join(sentences)

    return text



def neusum_predict(text):
    return "neusum"

def bertext_predict(text):

    if use_gpu == True:
        device = "cuda"
    else:
        device = "cpu"
    test_iter = data_loader.load_one_text_web(text, device)
    prediction = be_trainer.predict_text(test_iter, -1)

    return prediction

def ptrnet_predict(text):
    return "ptrnet"

def bertabs_predict(text):

    if use_gpu == True:
        device = "cuda"
    else:
        device = "cpu"
    test_iter = data_loader.load_one_text_web(text, device)
    prediction = ba_predictor.translate_text(test_iter, -1)

    return prediction


app=Flask(__name__,static_folder='assets',)


@app.route('/neusum', methods=['POST'])
def nspredict():
    if request.method == 'POST':
        plaintext = request.get_json()['text']
        try:
            summary= neusum_predict(plaintext)
            return jsonify({'status_code': 1, 'summary_content': summary})

        except TimeoutError as err:
            print(err)
            return jsonify({'status_code':-1})


@app.route('/bertext', methods=['POST'])
def bepredict():
    if request.method == 'POST':
        plaintext = request.get_json()['text']
        try:
            # print(plaintext)
            # plaintext = "this Terry Jones had a love of the absurd that contributed much to the anarchic humour of Monty Python's Flying Circus. His style of visual comedy, leavened with a touch of the surreal, inspired many comedians who followed him. It was on Python that he honed his directing skills, notably on Life of Brian and The Meaning of Life. A keen historian, he wrote a number of books and fronted TV documentaries on ancient and medieval history. Terence Graham Parry Jones was born in Colwyn Bay in north Wales on 1 February 1942. His grandparents ran the local amateur operatic society and staged Gilbert and Sullivan concerts on the town's pier each year His family moved to Surrey when he was four but he always felt nostalgic about his native land. \"I couldn't bear it and for the longest time I wanted Wales back,\" he once said. \"I still feel very Welsh and feel it's where I should be really.\" After leaving the Royal Grammar School in Guildford, where he captained the school, he went on to read English at St Edmund Hall, Oxford. However, as he put it, he \"strayed into history\", the subject in which he graduated. While at Oxford he wrote sketches for the Oxford Revue and performed alongside a fellow student, Michael Palin."
            plaintext = preprocess_text_ext(plaintext)

            summary= bertext_predict(plaintext)

            return jsonify({'status_code': 1, 'summary_content': summary})

        except TimeoutError as err:
            print(err)
            return jsonify({'status_code':-1})

@app.route('/ptrnet', methods=['POST'])
def pnpredict():
    if request.method == 'POST':
        plaintext = request.get_json()['text']
        try:
            summary= ptrnet_predict(plaintext)
            return jsonify({'status_code': 1, 'summary_content': summary})

        except TimeoutError as err:
            print(err)
            return jsonify({'status_code':-1})



@app.route('/bertabs', methods=['POST'])
def bapredict():
    if request.method == 'POST':
        plaintext = request.get_json()['text']
        try:
            ## 待修改
            # plaintext = "this Terry Jones had a love of the absurd that contributed much to the anarchic humour of Monty Python's Flying Circus. His style of visual comedy, leavened with a touch of the surreal, inspired many comedians who followed him. It was on Python that he honed his directing skills, notably on Life of Brian and The Meaning of Life. A keen historian, he wrote a number of books and fronted TV documentaries on ancient and medieval history. Terence Graham Parry Jones was born in Colwyn Bay in north Wales on 1 February 1942. His grandparents ran the local amateur operatic society and staged Gilbert and Sullivan concerts on the town's pier each year His family moved to Surrey when he was four but he always felt nostalgic about his native land. \"I couldn't bear it and for the longest time I wanted Wales back,\" he once said. \"I still feel very Welsh and feel it's where I should be really.\" After leaving the Royal Grammar School in Guildford, where he captained the school, he went on to read English at St Edmund Hall, Oxford. However, as he put it, he \"strayed into history\", the subject in which he graduated. While at Oxford he wrote sketches for the Oxford Revue and performed alongside a fellow student, Michael Palin."
            summary= bertabs_predict(plaintext)

            return jsonify({'status_code': 1, 'summary_content': summary})

        except TimeoutError as err:
            print(err)
            return jsonify({'status_code':-1})


@app.route('/', methods=['POST','GET'])
def index():
    return render_template("index.html")


if __name__ == '__main__':
    app.debug = True
    app.jinja_env.auto_reload = True
    #app.run()
    load_model()
    app.run(host="0.0.0.0")

