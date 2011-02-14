function load_testcaserun() {
  
}

$(function() {
  // $("#testcaserun-list").parent().resizable({
  //   alsoResize: "#testcaserun-list",
  //   handles: 's',
  //   maxHeight : $('#testcaserun-list table').height() + 50
  // });

  $("table.display").dataTable({
    "sScrollY": "200px",
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
  

  // TODO: this part of file should be considered as part related to
  // different view
  $("#testcaserun-status-form").live('change', function() {
    $('#testcaserun-status-form').ajaxForm({
      success: update_status,
    });
    $('#testcaserun-status-form').submit();
  });
  
  // TODO: Remove this die() clear
  $("#testcaserun-add-bug-form input[type=submit]").die('click');
  $("#testcaserun-add-bug-form input[type=submit]").live('click', function() {
    $('#testcaserun-add-bug-form').ajaxForm({
      success: function(response) {
        $("#testcaserun-add-bug-form .field-wrapper").removeClass('ui-state-error');
        $("#testcaserun-add-bug-form .field-wrapper  .error").text("");
        if(!response.success) {
          $(response.data).each(function(i, element) {
            $("#"+element[0]+"_wrapper").addClass("ui-state-error");
            $("#"+element[0]+"_wrapper .error").append(element[1]);
          });        
          $('#notification').jnotifyAddMessage({
            text: response.message,
            permanent: false,
            type: "error"
          });
        } else {
          $('#notification').jnotifyAddMessage({
            text: response.message,
            permanent: false,
            disappearTime: 2000
          });
        }
      }
    });
  });
});

function update_status(status) {
  $("#testcaserun_" + status.data.id+" .status").text(status.data.name);
  $("#testcaserun_" + status.data.id).css("background", status.data.color);
}

function update_bug(response, $form, options) {
  
}
