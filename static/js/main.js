// HashController,
// Implementation based on jquery-ui site, try to understand it, don't blame it.
var hash = {
    storedHash: '',
    listen: true,
    interval: null,
    cache: '',

    object : null, 
    node : null,
    view : null,

    _start_listening: function() {
	setTimeout(function() {
	    hash.listen = true;
	}, 600);
    },
    
    _stop_listening: function() {
	hash.listen = false;
    },

    _has_changed: function() {
	var locStr = hash.current_hash();
	if(hash.storedHash != locStr) {
	    hash._parse();

	    if(hash.listen == true) {
		hash.main();
	    }
	    hash.storedHash = locStr;
	}
	if(!hash.interval) hash.interval = setInterval(hash._has_changed, 50);
    },

    _parse: function() {
	segments = hash.current_hash().split("/");
	hash.object = segments[0];
	hash.node = segments[1];
	hash.view = segments[2];
    },
    
    _clean: function(locStr){
	return locStr.replace(/%23/g, "").replace(/[\?#]+/g, "");
    },

    init: function(){
	hash.storedHash = '';
	hash.update();
	hash._has_changed();
    },
    
    update: function() {
	hash.storedHash = hash.to_string();
	window.location.hash = hash.to_string();
    },
    
    current_hash: function() {
	return hash._clean(window.location.hash);
    },
    
    to_string: function() {
	return "#"+[hash.object, hash.node, hash.view].join("/");
    },
    
    // Controller view. Will react on every anchor change. Implement your logic here
    main: function() {
	update_tree(hash.node);
	render_application_view(hash.node, hash.view);
    }
};

function render_application_view(node_id, view) {
    $('#application-view').load("/ajax/requirement/"+node_id+"/"+view+"/");
}

function update_tree(node_id) {
    // jQuery.jstree._reference("#requirement-tree").select_node( 'li#'+node_id, true);
}

$(function() {
    
    $("#tabs").tabs({});

    $("#application-tree").jstree({
	"plugins" : [ "themes", "json_data", "ui", "cookies" ],
	"json_data" : {
	    "ajax" : {
		"url" : "/ajax/get_children/",
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

    hash.object = "requirement";
    hash.node = 1;
    hash.view = "details";
    hash.init();
    
});



// $(function() {
    
    
//     // $("form input[type=submit]").live("click", function(){
//     // 	$('form').ajaxForm({
//     // 	    success: function() {
//     // 		jQuery.jstree._reference("#requirement-tree").refresh(-1); 
//     //         }
//     // 	})
//     // });
    

//     // $("#messages").position({
//     // 	my: "left top",
//     // 	at: "left top",
//     // 	of: "body",
//     // 	offset: "10"
	
//     // })
    
//     // $("#messages").click(function() {
//     // 	$(this).hide( "blind", 1000 );
//     // });
    
// });
