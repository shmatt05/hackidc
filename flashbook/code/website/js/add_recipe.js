$(function () {
    $(".recipe-autocomplete").autocomplete({
      source: function (request, response) {
        $.ajax({
          url: "http://api.sandbox.amadeus.com/v1.2/airports/autocomplete",
          dataType: "json",
          data: {
            apikey: "nzPtUZtGWpnYAkC1NGGlNQxjCTMyPVfs",
            term: request.term
          },
          success: function (data) {
            response(data);
          }
        });
      },
      minLength: 1,
      select: function (event, ui) {
        var $url = 'images/' + $(event.target.parentElement).find('input').val().toLowerCase() + '.jpg';
        $(event.target.parentElement).css('background-image', 'url(' + $url + ')').addClass('selected');
        $(event.target).blur();
      },
      open: function () {
        $(this).removeClass("ui-corner-all").addClass("ui-corner-top");
      },
      close: function () {
        $(this).removeClass("ui-corner-top").addClass("ui-corner-all");
      }
    }).focus(function() {

      $(this).val('').parent().removeClass('selected').css('background-image', '');

    });
  });
  
  function Book() {
  alert("asd");
  }
  
  function login_data() {
                $.ajax({
                    url : 'http://flashbook-app.appspot.com/api/user/login',
                    dataType : 'json',
                    //contentType : 'application/json; charset=UTF-8',
                    type : 'POST'
                }).done(function(data, textStatus, jqXHR) {
                  console.log(data);
                  
                  $(".user").append("Hello " + data.response.authenticated_user.name); 

                }).fail(function(msg) {
                    console.log(msg);
                    return false;
                });
            }