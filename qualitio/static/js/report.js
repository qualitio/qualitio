$(function() {
  var ControllerView = Backbone.Controller.extend({
    
    routes: {
      ":type/:id/:view/": "render",
    },

    initialize: function() {
      this.application_view = new ApplicationView("report");
      this.application_tree = new ApplicationTree({"directory": "reportedirectory",
                                                   "file": "report"});
    },
    
    render: function(type, id, view) {
      this.application_tree.update(type, id, view);
      this.application_view.render(type, id, view);
    },
    
  });
  
  new ControllerView();
  Backbone.history.start();
});
