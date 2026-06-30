from flask import Flask, render_template

from config.imports_blueprints import ini_imports_blueprints

app = Flask(__name__)
ini_imports_blueprints()

@app.route('/')
def ini_app():
    return print('Flask Ok')

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
