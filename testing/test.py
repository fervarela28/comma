import requests
from datetime import datetime, timedelta
import time
import random

def send_get_request(resy_url, params):
    headers= {'Authorization': 'ResyAPI api_key="VbWk7s3L4KiK5fzlO7JD3Q5EYolJI7n5"'}
    r = requests.get(url = resy_url, params = params, headers=headers) 
    #print("request url: ", r.url)
    data = r.json()
    return data

def send_post_request(resy_url, data):
    headers= {'Authorization': 'ResyAPI api_key="VbWk7s3L4KiK5fzlO7JD3Q5EYolJI7n5"'}
    r = requests.post(url = resy_url, data = data, headers=headers)
    #print("request url: ", r.url)
    data = r.json()
    return data

# functions using resy's API
def login(email, password):
    # response has auth_token & payment_id. For auth_token & payment_id, response['token'] & response['payment_method_id']
    return send_post_request("https://api.resy.com/3/auth/password", {'email': email,'password': password})

def find_reservations(auth_token, day, party_size, venue_id):
    return send_get_request("https://api.resy.com/4/find", {'auth_token': auth_token,'day':day,'lat':'0','long':'0','party_size':party_size,'venue_id':venue_id})

def get_reservation_details(auth_token, day, party_size, config_id):
    return send_get_request("https://api.resy.com/3/details", {'auth_token': auth_token, 'day': day, 'party_size': party_size, 'config_id': config_id})

def get_user_reservations(auth_token, book_on_behalf_of, limit, offset, type_input):
    return send_get_request("https://api.resy.com/2/user/reservations", {'auth_token': auth_token,'book_on_behalf_of':book_on_behalf_of,'limit':limit,'offset':offset,'type':type_input})

def notify(auth_token, day, venue_id, time_preferred_start, time_preferred_end, num_seats, service_type_id):
    return send_post_request('https://api.resy.com/2/notify', {'auth_token': auth_token,'day':day,'num_seats':num_seats,'venue_id':venue_id, 
                                            'time_preferred_start': time_preferred_start, 'time_preferred_end':time_preferred_end, 
                                            'service_type_id':service_type_id})

def set_notifies(email, password, days_list, venue_id, time_preferred_start, time_preferred_end, num_seats, service_type_id):
    user_info = login(email, password)
    auth_token = user_info['token']
    print 'auth_token: ', auth_token
    for day in days_list:
        print notify(auth_token, day, venue_id, time_preferred_start, time_preferred_end, num_seats, service_type_id)
    return

set_notifies('commanyccomma@gmail.com', 'commanyccomma', ['2019-12-'+str(x) for x in range(10,11)], 466, '19:00:00','19:00:00', 4, 2)


def get_available_reservation(email, password, day, venue_id, party_size):
    user_info = login(email, password)
    auth_token = user_info['token']
    print 'auth_token: ', auth_token
    payment_id = user_info['payment_method_id']
    print 'payment_id: ', payment_id
    reservations = find_reservations(auth_token, day, party_size, venue_id)
    print reservations['results']['venues'][0]['slots']
    config_id = reservations['results']['venues'][0]['slots'][0]['config']['token']
    print 'config_id: ', config_id
    reservation_details = get_reservation_details(auth_token, day, party_size, config_id)
    book_token = reservation_details['book_token']['value']
    book = send_post_request("https://api.resy.com/3/book", {'book_token': book_token, 'struct_payment_method':'{"id":'+str(payment_id)+'}', 'auth_token': auth_token})
    print book 

def time_til_res(venue_id):
    non_midnight_places = {'1505': 15*60*60, '6194': 14*60*60, '418':14*60*60}
    tomorrow = datetime.now() + timedelta(1)
    midnight = datetime(year=tomorrow.year, month=tomorrow.month, 
                        day=tomorrow.day, hour=0, minute=0, second=0)
    return (midnight - datetime.now()).seconds - non_midnight_places.get(venue_id, 0)

def get_valid_datetimes(day, start_time_interval, end_time_interval):
    valid_datetime_objects = []
    first_datetime = datetime.strptime(day + start_time_interval, '%Y-%m-%d%H:%M:%S')
    last_datetime = datetime.strptime(day + end_time_interval, '%Y-%m-%d%H:%M:%S')
    valid_datetime_objects.append(first_datetime)

    current_datetime = first_datetime
    while current_datetime < last_datetime:
        current_datetime = current_datetime + timedelta(minutes=15)
        valid_datetime_objects.append(current_datetime)
    valid_datetimes = [x.strftime("%Y-%m-%d %H:%M:%S") for x in valid_datetime_objects]
    return valid_datetimes


def get_new_reservation(email, password, day, valid_datetimes, venue_id, party_size):
    user_info = login(email, password)
    auth_token = user_info['token']
    print 'auth_token: ', auth_token
    payment_id = user_info['payment_method_id']
    print 'payment_id: ', payment_id
    print 'sleeping for ', str(time_til_res(venue_id) - 1)
    time.sleep(max(time_til_res(venue_id) - 1, 0 ))
    for i in xrange(20):
        print "attempt to find reservation #", i
        reservations = find_reservations(auth_token, day, party_size, venue_id)
        venues = reservations['results']['venues']
        if venues == []:
            continue
        slots = reservations['results']['venues'][0]['slots']
        if len(slots) != 0:
            valid_slots = []
            for slot in xrange(len(slots)):
                if slots[slot]['date']['start'] in valid_datetimes:
                    valid_slots.append(slot)
            if valid_slots == []:
                print slots
                print [x['date']['start'] for x in slots ]
                print 'no valid reservation available'
                return
            random_reservation = valid_slots[random.choice(valid_slots)]
            #Maybe bug


            config_id = random_reservation['config']['token']
            print 'config_id: ', config_id
            reservation_details = get_reservation_details(auth_token, day, party_size, config_id)
            book_token = reservation_details['book_token']['value']
            book = send_post_request("https://api.resy.com/3/book", {'book_token': book_token, 'struct_payment_method':'{"id":'+str(payment_id)+'}', 'auth_token': auth_token})
            print "booking reply: ", book
            print 'successfully booked reservation at: ', random_reservation['date']['start']
            return

#get_new_reservation('ana.castillo.arauz@gmail.com', 'castillo28','2019-12-12',get_valid_datetimes('2019-12-12','18:00:00','21:00:00'), '6194', 4)



# Aqui hay ejemplos de cada uno de los API calls que se le puede hacer a resy. Estan en el orden que se deberian hacer para conseguir una reserva.
# el ultimo es un miscelaneous que puede servirnos en el futuro

# Login
# response has auth_token & payment_id. For auth_token, response[token]
# print send_post_request("https://api.resy.com/3/auth/password", {'email':'fernandoavarelaf@gmail.com','password':'qweasdzxc'})

# get restaurant reservations available Params: auth_token, venue_id, day, lat, long, party_size
# response has reservation slots available with their corresponding config_id/datetime/etc. For config, response[results][venues][0?][slots][0/1/...][config]
# print send_get_request("https://api.resy.com/4/find", {'auth_token':'ajHGLt1OmhCOsJIAJUctOU84y9sEmYCv_B47eRH9gzLluXIgPyp0LvxP2an6LxuZ9ZVgwvVO9TyJ5z4SdqfvrpJaIBhPdXaAunSMUC7TxJ8=-90d76b789d60921a11fc9d70ff9c170d160631ac467c4afd83cbfe39','day':'2019-09-30','lat':'0','long':'0','party_size':'2','venue_id':'3164'})

# asks for details of a specific res (book token important one to actually reserve) Params: auth_token, day, party_size, config_id
# response has book_token. response[book_token?][value]
# print send_get_request("https://api.resy.com/3/details", {'auth_token':'ajHGLt1OmhCOsJIAJUctOU84y9sEmYCv_B47eRH9gzLluXIgPyp0LvxP2an6LxuZ9ZVgwvVO9TyJ5z4SdqfvrpJaIBhPdXaAunSMUC7TxJ8=-90d76b789d60921a11fc9d70ff9c170d160631ac467c4afd83cbfe39','day':'2019-11-12','party_size':'2','config_id':''})

# books a reservation Params: auth_token, book_token, struct_payment_method, source_id(not necessary)
# response has resy_token, not important?
# print send_post_request("https://api.resy.com/3/book", {'book_token':"DkAFsO4PtBW|9C3zkwPJvifiMRmLaSqsbDoAeSm_BDIn0DTgmf0uLae2ctpkv7ygHORjMC0D_pRouEndPzoZ0Da3eF2gbtCsIvl46iYO_HhsXQ8cLH6366XY0lQcZTIx4Obg0U8ZOVlyN0GOczixGm4sr|_N9aYel4Wc8LkCTtU=-7600935d3b2a0c911d4e67e15cbfee31bacc032726f3cc13472ef74f",'struct_payment_method':'{"id":1416466}','auth_token':'ajHGLt1OmhCOsJIAJUctOU84y9sEmYCv_B47eRH9gzLluXIgPyp0LvxP2an6LxuZ9ZVgwvVO9TyJ5z4SdqfvrpJaIBhPdXaAunSMUC7TxJ8=-90d76b789d60921a11fc9d70ff9c170d160631ac467c4afd83cbfe39'})

# restaurant calendar availability Params: auth_token, venue_id, start_date, end_date, num_seats
# response has which dates are available, not very important
# print send_get_request('https://api.resy.com/3/venue/calendar',  {'auth_token':'ajHGLt1OmhCOsJIAJUctOU84y9sEmYCv_B47eRH9gzLluXIgPyp0LvxP2an6LxuZ9ZVgwvVO9TyJ5z4SdqfvrpJaIBhPdXaAunSMUC7TxJ8=-90d76b789d60921a11fc9d70ff9c170d160631ac467c4afd83cbfe39','start_date':'2019-09-30', 'end_date':'2020-09-30','num_seats':'2','venue_id':'3164'})
# Don angie = 1505, Lilia = 418, 4 charles = 834, I sodi = 443, Atoboy = 587, Rubirosa = 466, tokyo record = 1518, carbone = 6194





