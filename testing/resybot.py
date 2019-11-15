

class Booking:
	def __init__(self, name, age):
    	self.name = name
    	self.age = age

    	#Don angie = 1505, Lilia = 418, 4 charles = 834, I sodi = 443, Atoboy = 587, Rubirosa = 466, tokyo record = 1518
    	self.days_from_today = {"1505" : 29, "418" : 30, "834" : 30, "443" : 45, "587" : 10, "3015" :30, "466" : 45, "1518" : 30}

    	#VbWk7s3L4KiK5fzlO7JD3Q5EYolJI7n5 -> mismo pa todos parece. esta en un JS file en el website: https://resy.com/scripts/main-a65754f769.js
    	self.api_key = "VbWk7s3L4KiK5fzlO7JD3Q5EYolJI7n5"


import requests
def send_get_request(resy_url, params):
	r = requests.get(url = resy_url, params = params) 
	data = r.json()
	print data






var users = Map("andrew" -> "UWDavVer0DOrqDzuZsFwpl%7CVDn2gd5x5S63o9vVSBCbaaSHWmR0UyZPiGxoII75jURB9UmaUlfqlr1XBnbhNiOxiwZvik3SNGWj_h6fP1xs%3D-b8e81ab7c50dd48e1965682f935e2ffe66ac374098fd34c1a870cced", 
    "emily" -> "pxeCjmEQk%7CYtoywsw39JlA5ZVEMLz3hclbr0On%7ChvZSYOcSd0AUcn342qpnuqocWXm_R8tTRJ9D487_drD1btMMhlCalTrCZODS32r_0aAw%3D-0851b677784ef4fed7ca990927568559bd24e00e2f00aa7226a1e9d9", 
    "vicky" -> "u7WfBZ5S3UMBFjwDHBEvV4KNXCxiBkSwJmoNJflr36IiGg0SoIHtscLRRCDHKYFxLTyq1yTxaik6KsnGbOR6kF6O0Ec3dYarPGw1lKco7Yw%3D-a1132a63aca3baeb2ac56636a63d9b006305605dbf6006b989b80bf5",
    "alex" -> "C9mxcABpGlt8BAfLutc93LQZUCIh9EtD2Zq1V4rn0WI6aXuaKj6tD%7Ci5wr7WrO5QN0eFp0PMecQh935T%7CCEq_QSVcJ0tYcO%7CLze5fSMMEvM%3D-cced3ff478a59c16c913293129f62e3eb51a45616431409c49bb3973")
  var auth_token = "y1htwuEtHPsJu13Li8PB7kn53toteSXYw8EhOJHq7gNk6PSrJCy6cgTvfjJQr5QQ7b5bYYIyIYskoyjJpHPoDjK8DmSBbpyjoOCWwkQScvc%3D-4c118b57b4ad527e5dbb6a0705dc2b5fa15e3122d33db3315c5cade3"
  //Your user profile API key
  //
  var api_key = "VbWk7s3L4KiK5fzlO7JD3Q5EYolJI7n5"
  //RestaurantId where you want to make the reservation
  // Don angie = 1505, Lilia = 418, 4 charles = 834, I sodi = 443, Atoboy = 587, Rubirosa = 466, tokyo record = 1518
  var venueId = ""
  //YYYY-MM-DD of reservation
  var days_from_today = Map("1505" -> 29, "418" -> 30, "834" -> 30, "443" -> 45, "587" -> 10, "3015" ->30, "466" -> 45, "1518" -> 30)
  var day = ""
  //HH:MM:SS time of reservation in military time format
  var time = List(s""""2019-06-16 18:30:00"""",s""""2019-06-16 18:45:00"""",s""""2019-06-16 19:00:00"""",s""""19:15:00"""",s""""2019-06-16 19:30:00"""",s""""19:45:00"""",s""""20:00:00"""",s""""20:15:00"""",s""""20:30:00"""",s""""20:45:00"""",s""""21:00:00"""")
  //Size of party
  var partySize = "4"