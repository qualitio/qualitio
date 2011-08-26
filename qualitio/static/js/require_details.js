$(document).ready(function() {
  $("table.display.directory-content").dataTable({
    "sScrollY": "160px",
    "bPaginate": false,
    "sDom": 'rt<"bottom clearfix"lfp><"clear">',
    "aoColumnDefs": [
      { "bSortable": false, "aTargets": [0] },
      { "sWidth": "4px", "aTargets": [0,1] }
    ]
  });

  $("table.display:not(.directory-content)").dataTable({
    "sScrollY": "160px",
    "bPaginate": false,
    "bFilter": false,
    "aoColumnDefs": [
      { "bSortable": false, "aTargets": [0] },
      { "sWidth": "4px", "aTargets": [0,1] }
    ]
  });
});
