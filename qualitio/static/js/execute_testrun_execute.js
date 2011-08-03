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

  // We will toggle checkbox in the first table-td element,
  // if the element or the checkbox were clicked.
  var shouldToggleCheckbox = function(clickedElement) {
    var result = false;
    $('#testcaserun-list tbody tr').each(function(index, trRow){
      var firstTd = $('td:first', $(trRow))[0];
      var checkbox = $('td:first input[type="checkbox"]', $(trRow))[0];
      if (clickedElement === firstTd || clickedElement === checkbox) {
        result = true;
      }
    });
    return result;
  }

  $("#testcaserun-list tbody tr:not(.dataTables_empty_row)").click(function(event) {
    if (shouldToggleCheckbox(event.target)) {
      var checkbox = $('td:first input[type="checkbox"]', event.target);
      checked.attr('checked', ! checkbox.attr('checked'));
      return false;
    }

    // remove selection from other selected row
    $("#testcaserun-list tbody tr").removeClass('selected');

    $(this).addClass('selected');
    var testcaserun_id = $(this).attr("id").split("_")[1];
    $("#testcaserun-details").load( $(this).attr("href") );
  });

  // items selection
  $("table.display th.checkbox:first").itemsSelector({
      selector: "table.display td .modify"
  });
  $(".dataTables_scrollHead").css('overflow', 'visible');

  $(".glossary-language-switch").languageSwitcher();
});
