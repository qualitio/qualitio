$(function() {
  // $("#testcaserun-list").parent().resizable({
  //   alsoResize: "#testcaserun-list",
  //   handles: 's',
  //   maxHeight : $('#testcaserun-list table').height() + 50
  // });
  
  $("table.display").dataTable({
    "sScrollY": "200px",
    "bPaginate": false,
    "sDom": 'rt<"bottom clearfix"lfp><"clear">',
    "aoColumnDefs": [
      { "bSortable": false, "aTargets": [0],
        "sWidth": "4px", "aTargets": [0,1]}
    ]
  });

  $("#testcaserun-list tbody tr").hover(
    function() {
      $(this).addClass("hover");
    },
    function() {
      $(this).removeClass("hover");
    }
  );

  $("#testcaserun-list tbody tr").click(function() {
    $("#testcaserun-list tbody tr").removeClass('selected');
    $(this).addClass('selected');
    testcaserun_id = $(this).attr("id").split("_")[1];
    $("#testcaserun-details").load("/execute/ajax/testcaserun/"+testcaserun_id+"/");
  });
});
