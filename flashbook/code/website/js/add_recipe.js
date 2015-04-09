(function($){
  $(".background").on("click", function(){
    	$(this).toggleClass("active");
    if ( $('div.tab_data',this).is(":visible") === true ) {
$('div.tab_data',this).fadeOut(100);
$('i.fa',this).delay(150).fadeIn(100);
} else {
$('div.tab_data',this).delay(150).fadeIn(100);
$('i.fa',this).fadeOut(100);

  
}
    	
  });
 
})(jQuery);