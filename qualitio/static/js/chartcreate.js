$(document).ready(function(){
  var url = "/project/meego/chart/" + CHARTID  + "/chartview/" + document.location.search;

  $("#show-chart").click(function() {
    $(this).attr("href", url);
    return true;
  });
});
