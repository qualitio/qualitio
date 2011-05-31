jQuery.fn.bugTable = function() {
  return $(this).dataTable({
    "bStateSave": true,
    "sScrollY": "150px",
    "bFilter": false,
    "bInfo": false,
    "bPaginate": false,
    "aoColumnDefs": [
      { "bSortable": false, "aTargets": [0],
        "sWidth": "4px", "aTargets": [0,1]}
    ]
  });
};

jQuery.fn.loadBugs = function(testcaserun) {
  $(this).load('/execute/ajax/testcaserun/'+ testcaserun +'/bugs/', function() {
    $(this).find('table.display').bugTable();
      $("table.testcaserun-bugs-list th.checkbox:first", $(this)).itemsSelector({
	selector: "table.testcaserun-bugs-list td input[type='checkbox']"
    });
    $(".dataTables_scrollHead", $(this)).css('overflow', 'visible');
  });
};
jQuery.fn.reloadBugs = jQuery.fn.loadBugs


$(function() {
  $('#testcaserun-status-form').buttonset();
  $("#testcaserun-details table.display").bugTable();
  $('#current-bugs-table').loadBugs(TESTCASERUN);
  
  $("#testcaserun-status-form").change(function() {
    $(this).ajaxForm({
      success: function(status) {
        $("#testcaserun_" + status.data.id+" .status").text(status.data.name);
        $("#testcaserun_" + status.data.id).css("background", status.data.color);
        
        $(".passrate .element").remove();
        $(".passrate .value").text(status.data.passrate.toFixed(1)+" %");
        $.each(status.data.passrate_ratio, function(i, status) {
          $('<div class="element '+ status.name +'  "/>').appendTo('.passrate')
            .css('width', status.ratio +"%")
            .css('background', status.color);
        });
      },
    }).submit();
  });
  
  $("#testcaserun-add-bug-form input[type=submit]").live('click', function() {
    $('#testcaserun-add-bug-form').ajaxForm({
      beforeSubmit : function() {
        $("#testcaserun-add-bug-form input").addClass("disable");
      },
      success: function(response) {
        $("#testcaserun-add-bug-form input").removeClass("disable");
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
          // Update testcaserunlist
          $("#testcaserun_"+response.data.testcaserun+" .bugs").text(
            $.map(response.data.all_bugs, function(value) { return "#"+value }).join(" ")
          );
          // Reload bugtable
          $('#current-bugs-table').reloadBugs(TESTCASERUN);
          
          $('#notification').jnotifyAddMessage({
            text: response.message,
            permanent: false,
            disappearTime: 2000
          });
        }
      }
    });
  });
                                           

  $("#testcaserun-remove-bug-form input[type=submit]").die('click');
  $("#testcaserun-remove-bug-form input[type=submit]").live('click', function() {
    $('#testcaserun-remove-bug-form').ajaxForm({
      success: function(response) {
        if(!response.success) {
          $('#notification').jnotifyAddMessage({
            text: response.message,
            permanent: false,
            type: "error"
          });
        } else {
          // Reload bugtable
          $('#current-bugs-table').reloadBugs(TESTCASERUN);
          
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
