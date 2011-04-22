var resize_tree = function() {
  $("#application-tree").parent().resizable({
    handles: 'e',
    maxWidth: document.width/2,
    ghost: true,
    stop: function(event, ui) { 
      $('#application-view').parent().width(document.body.clientWidth - $(this).width());
    }
  });
};

$(document).ready(function() {
  resize_tree();
});

$(window).resize(function() {
  $('#application-view').parent()
    .width(document.body.clientWidth - $('#application-tree').parent().width());
  resize_tree();
});

