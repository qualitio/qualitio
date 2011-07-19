$(document).ready(function() {
  $("table.display").dataTable({
    "sScrollY": "330px",
    "bPaginate": false,
    "sDom": 'rt<"bottom clearfix"lfp><"clear">',
    "sWidth": "4px", "aTargets": [0],
    "aoColumnDefs": [ { "sWidth": "4px", "aTargets": [0] } ]
  });

  $("table.display.testcaserun-list th.checkbox:first").itemsSelector({
      selector: "table.display.testcaserun-list td .modify"
  });
  $(".dataTables_scrollHead").css('overflow', 'visible');

  $('input[value=Clone]').click(function() {
    jQuery.get('ajax/testrun/' + $(this).attr('name') + '/copy/', function(response){
      $.notification.notice(response.message);
      $.shortcuts.reloadTree(response.data, "testrundirectory", "testrun", response.data.current_id);
    });
  });

});
