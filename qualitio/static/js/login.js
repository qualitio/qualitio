$(function() {
  $('input[type=submit]').button();
  
  $("label").inFieldLabels(); 
  $("input").attr("autocomplete","off");
})
