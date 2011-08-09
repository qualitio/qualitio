$(function(){
  $("#tabs").tabs({
    spinner: 'Retrieving data...',
    cookie: { expires: 30 }
  }).height($("#tabs").parent().height());

});
