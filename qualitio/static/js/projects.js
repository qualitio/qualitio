$(window).resize(function() {
  $('#projects .panel').css('height',
                            document.body.clientHeight - $('#header').height() - $('#projects .header').height() - 35);
});

$(function() {
  $(window).resize();

  $(".project-add-button")
    .button({
      icons: {
        primary: "ui-icon-circle-plus"
      },
      text: false
    });

  $('#project_form').ajaxForm({
    success: function(response) {
      if(!response.success) {
        $.notification.error(response.message);
        $.shortcuts.showErrors(response.data)
      } else {
        $.notification.notice(response.message);
        document.location = response.data.url;
      }
    },
    beforeSubmit: function() {
      $.shortcuts.hideErrors();
    }
  });
})

