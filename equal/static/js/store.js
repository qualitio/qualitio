function render_application_view(type, node, view) {
  $('#application-view').load("/store/ajax/"+type+"/"+node+"/"+view+"/");
}

hash.main = function() {
  object_plain_id = hash.node.split("_")[0]
  render_application_view(hash.object, object_plain_id, hash.view);
}

$(function() {
  $("#application-tree").jstree({
    "plugins" : [ "themes", "json_data", "ui", "cookies","types"],
    "json_data" : {
      "ajax" : {
        "url" : "ajax/get_children",
        "data" : function (n) {
          return {
            id : n.attr ? n.attr("id").split("_")[0] : 0, //get only the id from {id}_{type_name}
            type: n.attr ? n.attr("rel") : "testcasedirectory"
          };
        }
      }
    },
    "types" : {
      "valid_children" : [ "testcasedirectory"],

      "types" : {
        "testcasedirectory" : {
          "valid_children" : "all"
        },
        "testcase" : {
          "icon" : {
            "image" : "/static/images/file.png"
          },
        }
      }
    }
  }).bind("select_node.jstree", function (node, data) {
    hash.object = data.rslt.obj.attr('rel');
    hash.node = data.rslt.obj.attr("id").split("_")[0];
    hash.views = "details";
    hash.update();
  });

  hash._parse();
  if(!hash.object) {
    hash.object = "testcasedirectory";
    if(!hash.node) {
      hash.node = 1;
      if(!hash.view) {
        hash.view = "details";
      }
    }
  }
  hash.init();

  $("#application-tree").parent().resizable({
    alsoResize: '#application-tree',
    resize: function(event, ui) {
      percent = $(this).width()/$(this).offsetParent().width()*100;
      neighbor = $('#application-view').parent();
      neighbor.css("width", 100-percent+"%");
    },
    maxWidth: document.width/2
  });

});
