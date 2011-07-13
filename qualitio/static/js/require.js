$(function() {
  var ControllerView = Backbone.Controller.extend({

    routes: {
      ":type/:id/:view/": "render",
    },

    initialize: function() {
      this.application_view = new ApplicationView("require");
      this.application_tree = new ApplicationTree({"directory": "requirement",
                                                   "directory_icon": "/static/images/tree/requirement.png"});
    },

    render: function(type, id, view) {
      this.application_tree.update(type, id, view);
      this.application_view.render(type, id, view);
      $.shortcuts.selectTreeNode(id, type);
    },

  });

  new ControllerView();
  Backbone.history.start();
});
