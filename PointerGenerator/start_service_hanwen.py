from flask import Flask, jsonify, request
from flask import render_template

import config
from data import Vocab
from predict import build_batch_by_article
from predict import BeamSearch
model_path = "./logs/weibo_adagrad/train_20201204_215649/model/zh45000"
vocab = Vocab("./dataset/finished_files/vocab", config.vocab_size)
envocab = Vocab("./dataset/envocab", config.vocab_size)
beam_processor = BeamSearch(model_path, vocab) # 注意需要选词汇表进行中英文摘要

def ptrnet_predict(text):
    return "ptrnet"

app=Flask(__name__,static_folder='assets',)

@app.route('/ptrnet', methods=['POST'])
def pnpredict():
    if request.method == 'POST':
        plaintext = request.get_json()['text']
        # print(plaintext)
        try:
            batch = build_batch_by_article(plaintext, vocab)
            summary = beam_processor.decode(batch)
            return jsonify({'status_code': 1, 'summary_content': summary})

        except TimeoutError as err:
            print(err)
            return jsonify({'status_code':-1})

@app.route('/', methods=['POST','GET'])
def index():
    return render_template("index.html")


if __name__ == '__main__':
    string = "近日，一段消防员用叉子吃饭的视频在网上引起热议。原来是因为训练强度太大，半天下来，大家拿筷子的手一直在抖，甚至没法夹菜。于是，用叉子吃饭，渐渐成了上海黄浦消防车站中队饭桌上的传统。转发，向消防员致敬！"
    app.debug = True
    app.jinja_env.auto_reload = True
    app.run()
    # app.run(host="0.0.0.0")

