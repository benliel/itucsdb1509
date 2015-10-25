import datetime
from flask import Flask
from flask import render_template


app = Flask(__name__)


@app.route('/') 
def home_page():
    now = datetime.datetime.now()
    return render_template('home.html', current_time=now.ctime())
    
    
@app.route('/movies') 
def movies_page():
    return render_template('movies.html')


if __name__ == '__main__': 
    app.run(host='0.0.0.0', port=5000)

<<<<<<< HEAD
=======
if __name__ == '__main__':
    VCAP_APP_PORT = os.getenv('VCAP_APP_PORT')
    if VCAP_APP_PORT is not None:
        port, debug = int(VCAP_APP_PORT), False
    else:
        port, debug = 5000, True
    app.run(host='0.0.0.0', port=port, debug=debug)
>>>>>>> f735b8df76a23f4c11be9c39487943ce01065987
