$(function() {
  $('input[type=submit], .button').button();

  $("label").inFieldLabels();
  $("input").attr("autocomplete","off");
})

$(window).resize(function(){
  $("label").inFieldLabels();
});
