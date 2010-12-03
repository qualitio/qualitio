function render_application_view(object, node_id, view) {
  $('#application-view').load("/require/ajax/"+object+"/"+node_id+"/"+view+"/");
}

function render_application_tree(node_id) {
  // jQuery.jstree._reference("#requirement-tree").select_node( 'li#'+node_id, true);
}

hash.main = function() {
  object_plain_id = hash.node.split("_")[0];
  render_application_view(hash.object, object_plain_id, hash.view);
}

$(function() {
  $("#application-tree").jstree({
    "plugins" : [ "themes", "json_data", "ui", "cookies" ],
    "json_data" : {
      "ajax" : {
	"url" : "/require/ajax/get_children/",
	"data" : function (n) {
	  return { id : n.attr ? n.attr("id") : 0 };
	}
      }
    }
  }).bind("select_node.jstree", function (node, data) {
    $("#application-tree").jstree("open_node","li#"+data.rslt.obj.attr("id"));
    hash.object = 'requirement';
    hash.node = data.rslt.obj.attr('id');
    if (!hash.view)
      hash.view = 'details';
    hash.update();
  }).bind("loaded.jstree", function (event, data) {
    $("#application-tree").jstree("select_node",".jstree-last");
  });

  hash.init();
});
