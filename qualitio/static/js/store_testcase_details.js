$(function() {
  $(".glossary-language-switch").languageSwitcher();

  $('input[value=Clone]').click(function() {
    jQuery.get('ajax/testcase/' + $(this).attr('name') + '/copy/', function(response){
      $.notification.notice(response.message);
      $.shortcuts.reloadTree(response.data, "testcasedirectory", "testcase", response.data.current_id);
    });
  });
});
