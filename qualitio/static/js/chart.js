$(document).ready(function() {
  var chartid = $("#id_chart");
  var button = $(".create-chart");

  var buildLink = function() {
    button.attr("href", "/project/meego/chart/" + chartid.val() + "/");
  };

  chartid.change(buildLink);
  buildLink();
});
