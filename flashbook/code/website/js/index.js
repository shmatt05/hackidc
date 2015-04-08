//Author: Chris Mills, Dec. 2014

// Description: Some "Material Design" compliant/inspired assets for use as a reference

// Notes: This project was my first real stab at implementing a stylesheet with SCSS and Compass Mixins, along with my first attempt to replicate some of the stylistic traits of Google's Material Design / Polymer appearance, for use in a few little projects I'm working on

// I'm also learning jQuery/JS, so this is my first real use of JS to augment user interaction.


// Browser Compatibility Breakdown:
// Due to the use of the vh unit and calc, the layout will breakdown for IE versions lower than 9, Safari lower than 7, and Android Browser earlier than 4.4 if your .navItems exceed the number that can be displayed onscreen at one time, requiring the .navbar element to become scrollable, if you are in the "full" layout mode. I may tinker with this a bit to try to improve browser compatibility in the future.

//Credits:
// Colors and terminology derived from the Material Design spec sheet (http://www.google.com/design/spec/style/color.html#color-color-palette), along with Demos for Polymer (https://www.polymer-project.org)

// Full credit for the design concepts and styles given to Google Inc and the Polymer authors. If code was unintentionally recreated or replicated, the Polymer license is included below.

// Apart from areas specifically credited (inline) to particular individuals, implementation of the style is the work of the author.

// Copyright (c) 2014 The Polymer Authors. All rights reserved.
//
// Redistribution and use in source and binary forms, with or without
// modification, are permitted provided that the following conditions are
// met:
//
//    * Redistributions of source code must retain the above copyright
// notice, this list of conditions and the following disclaimer.
//    * Redistributions in binary form must reproduce the above
// copyright notice, this list of conditions and the following disclaimer
// in the documentation and/or other materials provided with the
// distribution.
//    * Neither the name of Google Inc. nor the names of its
// contributors may be used to endorse or promote products derived from
// this software without specific prior written permission.
//
// THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
// "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
// LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
// A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
// OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
// SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
// LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
// DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
// THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
// (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
// OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

/* JS BEGINS */

$(document).ready(function() {
  
  // Store the pixel width of the breakpoint
  var $breakpointWidth = $('.breakpointTarget').width();
  // Stored variable to help "us" remember whether or not we've directly changed the title of the screen at the small breakpoint - when we pull the coreToolbar in, we will actively replace the "drawerTitle" with the "appTitle" to let our users know what app they're using when they navigate its menus.
  var $titleState = 0;
  
  // Determine if the .overlay selector exists, if it does, remove it, if not, append it to the body
  var overlayHandle = function() {
    if($('.overlay').length) {
      $('.overlay').remove();
      $('body').css('overflow', 'visible');
    } else {
     $('body').append('<div class="overlay"></div>');
     $('body').css('overflow', 'hidden');
    }
  }
  
  var titleChange = function() {
    $('.drawerTitle').toggle();
    $('.appTitle').toggle();
    $titleState = 1;
    
    if($titleState = 1){
      $titleState = 0;
    }
  }
  
  var titleCleanup = function() {
    if($titleState = 0){  
    } else {
      $('.drawerTitle').toggle();
      $('.appTitle').toggle();
      $titleState = 0;
    }
  }
  
  // If the window is resized to make the slide-over nav unnecessary while the it is open, toggle the drawer dim off and close the nav back to the docked position
  $(window).resize(function() {
    if($('.nav').hasClass('expandNav')) {
      $('.nav').toggleClass('expandNav');
      overlayHandle();
      titleCleanup();
      
      if($(window).width() > $breakpointWidth) {
        titleCleanup();
        // Remove any of the stuff we added inline if we resize the window above our breakpoint (Solution thanks to: http://stackoverflow.com/questions/17623003/media-queries-not-working-properly-after-javascript-alters-element-css for media breakpoints not functioning correctly after these fancy toggles)
        $('.drawerTitle').attr('style', '');
        $('.appTitle').attr('style', '');
      }
    }
  });
  
  $('#drawerToggle').click(function(){
    $('.nav').toggleClass('expandNav');
    overlayHandle();
    titleChange();
  });
  
  $('body').click(function(e) {
    if($('.nav').hasClass('expandNav')) {
      // We have to prevent the Toggle from triggering twice when we click on the toggle element, because it is not part of .nav
      if (!$(this).is(e.target) && !$('#drawerToggle').is(e.target)) {
        $('.nav').toggleClass('expandNav');
        overlayHandle();
        titleCleanup();
      }
    }
  });
  
});



 
    