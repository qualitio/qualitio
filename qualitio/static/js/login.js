$(function() {
  $('input[type=submit], .button').button();
  
  $("label").inFieldLabels(); 
  $("input").attr("autocomplete","off");
})
