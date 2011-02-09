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

$(document).ajaxComplete(function() {
  $("input[type=submit], .button").button();
  $("table.data").dataTable({
    "bFilter": true,
    "sScrollY": "270px",
    "sDom": 'rt<"bottom clearfix"lfp><"clear">'
  });
  $(".date-field").datepicker({
    showWeek: true ,
    dateFormat: DATE_FORMAT
  });
});

