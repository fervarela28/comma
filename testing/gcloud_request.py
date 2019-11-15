import requests
import flask

params = {'user':'andrewandrews@email.com',
       'pass':'andrewandrews',
       'rest':'test',
       'party_size':'test',
       'start_date':'test',
       'end_date':'test',
       'start_time':'test',
       'end_time':'test'}

delete = {'id':'113'}
#app = flask.Flask('thisapp')
#response = app.make_response(({'a':'b'}, 200))
#app = flask.Flask(__name__)
#with app.app_context():
#	print flask.jsonify(a=[['user', 'pass', 'rest', 'party_size', 'start_date', 'end_date', 'start_time', 'end_time'], ['fernandoavarelaf@gmail.com', 'qweasdzxc', '443', '4', '2019-11-14', '2019-11-30', '17:00', '21:00'], ['fernandoavarelaf@gmail.com', 'qweasdzxc', '6174', '4', '2019-10-16', '2019-12-31', '17:00', '21:00'], ['fernandoavarelaf@gmail.com', 'qweasdzxc', '443', '2', '2019-09-16', '2019-12-31', '17:00', '23:00']])

r = requests.get(url = "https://us-central1-quickstart-1558446744841.cloudfunctions.net/delete_reservation_request", params = delete) 
#r = requests.get(url = "https://us-central1-quickstart-1558446744841.cloudfunctions.net/get_user_requests", params = params) 
print r.text

