function load_testcaserun() {
  
}

$(function() {
  $("#testcaserun-list").parent().resizable({
    alsoResize: "#testcaserun-list",
    handles: 's',
    maxHeight : $('#testcaserun-list table').height() + 50
  });
  
  $("#testcaserun-list tr.row").hover(
    function() {
      $(this).addClass("hover");
    },
    function() {
      $(this).removeClass("hover");
    }
  );

  $("#testcaserun-list tr.row").click(function() {
    testcaserun_id = $(this).attr("id").split("_")[1];
    $("#testcaserun-details").load("/execute/ajax/testcaserun/"+testcaserun_id+"/");
  });
  

  // TODO: this part of file should be considered as part related to
  // different view
  $("#testcaserun-status-form").live('change', function() {
    $('#testcaserun-status-form').ajaxForm({
      success: update_status,
    });
    $('#testcaserun-status-form').submit();
  });
});

function update_status(status) {
  $("#testcaserun_" + status.data.id+" .status").text(status.data.name);
  $("#testcaserun_" + status.data.id).css("background", status.data.color);
}
