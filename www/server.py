from build import rebuild_all
from bottle import route, run, template

@route('/rebuild')
def rebuild():
    rebuild_all()
    return 'Rebuilt done !'

run(host='0.0.0.0', port=8000, debug=True)