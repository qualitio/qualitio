$(function() {
  $('#reportdirectory_form').ajaxForm({ 
    beforeSubmit: $.shortcuts.hideErrors,
    success: function(response) {
      if(!response.success) {
        $.notification.error(response.message);
        $.shortcuts.showErrors(response.data)
      } else {
        $.notification.notice(response.message);
        $.shortcuts.reloadTree(response.data, "reportdirectory");

        $("h1").text("report directory : " + $('#id_name').val());

        $('#application-tree').bind("refresh.jstree", function (event, data) {
          $("#application-tree").jstree("open_node", "#"+data.args[1].parent_id+"_reportdirectory", function() {
            $("#application-tree").jstree("select_node", "#"+data.args[1].current_id+"_reportdirectory");
            $("#application-tree").jstree("deselect_node", "#"+data.args[1].parent_id+"_reportdirectory");
            document.location.hash = '#reportdirectory/'+ data.args[1].current_id +"/edit/";
          });
        });
      }
    },
  });
});
