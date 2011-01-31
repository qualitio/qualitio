function render_application_view(object, node_id, view) {
  $('#application-view').load("/require/ajax/"+object+"/"+node_id+"/"+view+"/");
}

hash.main = function() {
  object_plain_id = hash.node.split("_")[0];
  render_application_view(hash.object, object_plain_id, hash.view);
}

$(function() {
  $("#application-tree").jstree({
    "plugins" : [ "themes", "json_data", "ui", "cookies", "types"],
    "json_data" : {
      "ajax" : {
	"url" : "/require/ajax/get_children", // TODO: custom place in tree
	"data" : function (n) {
	  return { 
            id : n.attr ? n.attr("id").split("_")[0] : 0,
            type: n.attr ? n.attr("rel") : "requirement" // TODO: custom place in tree
          };
	}
      }
    },
    "types" : {
      "valid_children" : ["requirement"], // TODO: custom place in tree
      "types" : {
        "requirement" : {
          "icon" : {
            "image" : "/static/images/requirement_icon_small.png" // TODO: custom place in tree
          }
        }
      }
    }
  }).bind("select_node.jstree", function (node, data) {
    hash.object = data.rslt.obj.attr('rel');
    hash.node = data.rslt.obj.attr("id").split("_")[0];
    if (!hash.view || hash.view == 'new')
      hash.view = 'details';
    hash.update(true);
  }).bind("loaded.jstree", function (event, data) {
    if(!window.location.hash)
      $("#application-tree").jstree("select_node",".jstree-last");
  });

  hash.init();
});
