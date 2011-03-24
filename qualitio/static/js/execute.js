$(function() {
  
  var ApplicationTree = Backbone.View.extend({
    el: $('#application-tree'),

    initialize: function() {
      $(this.el).jstree({
        "ui" : {
	  "select_limit" : 1
        },
        "json_data" : {
          "ajax" : {
            "url" : "ajax/get_children",
            "data" : function (n) {
              return {
                id : n.attr ? n.attr("id").split("_")[0] : 0, //get only the id from {id}_{type_name}
                type: n.attr ? n.attr("rel") : "testrundirectory"
              };
            }
          }
        },
        "types" : {
          "valid_children" : [ "testrundirectory"],
          "types" : {
            "testrundirectory" : {
              "valid_children" : "all"
            },
            "testrun" : {
              "icon" : {
                "image" : "/static/images/file.png"
              },
            }
          }
        },
        "plugins" : [ "themes", "json_data", "ui", "cookies","types"]
      }).bind("select_node.jstree", function (node, data) {
        id = data.rslt.obj.attr("id").split("_")[0],
        type = data.rslt.obj.attr("id").split("_")[1];
        
        _id = document.location.hash.split("/")[1];
        _type = window.location.hash.split('/')[0].split("#")[1];
        _view = document.location.hash.split("/")[2];
        
        if ( !(_type == type) || !(_id == id) || (_view == 'new') || (_view == 'newtestrun') ){
          document.location.hash = '#'+ type +'/'+ id +"/details/";
        }
      });
    },

    update: function(type, id, view) {
      // $(this.el).jstree("select_node","#"+ id +"_"+ type, true);
      // console.log( $(this.el).jstree("_is_loaded", "#"+ id +"_"+ type));
      // jQuery.getJSON("/execute/ajax/get_antecedents", {type:type,
      // id:id});
      // if( !$("#"+ id +"_"+ type).length) {
      //   alert('nie widać');
      //   jQuery.getJSON("/execute/ajax/get_antecedents", {type:type, id:id}, function(data) {
      //     // console.log(data);
      //     $.each(data.nodes, function(i, node) {
      //       // console.log( "1_testrundirectory", node, "1_testrundirectory" == node)
      //       $("#application-tree").jstree("open_node", "#"+ node, function() {
      //         $(this.el).jstree("select_node","#"+ id +"_"+ type, true);
      //       });
      //       // $("#application-tree").jstree("open_node", "#"+ node);
      //       // console.log('$("#application-tree").jstree("open_node", "#'+ node +'")');
      //     });
      //   });
      // } else {
      //   $(this.el).jstree("select_node","#"+ id +"_"+ type, true)
      // }
      if ( !$(this.el).jstree("is_selected", "#"+ id +"_"+ type) ) {
      //   // console.log( $("#"+ id +"_"+ type) );
      //   console.log("test");
      //   console.log( $("#"+ id +"_"+ type).css("display") );
        $(this.el).jstree("select_node","#"+ id +"_"+ type, true);
      }
    }
  });

  var ApplicationView = Backbone.View.extend({
    el: $('#application-view'),
    
    render: function(type, id, view) {
      $(this.el).load("/execute/ajax/"+type+"/"+id+"/"+view+"/", function() {
        $(this).removeClass('disable');
      }).addClass('disable');
    }
  });
  
  var ControllerView = Backbone.Controller.extend({
    
    routes: {
      ":type/:id/:view/": "render",
    },

    initialize: function() {
      this.application_view = new ApplicationView();
      this.application_tree = new ApplicationTree();
    },
    
    render: function(type, id, view) {
      this.application_tree.update(type, id, view);
      this.application_view.render(type, id, view);
    },
    
  });
  
  new ControllerView();
  Backbone.history.start();
  
});
