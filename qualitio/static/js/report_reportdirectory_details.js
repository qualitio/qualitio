$(document).ready(function() {
  $("table.display").dataTable({
    "sScrollY": "330px",
    "bPaginate": false,
    "sDom": 'rt<"bottom clearfix"lfp><"clear">',
    "sWidth": "4px", "aTargets": [0],
    "aoColumnDefs": [ { "sWidth": "4px", "aTargets": [0] } ]
  });
});
