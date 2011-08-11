/* Simple jQuery wrapper on code that checks for browser refresh.
 * Based on code founded in:
 *     http://www.tedpavlic.com/post_detect_refresh_with_javascript.php
 */
(function($) {
    // By default, turn refresh detection on
    var refresh_prepare = 1;
    var functions = [];
    var turnedOn = false;

    var indexOf = function(array, elem) {
	for (i = 0; i < array.length; i++) {
	    if (array[i] === elem)
		return i;
	}
	return -1;
    };

    $.onrefresh = {
	bind: function(fun) {
	    if (fun) {
		functions.push(fun);
	    }
	},
	unbind: function(fun) {
	    functions = functions.splice(indexOf(functions, fun), 1);
	},
	unbindAll: function() {
	    functions = [];
	},
	reset: function() {
	    // The next page will look like a refresh but it actually
	    // won't be, so turn refresh detection off.
	    refresh_prepare = 0;

	    // Also return true so this can be placed in onSubmits
	    // without fear of any problems.
	    return true;
	},
	turnOn: function() {
	    if (! turnedOn) {
		$(window).load(checkRefresh);
		$(window).unload(prepareForRefresh);
		turnedOn = true;
	    }
	},
	turnOff: function() {
	    if (turnedOn) {
		$(window).unbind('load', checkRefresh);
		$(window).unbind('unload', prepareForRefresh);
		turnedOn = false;
	    }
	}
    };

    var checkRefresh = function() {
	// Get the time now and convert to UTC seconds
	var today = new Date();
	var now = today.getUTCSeconds();

	// Get the cookie
	var cookie = document.cookie;
	var cookieArray = cookie.split('; ');

	// Parse the cookies: get the stored time
	for(var loop=0; loop < cookieArray.length; loop++) {
	    var nameValue = cookieArray[loop].split('=');

	    // Get the cookie time stamp
	    if( nameValue[0].toString() == 'SHTS' ) {
		var cookieTime = parseInt( nameValue[1] );
	    }
	    // Get the cookie page
	    else if( nameValue[0].toString() == 'SHTSP' ) {
		var cookieName = nameValue[1];
	    }
	}

	if (cookieName &&
	    cookieTime &&
	    cookieName == escape(location.href) &&
	    Math.abs(now - cookieTime) < 5 ) {
	    // Refresh detected

	    for (i = 0; i < functions.length; i++) {
		functions[i]();
	    }

	    // If you would like to toggle so this refresh code
	    // is executed on every OTHER refresh, then
	    // uncomment the following line
	    // refresh_prepare = 0;
	}

	// You may want to add code in an else here special
	// for fresh page loads
    };

    var prepareForRefresh = function() {
	if (refresh_prepare > 0) {
	    // Turn refresh detection on so that if this
	    // page gets quickly loaded, we know it's a refresh
	    var today = new Date();
	    var now = today.getUTCSeconds();
	    document.cookie = 'SHTS=' + now + ';';
	    document.cookie = 'SHTSP=' + escape(location.href) + ';';
	} else {
	    // Refresh detection has been disabled
	    document.cookie = 'SHTS=;';
	    document.cookie = 'SHTSP=;';
	}
    };

    $.onrefresh.turnOn();
})(jQuery);
