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
  var booking_condition = {};
  var book = {} ;
  booking_condition = {
        type: "flight",
        origin: $('#recipe-origin').val(),
        destination:$('#recipe-destination').val(),
        booking_start_date: $('#dater-from').val() + "T00:00:00.00001Z",
        booking_end_date: $('#dater-to').val()+ "T00:00:00.00001Z",
        max_price:$('#recipe-price').val(),
        min_duration:$('#dater-duration').val().split(",")[0],
        max_duration:$('#dater-duration').val().split(",")[1],
        number_of_connections:2,
        max_flight_duration:40,
        number_of_adult_tickets:1
    }
  book = {
    title: "",
    booking_condition: booking_condition
  }
  console.log(book);
  $.ajax({
        url : 'http://flashbook-app.appspot.com/api/recipe/all',
        dataType : 'json',
        contentType : 'application/json; charset=UTF-8',
        type : 'POST',
        data : JSON.stringify(book)
    }).done(function(data, textStatus, jqXHR) {
        console.log(data);
        setTimeout(function(){
            window.location = "http://flashbook-app.appspot.com/my_recipes.html";
        }, 2000);
        
    }).fail(function(msg) {
       console.log(msg);
       setTimeout(function(){
            window.location = "http://flashbook-app.appspot.com/my_recipes.html";
        }, 2000);
    });
    
   
  }