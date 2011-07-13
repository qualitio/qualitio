jQuery.fn.refresh = function () {
  _this = $(this).find("table");

  _this.find("tr")
    .removeClass("disable")
    .find("input")
    .attr("disabled", false);

  $(".connected-testcases table").find("input[name=connected_test_case]").each( function(i, el) {
    origin_tr_element = _this.find("input[name=available_test_case][value="+ $(this).val() +"]").parents("tr");
    origin_tr_element
      .addClass("disable")
      .find("input")
      .attr("disabled", true)
      .attr("checked", false);
  });

  $(this).find("input[name=select-all]").attr("checked", false);
}

var connected_testcases = null;
$(function() {

  connected_testcases = $(".connected-testcases table.display").dataTable({
    "sScrollY": "300px",
    "bPaginate": false,
    "bFilter": false,
    "sDom": 'rt<"bottom clearfix"lfp><"clear">',
    "aoColumnDefs": [
      { "bSortable": false, "aTargets": [0],
        "sWidth": "4px", "aTargets": [0, 1]}
    ]
  });
  $("#remove-testcases-button").appendTo($(".connected-testcases .bottom"));

  var available_testcases = $(".available-testcases table.display").dataTable({
    "sScrollY": "300px",
    "bPaginate": false,
    "sDom": 'rt<"bottom clearfix"lfp><"clear">',
    "aoColumnDefs": [
      { "bSortable": false, "aTargets": [0],
        "sWidth": "4px", "aTargets": [0, 1]}
    ]
  });
  $("#add-testcases-button").appendTo($(".available-testcases .bottom"));

  $(".available-testcases").refresh();


  $("#remove-testcases-button").click(function() {
    $(".connected-testcases input.modify:checked").each( function(i) {
      var pos = connected_testcases.fnGetPosition( $(this).parents('tr')[0] );
      connected_testcases.fnDeleteRow(pos);
    });
    $(".connected-testcases input[name=select-all]").attr("checked", false);
    $(".available-testcases").refresh();
  });


  $("#add-testcases-button").click( function() {
    $(".available-testcases input.modify:checked").each( function() {
      parent_tr = $(this).parents("tr");

      control_box = parent_tr.find('.select').clone();
      control_box.find('input[name=available_test_case]').attr("name", "connected_test_case");

      connected_testcases.fnAddData([control_box.html(),
                                     parent_tr.find('.id').html(),
                                     parent_tr.find('.path').html(),
                                     parent_tr.find('.name').html(),
                                     ""]);
    });
    $(".available-testcases").refresh();
  });


  // items selection
  $(".connected-testcases table.display th.checkbox:first").itemsSelector({
      selector: ".connected-testcases table.display td .modify"
  });
  $(".available-testcases table.display th.checkbox:first").itemsSelector({
      selector: ".available-testcases table.display td .modify"
  });
  $(".dataTables_scrollHead").css('overflow', 'visible');

  $('#testrun_form').ajaxForm({
    success: function(response) {
      if(!response.success) {
        $.notification.error(response.message);
        $.shortcuts.showErrors(response.data)
      } else {
        $("h1").text("test run: " + $('#id_name').val());
        $.notification.notice(response.message);
        $.shortcuts.reloadTree(response.data, "testrundirectory", "testrun", response.data.current_id);
      }
    },
    beforeSubmit: function() {
      $.shortcuts.hideErrors();
    }
  });
});
