$(function() {
  
  jQuery.fn.passrate = function (method, value) {
    
    if (method==="update") {
      return jQuery(this)
        .find(".value").text(value+' %').end()
        .find(".passed").css('width', value+"%").end()
        .find(".failed").css('width', (100 - value)+"%").end();
    }
    
    passrate = parseInt(jQuery(this).text(), 10);
    
    return jQuery(this)
      .text("")
      .addClass("passrate")
      .append('<div class="value">'+ passrate +' %</div>')
      .append('<div class="element passed"/>')
      .append('<div class="element failed"/>')
      .find(".passed").css('width', passrate+"%").end()
      .find(".failed").css('width', (100 - passrate)+"%").end();
  }
  

  var ControllerView = Backbone.Controller.extend({
    
    routes: {
      ":type/:id/:view/": "render",
    },

    initialize: function() {
      this.application_view = new ApplicationView("execute");
      this.application_tree = new ApplicationTree({"directory": "testrundirectory",
                                                   "file": "testrun"});
    },
    
    render: function(type, id, view) {
      this.application_tree.update(type, id, view);
      this.application_view.render(type, id, view);
    },
    
  });
  
  new ControllerView();
  Backbone.history.start();
});
