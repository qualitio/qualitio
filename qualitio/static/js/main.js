var resize_main_window = function() {
  $('#application-view')
    .css('height', 
         document.body.clientHeight - $('#header').height() - 5 - 2*$('#footer').height());
  $('#application-tree')
    .css('height', 
         document.body.clientHeight - $('#header').height() - 25 - 2*$('#footer').height());
};

$(document).ready(function() {
  $('#notification').jnotifyInizialize({
    oneAtTime: true
  });

  resize_main_window();
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
      field = element[0]; message = element[1];
      
      $field = $('#id_'+ field);
      $field_errors = $('#id_' +field+ '_error');
      
      if( $field_errors.length ) {
        $field_errors.text(message).fadeIn();
      } else {
        $field.before($('<div style="display:block" class="error">'+message+'</div>').fadeIn());
      }
    });
  },
  
  hideErrors: function() {
    $('.error').hide();
  },

  reloadTree: function(data, directory_type, target_type) {
    if (!target_type) {
      target_type = directory_type;
    }
    $('#application-tree').jstree('refresh', "#"+data.parent_id+"_"+directory_type, data);
  },
  
  _openNode: function(nodes, target) {
    if (node = nodes.shift()) {
      $('#application-tree').jstree("open_node", "#"+node, function() {
        jQuery.shortcuts._openNode(nodes, target);
      }, true)
    } else {
      $('#application-tree').jstree("select_node", "#"+target, true);
    }
  },

  selectTreeNode: function(id, type) {
    if ( !$('#application-tree').jstree("is_selected", "#"+id+"_"+type) && id) {
      jQuery.getJSON('ajax/get_antecedents', {'id': id, 'type': type}, function(data) {
        jQuery.shortcuts._openNode(data.nodes, data.target);
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
      $(this.el).load("/"+this.application_name+"/ajax/"+type+"/"+id+"/"+view+"/", function() {
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
	  "select_limit" : 1
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
      });
      $.shortcuts.selectTreeNode(this.id, this.type);

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
      this.type = type;
      this.id = id;
      $.shortcuts.selectTreeNode(id, type);
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

    this.each(function(){
      tables.push($(this).originDataTable(setting));
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
    $(this).load("/glossary/ajax/language_switch/", function() {
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

