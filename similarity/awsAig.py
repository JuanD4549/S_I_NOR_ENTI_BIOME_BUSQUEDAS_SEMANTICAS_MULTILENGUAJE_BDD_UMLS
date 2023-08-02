from flask import Flask, request
import os
app = Flask(__name__)

@app.route('/awesomeAigment', methods=['GET', 'POST'])
def awesome_aigment():
    if request.method == 'GET':
        os.system('ipython awesomeAigment2.ipynb')
        return "ok"
if __name__=='__main__':
    app.run(host='0.0.0.0', port=3000)