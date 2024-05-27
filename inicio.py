from flask import Flask
app = Flask(__name__)
@app.route('/')
def helo_world():
    return 'hello, world'

if __name__ == '__main__':
    app.run()#para ejecutar el metodo

