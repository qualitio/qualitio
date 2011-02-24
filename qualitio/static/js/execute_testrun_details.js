$(document).ready(function() {
  $("table.display").dataTable({
    "sScrollY": "230px",
    "bPaginate": false,
    "sDom": 'rt<"bottom clearfix"lfp><"clear">',
    "sWidth": "4px", "aTargets": [0]
  });
});
