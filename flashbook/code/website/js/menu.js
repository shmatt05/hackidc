function login_data() {
                $.ajax({
                    url : 'http://flashbook-app.appspot.com/api/user/login',
                    dataType : 'json',
                    //contentType : 'application/json; charset=UTF-8',
                    type : 'POST'
                }).done(function(data, textStatus, jqXHR) {
                  console.log(data);
                  
                  $(".user").text("Hello " + data.response.authenticated_user.name); 

                }).fail(function(msg) {
                    console.log(msg);
                    return false;
                });
            }
            
nav = "" ;
nav += '<h1><a href="index.html">Flashbook</a></h1>' ;
nav += '<nav id="nav">' ;
nav += '<ul>' ;
nav += '<li class="special">' ;
nav += '<a href="#" class="menuToggle"><span>Menu</span></a>' ;
nav += '<div id="menu">' ;
nav += '<p id="user-name" class="user" ></p>' ;
nav += '<ul>' ;
nav += '<li><a href="index.html">Home</a></li>' ;
nav += '<li><a href="add_recipe.html">Add a recipe</a></li>' ;
nav += '<li><a href="my_recipes.html">My recipes</a></li>' ;
nav += '<li><a href="#">Sign Out</a></li>' ;
nav += '</ul>' ;
nav += '</div>' ;
nav += '</li>' ;
nav += '</ul>' ;
nav += '</nav>' ;
$("#header").append(nav);

footer = "";
footer += '<ul class="icons">';
footer += '<li><a href="#" class="icon fa-twitter"><span class="label">Twitter</span></a></li>';
footer += '<li><a href="#" class="icon fa-facebook"><span class="label">Facebook</span></a></li>';
footer += '<li><a href="#" class="icon fa-instagram"><span class="label">Instagram</span></a></li>';
footer += '<li><a href="#" class="icon fa-dribbble"><span class="label">Dribbble</span></a></li>';
footer += '<li><a href="mailto:aripro@gmail.com" class="icon fa-envelope-o"><span class="label">Email</span></a></li>';
footer += '</ul>';

$("#footer").append(footer);

login_data();
