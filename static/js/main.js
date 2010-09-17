// HashController,
// Implementation based on jquery-ui site, try to understand it, don't blame it.

var hash = {
    storedHash: '',
    listen: true,
    interval: null,
    cache: '',
    
    init: function(){
	hash.storedHash = '';
	hash.checkHashChange();
    },
    
    checkHashChange: function() {
	var locStr = hash.currHash();
	if(hash.storedHash != locStr) {
	    if(hash.listen == true) hash.refreshToHash(); ////update was made by back button
	    hash.storedHash = locStr;
	}
	
	if(!hash.interval) hash.interval = setInterval(hash.checkHashChange, 100);
	
    },

    refreshToHash: function(locStr) {
	if(locStr) var newHash = true;
	locStr = locStr || hash.currHash();

	// Need better url anchor parser
	node_id = hash.currHash().split('/')[1];
	
	// Update details area 
	$('#requirement-details').load('/requirements/ajax/requirement/'+node_id+'/', function(e) {
	    $("#tabs").tabs();
	});

	// Update tree area
	jQuery.jstree._reference("#requirement-tree").select_node( 'li#'+node_id, true);
	
	// if the hash is passed
	// if(newHash){ hash.updateHash(locStr, true); }
    },

    updateHash: function(locStr, ignore) {
	console.log("test");
	if(ignore == true){ hash.stopListening(); }
	window.location.hash = locStr;
	if(bookmarklet){ window.parent.location.hash = locStr; }
	if(ignore == true){ 
	    hash.storedHash = locStr; 
	    hash.startListening();
	}
    },

    clean: function(locStr){
	return locStr.replace(/%23/g, "").replace(/[\?#]+/g, "");
    },
    
    currHash: function() {
	return hash.clean(window.location.hash);
    },
};




$(function () {
    $("#requirement-tree").jstree({
	"plugins" : [ "themes", "json_data", "ui", "cookies" ],
	"json_data" : {
	    "ajax" : {
		"url" : "/requirements/ajax/get_children/",
		"data" : function (n) { 
		    return { id : n.attr ? n.attr("id") : 0 };
		}
	    }
	}
    }).bind("select_node.jstree", function (node, data) {
	node_id = data.rslt.obj.attr('id');
	document.location.hash = "requirement/"+node_id;
    });
});

$(function() {
    hash.init();
});
