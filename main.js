function getCookie(cname) {
    var name = cname + "=";
    var decodedCookie = decodeURIComponent(document.cookie);
    var ca = decodedCookie.split(';');
    for(var i = 0; i <ca.length; i++) {
        var c = ca[i];
        while (c.charAt(0) == ' ') {
            c = c.substring(1);
        }
        if (c.indexOf(name) == 0) {
            return c.substring(name.length, c.length);
        }
    }
    return "";
};

function swap(json){
  var ret = {};
  for(var key in json){
    ret[json[key]] = key;
  }
  return ret;
}

var rest_to_id = {'Blanca': '5994','Misi': '3015','Wayan': '4599','Don Angie' : '1505', 'Lilia' : '418', '4 Charles' : '834', 'I Sodi' : '443', 'Atoboy' : '587', 'Rubirosa' : '466', 'Tokyo Record' : '1518', 'Carbone' : '6194'}
var id_to_rest = swap(rest_to_id)

$( document ).ready(function() {
    if(getCookie('user')){
        login_nav = $("#login_nav");
        login_nav.attr("href", "my_requests.html");
        login_nav.text("My Account")
    }
});