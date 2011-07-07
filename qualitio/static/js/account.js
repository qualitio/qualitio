$(window).resize(function() {
  $('#account .panel').css('height',
                          document.body.clientHeight - $('#header').height() - 25 - 2*$('#footer').height());
});

$(function() {
  $(window).resize();
})

