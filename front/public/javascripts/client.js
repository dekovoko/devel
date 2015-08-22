$(document).ready(function () {

  $("#login").click(function(){
    $("fieldset#signin_menu").toggle();
    $("#login").toggleClass("menu-open");
  })

  $("#login_close").click(function(){
    $("fieldset#signin_menu").hide();
  });

});
