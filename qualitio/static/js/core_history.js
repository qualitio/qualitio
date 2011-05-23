$(document).ready(function() {
  $("table.display").dataTable({
    "sScrollY": "300px",
    "aaSorting": [[ 0, "desc" ]],
    "sDom": 'rt<"bottom clearfix"lfp><"clear">',
    "aoColumnDefs": [ { "sWidth": "130px", "aTargets": [0] },
                      { "sWidth": "130px", "aTargets": [1] }]
  });
});
