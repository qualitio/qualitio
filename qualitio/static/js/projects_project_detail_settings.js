$(function(){

  // $('.delete input').button({
  //   icons: {
  //     primary: "ui-icon-circle-close"
  //   },
  //   text: false
  // });

  $('#project_settings').ajaxForm({
    success: function(response) {
      $("#tabs").tabs("load", 1);
    }
  });

});

