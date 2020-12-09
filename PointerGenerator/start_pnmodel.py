from flask import Flask, jsonify, request
from flask import render_template
from flask_cors import CORS
import config
from data import Vocab
from predict import build_batch_by_article
from predict import BeamSearch
model_path = "./logs/weibo_adagrad/train_20201204_215649/model/zh45000"
vocab = Vocab("./dataset/finished_files/vocab", config.vocab_size)
envocab = Vocab("./dataset/envocab", config.vocab_size)
beam_processor = BeamSearch(model_path, vocab) # 注意需要选词汇表进行中英文摘要

## 读取模型

app=Flask(__name__,static_folder='assets',)
CORS(app,supports_creadtials=True)

@app.route('/ptrnet', methods=['POST'])
def pnpredict():
    if request.method == 'POST':
        plaintext = request.get_json()['text']
        try:
            # 待修改，如加上预处理等步骤
            batch = build_batch_by_article(plaintext, vocab)
            summary = beam_processor.decode(batch)
            return jsonify({'status_code': 1, 'summary_content': summary})

        except TimeoutError as err:
            print(err)
            return jsonify({'status_code':-1})


@app.route('/', methods=['POST','GET'])
def index():
    plaintext = request.args.get("text")
    # 调试时在此修改，如能够正确返回再在pnpredict用相同的方式改
    # 调试时，浏览器访问“ 127.0.0.1:5002/?text=待做摘要的文本 ”，看有没有结果
    batch = build_batch_by_article(plaintext, vocab)
    summary = beam_processor.decode(batch)
    return jsonify({"summary":summary})


if __name__ == '__main__':
    
    app.debug = True
    app.jinja_env.auto_reload = True
    app.config["JSON_AS_ASCII"] = False

    # load_model() 
    # app.run()
    
    app.run(host="0.0.0.0", port=5002)

