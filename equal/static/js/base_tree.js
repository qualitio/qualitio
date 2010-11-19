function post_update() {
  $("input[type=submit], .button").button();
  $("#application-tree").height($("#application-view").parent().height()-10);
  $("#application-tree").parent().height($("#application-view").parent().height());
  $("#application-tree").parent().resizable( "option", "minHeight", $("#application-view").parent().height());
}
