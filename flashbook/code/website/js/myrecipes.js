$.ajax({
    url : 'http://flashbook-app.appspot.com/api/user/login',
    dataType : 'json',
    //contentType : 'application/json; charset=UTF-8',
    type : 'POST'
}).done(function(data, textStatus, jqXHR) {
  alert(data);

}).fail(function(msg) {
    console.log(msg);
});


