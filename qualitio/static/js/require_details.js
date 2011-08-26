$(document).ready(function() {
  $("table.display").dataTable({
    "sScrollY": "160px",
    "bPaginate": false,
    "bFilter": false,
    "aoColumnDefs": [
      { "bSortable": false, "aTargets": [0] },
      { "sWidth": "4px", "aTargets": [0,1] }
    ]
  });
});
