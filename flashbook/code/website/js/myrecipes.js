$.ajax({
    url : 'http://flashbook-app.appspot.com/api/user/login',
    dataType : 'json',
    //contentType : 'application/json; charset=UTF-8',
    type : 'POST'
}).done(function(data, textStatus, jqXHR) {
  console.log(data);

}).fail(function(msg) {
    console.log(msg);
});

$.ajax({
    url : 'http://flashbook-app.appspot.com/api/recipe/all',
    dataType : 'json',
    //contentType : 'application/json; charset=UTF-8',
    type : 'GET'
}).done(function(data, textStatus, jqXHR) {
  console.log(data);

}).fail(function(msg) {
    console.log(msg);
});
