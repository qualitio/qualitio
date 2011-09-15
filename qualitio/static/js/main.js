var resize_main_window = function() {
  $('#application-view')
    .css('height',
         document.body.clientHeight - $('#header').height() - 69);
  $('#application-tree')
    .css('height',
         document.body.clientHeight - $('#header').height() - 90);
};

$(document).ready(function() {
  $('#notification').jnotifyInizialize({
    oneAtTime: true
  });

  resize_main_window();


  $(function () {
    $(".reports-menu").live({
      mouseenter: function(){
        $(".reports-menu .position").show();
      },
      mouseleave: function() {
        $(".reports-menu .position").hide();
      }
    });
  });

});

$(window).resize(function() {
  resize_main_window();
});

(function( $ ){
  $.fn.serializeJSON=function() {
    var json = {};
    jQuery.map($(this).serializeArray(), function(n, i){
      json[n['name']] = n['value'];
    });
    return json;
  };
})( jQuery );

jQuery.shortcuts = {
  showErrors: function(errors) {
    $(errors).each(function(i, element, value) {
      var field = element[0], message = element[1];

      var $field = $('#id_'+ field);
      var $field_errors = $('#id_' +field+ '_error');
      var parentIsRemoved = $field.parents('.removed').length > 0;

      if (! parentIsRemoved) {  // we don't want to validate removed / deleted items
	if( $field_errors.length ) {
          $field_errors.text(message).fadeIn();
	} else {
          $field.before($('<div style="display:block" class="error">'+message+'</div>').fadeIn());
	}
      }
    });
  },

  hideErrors: function() {
    $('.error').hide();
  },

  reloadTree: function(data, directory_type, target_type, object_id) {
    if (!target_type) {
      target_type = directory_type;
    }

    $('#application-tree').jstree('refresh', -1, data);

    $('#application-tree').bind("refresh.jstree", function (event, data) {
      $('#application-tree').jstree('deselect_all');
      $.shortcuts.selectTreeNode(data.args[1].current_id, target_type);
      document.location.hash = '#' + target_type + '/' + data.args[1].current_id +"/edit/";
    });

  },

  _openNode: function(nodes, target) {
    if (nodes.length) {
      var node = nodes.shift()
      if ( !$.jstree._reference("#application-tree").is_open("#"+node)) {
        $.jstree._reference("#application-tree").open_node("#"+node, function() {
          jQuery.shortcuts._openNode(nodes, target);
        });
      } else {
        jQuery.shortcuts._openNode(nodes, target);
      }
    } else {
      $.jstree._reference("#application-tree").select_node("#"+target, true)
    }
  },

  selectTreeNode: function(id, type) {
    if ( !$('#application-tree').jstree("is_selected", "#"+id+"_"+type) && id) {
      $.ajax({
        url: 'ajax/get_antecedents',
        dataType: 'json',
        data: {'id': id, 'type': type},
        async:   false,
        success: function(data) {
          jQuery.shortcuts._openNode(data.nodes, data.target);
          $.jstree._reference("#application-tree").select_node("#"+data.target, true)
        }
      });
    }
  }
}

jQuery.notification = {

  element: '#notification',

  notice: function(message) {
    $(this.element).jnotifyAddMessage({
      text: message,
      permanent: false,
      disappearTime: 2000
    });
  },

  error: function(message) {
    $(this.element).jnotifyAddMessage({
      text: message,
      permanent: true,
      type: "error"
    });
  },

  hide: function() {
    $('.jnotify-item-wrapper').remove()
  }
}

$(document).ajaxComplete(function() {
  $("input[type=submit], .button").button();
  $(".date-field").datepicker({
    showWeek: true ,
    dateFormat: DATE_FORMAT
  });
});

$(function() {

  ApplicationView = Backbone.View.extend({
    el: $('#application-view'),

    initialize: function(application_name) {
      this.application_name = application_name;
    },

    render: function(type, id, view) {
      $(this.el).load("/project/"+PROJECT_SLUG+"/"+this.application_name+"/ajax/"+type+"/"+id+"/"+view+"/", function() {
        $(this).removeClass('disable');
      }).addClass('disable');
    }
  });

  ApplicationTree = Backbone.View.extend({
    el: $('#application-tree'),

    initialize: function(options) {
      var self = this;

      self.directory_type = options.directory;
      self.file_type = options.file;

      self.id = window.location.hash.split("/")[1];
      self.type = window.location.hash.split('/')[0].split("#")[1];
      self.view = window.location.hash.split('/')[2]


      var tree_types = {
        "types": {
          "valid_children" : [ self.directory_type ]
        }
      };

      tree_types.types[self.directory_type] = {
        "valid_children": "all",
        "icon": {
          "image":  options.directory_icon || "/static/images/tree/directory.png"
        }
      }

      if (self.file_type) {
        tree_types.types[self.file_type] = {
          "icon": {
            "image": options.file_icon || "/static/images/tree/file.png"
          }
        }
      }

      $(this.el).jstree({
        "ui" : {
          "select_limit" : 1,
          "initially_select" : [ self.id +  "_" + self.type ]
        },
        "json_data" : {
          "ajax" : {
            "url" : "ajax/get_children",
            "data" : function (n) {
              return {
                id : n.attr ? n.attr("id").split("_")[0] : 0, //get only the id from {id}_{type_name}
                type: n.attr ? n.attr("rel") : self.directory_type,
              };
            }
          }
        },
        "types" : tree_types,
        "themes" : {
          "url": MEDIA_URL + "js/themes/default/style.css",
        },
        "plugins" : [ "themes", "json_data", "ui", "cookies","types"]
      }).bind("loaded.jstree", function (event, data) {
        $.shortcuts.selectTreeNode(self.id, self.type);
      });
    },

    events: {
      "click #application-tree a":          "open_event",
    },

    open_event: function(e) {
      this.open($(e.target).parents('li:first'));

    },

    open: function(target) {
      id = target.attr("id").split("_")[0];
      type = target.attr("id").split("_")[1];
      document.location.hash = '#'+ type +'/'+ id +"/details/";
    },

    update: function(type, id, view) {
      self.type = type;
      self.id = id;
      $.shortcuts.selectTreeNode(self.id, self.type);
    }
  });

});


/* This jQuery plugin allows to take control over
 * the creation event of dataTables plugin. Basically
 * we need this response with table's draw function
 * on windows resize.
 */
(function($){
  $.fn.originDataTable = $.fn.dataTable;

  $.fn.dataTable = function(setting){
    var tables = [];
    var defaults = {
      "sDom": 'rt<"bottom clearfix"ilfp><"clear">'
    };
    var opts = $.extend(defaults, setting);

    this.each(function(){
      tables.push($(this).originDataTable(opts));
    });

    var onResize = function(){
      $.each(tables, function(index, table){ table.fnDraw(); });
    };

    $(window).resize(onResize);

    // if it is a tree view bind the event.
    // we don't need it if the filter view is load.
    if ($.onTreeResize) {
      $.onTreeResize(onResize);
    }

    return tables.length > 0 ? tables[0] : null;
  }
})(jQuery);

(function($){
  $.fn.languageSwitcher = function() {
    $(this).load("/project/" + PROJECT_SLUG + "/glossary/ajax/language_switch/", function() {
      $(this).appendTo("#application-view-menu");
      $(this).find('form').change( function() {
      $(this).submit();
      })
        .ajaxForm({
          success: function(response) {
            $.notification.notice(response.message);
            Backbone.history.loadUrl();
          },
        });
    });
  }
})(jQuery);


/* This little snipplet below make sure that "chose"
 * plugin for select box behaviours as expected
 */
(function($){
  function onResize() {
    $('.chzn-container').css('width', '100%');
    $('.chzn-drop').css('width', '100%');
    $('.chzn-drop').width($('.chzn-drop').width() - 2);
  }

  $.fn.originChosen = $.fn.chosen;
  $.fn.chosen = function(settings) {
    var toReturn = $(this).originChosen(settings);
    $(window).unbind('resize', onResize);
    $(window).resize(onResize);
    onResize();
    return toReturn;
  }
})(jQuery);
