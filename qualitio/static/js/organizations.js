$(window).resize(function() {
  $('#projects .panel').css('height',
                            document.body.clientHeight - $('#header').height() - $('#projects .header').height() - 35);
});

$(function() {
  $(window).resize();
  $('.button').button();

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

$(document).ready(function() {
  $('#articles').css('display', 'none');

  $('#faq_control').click(function() {
    if ($('#faq').css('display') == 'none') {
      $('#faq').css('display', 'block');
      $('#faq_control').text('hide FAQ');
    } else {
      $('#faq').css('display', 'none');
      $('#faq_control').text('show FAQ');
    }
  });
  
  $('#articles_control').click(function() {
    if ($('#articles').css('display') == 'none') {
      $('#articles').css('display', 'block');
      $('#articles_control').text('hide articles');
    } else {
      $('#articles').css('display', 'none');
      $('#articles_control').text('show articles');
    }
  });

});
