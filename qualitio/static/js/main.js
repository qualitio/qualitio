// HashController,
// Implementation based on jquery-ui site, try to understand it, don't blame it.
var hash = {
  storedHash: '',
  listen: true,
  interval: null,
  cache: '',

  object : null,
  node : null,
  view : null,

  _start_listening: function() {
    setTimeout(function() {
      hash.listen = true;
    }, 600);
  },

  _stop_listening: function() {
    hash.listen = false;
  },

  _has_changed: function() {
    var locStr = hash.current_hash();
    if(hash._clean(hash.storedHash) != locStr) {
      hash._parse();

      if(hash.listen == true) {
        hash.main();
        hash.post_main();
      }
      hash.storedHash = locStr;
    }
    if(!hash.interval) hash.interval = setInterval(hash._has_changed, 50);
  },

  _parse: function() {
    segments = hash.current_hash().split("/");
    hash.object = segments[0];
    hash.node = segments[1];
    hash.view = segments[2];
  },

  _clean: function(locStr){
    return locStr.replace(/%23/g, "").replace(/[\?#]+/g, "");
  },

  init: function(){
    if (window.location.hash) {
      hash._parse()
      hash.update();
    } else {
      hash.storedHash = '';
    }
    hash._has_changed();
  },

  update: function(refresh) {
    hash.storedHash = hash.to_string();
    window.location.hash = hash.to_string();
    if (refresh) {
      hash.main();
    }
  },

  current_hash: function() {
    return hash._clean(window.location.hash);
  },

  to_string: function() {
    return "#"+[hash.object, hash.node, hash.view].join("/")+"/";
  },

  // Controller view. Will react on every anchor change. Implement your logic here
  main: function() {
    return alert("One function to rule them all, not implemented")
  },

  post_main: function() {
    return 0;
  }
};

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
