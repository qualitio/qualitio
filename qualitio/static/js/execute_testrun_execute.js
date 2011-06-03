$(function() {
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

  // items selection
  $("table.display th.checkbox:first").itemsSelector({
      selector: "table.display td .modify"
  });
  $(".dataTables_scrollHead").css('overflow', 'visible');
  
  $(".glossary-language-switch").languageSwitcher();
});
