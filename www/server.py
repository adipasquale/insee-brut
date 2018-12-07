from build import build
from bottle import route, run, template
from settings import BOTTLE_DEBUG


@route('/admin/rebuild')
def rebuild():
    build()
    return 'Rebuilt done !'

run(host='localhost', port=8000, debug=BOTTLE_DEBUG)