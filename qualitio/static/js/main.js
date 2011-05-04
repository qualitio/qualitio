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

  
jQuery.fn.dataTableToggleSelect = function() {
  return jQuery(this).live('click', function() {
    $(this).parents('.dataTables_wrapper')
      .find('input.modify:not(:disabled)')
      .attr('checked', $(this).attr('checked'));
  });
};

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
      this.directory_type = options.directory;
      this.file_type = options.file;
      
      this.id = document.location.hash.split("/")[1];
      this.type = window.location.hash.split('/')[0].split("#")[1];
      
      var tree_types = {
        "types": {
          "valid_children" : [ this.directory_type ]
        }
      };
      
      tree_types.types[this.directory_type] = {
        "valid_children": "all",
        "icon": {
          "image":  options.directory_icon || "/static/images/tree/directory.png"
        }
      }
      
      if (this.file_type) {
        tree_types.types[this.file_type] = {
          "icon": {
            "image": options.file_icon || "/static/images/tree/file.png"
          }
        }
      }
      
      var self = this;
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
                type: n.attr ? n.attr("rel") : this.directory_type
              };
            }
          }
        },
        "types" : tree_types,
        "plugins" : [ "themes", "json_data", "ui", "cookies","types"]
      }).bind("select_node.jstree", function (node, data) {
        self.id = data.rslt.obj.attr("id").split("_")[0],
        self.type = data.rslt.obj.attr("id").split("_")[1];
        document.location.hash = '#'+ self.type +'/'+ self.id +"/details/";
      });
      $.shortcuts.selectTreeNode(this.id, this.type);
    },

    update: function(type, id, view) {
      this.type = type;
      this.id = id;
      $.shortcuts.selectTreeNode(id, type);
    }
  });
  
});
