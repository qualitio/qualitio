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

  // let's sign empty "tr" elements with "dataTables_empty_row" class.
  // That because we do not want to add "hover" to "tr" with
  // "No data available in table" banner.
  $("#testcaserun-list tbody tr td.dataTables_empty").parent().each(function(){
    $(this).addClass("dataTables_empty_row");
  });

  $("#testcaserun-list tbody tr:not(.dataTables_empty_row)").hover(
    function() { $(this).addClass("hover"); },
    function() { $(this).removeClass("hover"); }
  );

  $("#testcaserun-list tbody tr:not(.dataTables_empty_row)").click(function() {
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
