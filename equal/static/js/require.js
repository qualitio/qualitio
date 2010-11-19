function render_application_view(node_id, view) {
  $('#application-view').load("/require/ajax/requirement/"+node_id+"/"+view+"/", function() {
    $("input[type=submit], .button").button();
    
    // $("#application-tree").height($("#application-view").parent().height()-10);
    // $("#application-tree").parent().height($("#application-view").parent().height());

    // $("#application-tree").parent().resizable("option", "minHeight", $("#application-view").parent().height());
  });
}

function render_application_tree(node_id) {
    // jQuery.jstree._reference("#requirement-tree").select_node( 'li#'+node_id, true);
}

function render_application_menu(node_id, view) {
    $('#application-view-menu').load("/require/ajax/requirement/"+node_id+"/menu/", function() {
	$('#application-view-menu .'+view).css('font-weight', 'bold')
    });
}

hash.object = "requirement";
hash.node = 1;
hash.view = "details";

// One function to rule them all
hash.main = function() {
  object_plain_id = hash.node.split("_")[0];
  render_application_view(hash.object, object_plain_id, hash.view);
    // render_application_tree(hash.node);
    // render_application_menu(hash.node, hash.view);
    // render_application_view(hash.node, hash.view);
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
    hash.update();
  });

  $('.switch-testcase-add-view').live('click', function() {
    $('.testcase-add-view').toggle();
  });
  
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
