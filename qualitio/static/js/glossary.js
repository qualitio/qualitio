$(function() {
  $(".word-add-button")
    .button({
      icons: {
        primary: "ui-icon-circle-plus"
      },
      text: false
    })
    .click( function () {
      document.location.href = "#word/new/";
    });

  var ControllerView = Backbone.Controller.extend({
    view_el: $('#application-view'),
    list_el: $('#application-tree'),

    routes: {
      "word/:id/edit/": "edit",
      "word/new/": "new",
    },

    initialize: function() {
      $(this.list_el).load("/project/" + PROJECT_SLUG + "/glossary/ajax/word/list/", function() {
        $(".word-search input")
          .focus()
          .livefilter({selector:'#application-tree a'});
      });
    },

    edit: function(id) {
      $(this.view_el).load("/project/" + PROJECT_SLUG + "/glossary/ajax/word/"+id+"/edit/", function() {
        $(this).removeClass('disable');
      }).addClass('disable');
    },

    new: function() {
      $(this.view_el).load("/project/" + PROJECT_SLUG + "/glossary/ajax/word/new/", function() {
        $(this).removeClass('disable');
      }).addClass('disable');
    }

  });

  new ControllerView();
  Backbone.history.start();
  
});
