from build import rebuild_all
from bottle import route, run, template

@route('/admin/rebuild')
def rebuild():
    rebuild_all()
    return 'Rebuilt done !'

run(host='localhost', port=8000, debug=True)