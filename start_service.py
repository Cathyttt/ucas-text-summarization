from flask import Flask, jsonify, request
from flask import render_template


import torch
import torch.nn.functional as F

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

    model = loadbert(pretrained=True)
    model.eval()
    if use_gpu:
        model.cuda()


def neusum_predict(text):
    return "neusum"

def bertext_predict(text):
    return "bertext"+"\'"

def ptrnet_predict(text):
    return "ptrnet"

def bertabs_predict(text):
    return "bertabs"


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

