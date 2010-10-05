function render_application_view(node_id, view) {
    $('#application-view').load("/require/ajax/requirement/"+node_id+"/"+view+"/");
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
    render_application_tree(hash.node);
    render_application_menu(hash.node, hash.view);
    render_application_view(hash.node, hash.view);
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
