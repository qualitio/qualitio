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
        document.location.href = '#' + data.rslt.obj.attr('rel') +'/'+ data.rslt.obj.attr("id").split("_")[0] + "/details/";
      });
    },

    update: function(type, id, view) {
      if ( !$(this.el).jstree("is_selected", "#"+ id +"_"+ type) ) {
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
  
  var ExecuteController = Backbone.Controller.extend({
    
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
  
  new ExecuteController();
  Backbone.history.start();
  
});
