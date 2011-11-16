$(document).ready(function() {
  $("table.display").dataTable({
    "sScrollY": "230px",
    "bPaginate": false,
    "aoColumnDefs": [
      { "bSortable": false, "aTargets": [0] },
      { "sWidth": "4px", "aTargets": [0,1] }
    ]
  });
});
