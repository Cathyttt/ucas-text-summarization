from flask import Flask, jsonify, request
from flask_cors import CORS
from main import predict
use_gpu = True
bs_model=None


## 读取模型
def load_model():
    """Load the pre-trained model, you can use your model just as easily.
    """
    global bs_model

    model = loadbert(pretrained=True)
    model.eval()
    if use_gpu:
        model.cuda()


def banditsum_predict(text):
    # 待添加
    return text

app=Flask(__name__)
CORS(app,supports_creadtials=True)

@app.route('/banditsum', methods=['POST'])
def bspredict():
    if request.method == 'POST':
        plaintext = request.get_json()['text']
        try:
            # 待修改，如加上预处理等步骤
            summary= banditsum_predict(plaintext)

            return jsonify({'status_code': 1, 'summary_content': summary})

        except TimeoutError as err:
            print(err)
            return jsonify({'status_code':-1})

@app.route('/', methods=['POST','GET'])
def index():
    plaintext = request.args.get("text")

    # 调试时在此修改，如能够正确返回再在bspredict用相同的方式改
    # 调试时，浏览器访问“ 127.0.0.1:5001/?text=待做摘要的文本 ”，看有没有结果

    summary = predict(plaintext)

    return jsonify({"summary": summary})


if __name__ == '__main__':
    app.debug = True
    app.jinja_env.auto_reload = True

    app.run(host="0.0.0.0",port=5001)


