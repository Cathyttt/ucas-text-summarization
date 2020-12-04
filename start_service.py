from flask import Flask, jsonify, request
from flask import render_template


import torch
import torch.nn.functional as F
from pytorch_transformers import BertTokenizer
from ts_bert.src.opts import parse_opt
from ts_bert.src.models.model_builder import ExtSummarizer, AbsSummarizer
from ts_bert.src.models import data_loader
from ts_bert.src.models.trainer_ext import build_trainer_ext
from ts_bert.src.models.predictor import build_predictor
from ts_bert.src.models.trainer import build_trainer

use_gpu = True

ns_model=None
be_model=None
pn_model=None
ba_model=None

## 读取四种模型
def load_model():
    """Load the pre-trained model, you can use your model just as easily.
    """
    global ns_model
    global be_model
    global pn_model
    global ba_model

    be_args = parse_opt()
    ba_args = parse_opt()
    device = "cpu" if be_args.visible_gpus == '-1' else "cuda"

    be_checkpoint = torch.load(be_args.test_from, map_location=lambda storage, loc: storage)
    be_model = ExtSummarizer(be_args, device, be_checkpoint)
    be_model.eval()

    ba_checkpoint = torch.load(ba_args.test_from, map_location=lambda storage, loc: storage)
    ba_model = AbsSummarizer(ba_args, device, ba_checkpoint)
    ba_model.eval()

def preprocess_text_ext(text):



def neusum_predict(text):
    return "neusum"

def bertext_predict(args, text, device, model):

    test_iter = data_loader.load_one_text(args, text, '', device)
    device_id = 0 if device == "cuda" else -1
    trainer = build_trainer_ext(args, device_id, model, None)
    prediction = trainer.predict_text(test_iter, -1)

    return prediction

def ptrnet_predict(text):
    return "ptrnet"

def bertabs_predict(args, text, device, model):

    test_iter = data_loader.load_one_text(args, text, '', device)
    tokenizer = BertTokenizer.from_pretrained('bert-base-uncased', do_lower_case=True, cache_dir=args.temp_dir)
    symbols = {'BOS': tokenizer.vocab['[unused0]'], 'EOS': tokenizer.vocab['[unused1]'],
               'PAD': tokenizer.vocab['[PAD]'], 'EOQ': tokenizer.vocab['[unused2]']}
    predictor = build_predictor(args, tokenizer, symbols, model)
    prediction = predictor.translate_text(test_iter, -1)

    return prediction


app=Flask(__name__,static_folder='assets',)


@app.route('/neusum', methods=['POST'])
def nspredict():
    if request.method == 'POST':
        plaintext = request.args.get('text')
        try:
            summary= neusum_predict(plaintext)
            return jsonify({'status_code': 1, 'summary_content': summary})

        except TimeoutError as err:
            print(err)
            return jsonify({'status_code':-1})


@app.route('/bertext', methods=['POST'])
def bepredict():
    if request.method == 'POST':
        plaintext = request.args.get('text')
        try:
            ## 待修改
            summary= bertext_predict(plaintext)

            return jsonify({'status_code': 1, 'summary_content': summary})

        except TimeoutError as err:
            print(err)
            return jsonify({'status_code':-1})

@app.route('/ptrnet', methods=['POST'])
def pnpredict():
    if request.method == 'POST':
        plaintext = request.args.get('text')
        try:
            summary= ptrnet_predict(plaintext)
            return jsonify({'status_code': 1, 'summary_content': summary})

        except TimeoutError as err:
            print(err)
            return jsonify({'status_code':-1})



@app.route('/bertabs', methods=['POST'])
def bapredict():
    if request.method == 'POST':
        plaintext = request.args.get('text')
        try:
            ## 待修改
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
    app.run()
    # app.run(host="0.0.0.0")
