$(document).ready( function() {
  $("#application-tree").parent().resizable({
    alsoResize: '#application-tree',
    resize: function(event, ui) {
      percent = $(this).width()/$(this).offsetParent().width()*100;
      neighbor = $('#application-view').parent();
      neighbor.css("width", 100-percent+"%");
    },
    maxWidth: document.width/2
  });
});

$(document).ajaxComplete(function() {
  $("input[type=submit], .button").button();
  $("#application-tree").height($("#application-view").parent().height()-10);
  $("#application-tree").parent().height($("#application-view").parent().height());
  $("#application-tree").parent().resizable( "option", "minHeight", $("#application-view").parent().height());
});
