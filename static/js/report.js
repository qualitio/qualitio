function render_application_menu(type, node, view) {
    $('#application-view-menu').load("/report/ajax/"+type+"/"+node+"/"+view+"/menu/");
}

function render_application_view(type, node, view) {
    $('#application-view').load("/report/ajax/"+type+"/"+node+"/"+view+"/");
}

hash.main = function() {
    object_plain_id = hash.node.split("_")[0]

    render_application_menu(hash.object, object_plain_id, hash.view);
    render_application_view(hash.object, object_plain_id, hash.view);
    // render_application_tree(hash.node);
}

$(function() {
    $("#application-tree").jstree({
	"plugins" : [ "themes", "json_data", "ui", "cookies","types"],
	"json_data" : {
	    "ajax" : {
		"url" : "/report/ajax/get_children/",
		"data" : function (n) {
		    return {
			id : n.attr ? n.attr("id").split("_")[0] : 0, //get only the id from {id}_{type_name}
			type: n.attr ? n.attr("rel") : 'reportdirectory'
		    };
		}
	    }
	},
	"types" : {
	    "max_depth" : -2,
	    "max_children" : -2,
	    "valid_children" : [ "reportdirectory"],
	    "types" : {
		"reportdirectory" : {
	            "valid_children" : [ "directory", "file" ],
	        },
	        "report" : {
		    "valid_children" : ["none"],
		    "icon" : {
	                "image" : "/static/images/file.png"
	            },
		}
	    }
	}
    }).bind("select_node.jstree", function (node, data) {
	hash.object = data.rslt.obj.attr('rel');
	hash.node = data.rslt.obj.attr("id").split("_")[0];
	hash.update();
    });


    hash.object = "reportdirectory";
    hash.node = 1;
    hash.view = "details";

    hash.init();
});
