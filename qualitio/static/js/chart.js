/* This file contains all of needed functions in chart wizzard views: */
/* ATTENTION: "simple.inheritance.js" file should be include *before* this file */

/* Utils */
var URLFor = (function () {

  var addQuestionMark = function (params) {
    var p = (params || "");
    if ( ! /^\?/.test(p) && p !== "")
      p = "?" + p;
    return p;
  }

  var baseUrl = function (opts) {
    return "/project/" + opts.projectSlug + "/chart/";
  }

  return {
    dummy: function (opts) {
      return "#";
    },

    /* Requires:
     * - opts.projectSlug,
     */
    chartTypeView: function(opts) {
      return baseUrl(opts);
    },

    /* Requires:
     * - opts.projectSlug,
     */
    chart: function(opts) {
      return baseUrl(opts);
    },

    /* Requires:
     * - opts.projectSlug,
     * - opts.chartid,
     * - opts.searchParams
     */
    xAxisView: function(opts) {
      return baseUrl(opts) + "filter/X/" + opts.chartid  + "/" + addQuestionMark(opts.searchParams);
    },

    /* Requires:
     * - opts.projectSlug,
     * - opts.chartid,
     * - opts.searchParams
     */
    yAxisView: function(opts) {
      return baseUrl(opts) + "filter/Y/" + opts.chartid  + "/" + addQuestionMark(opts.searchParams);
    },

    /* Requires:
     * - opts.projectSlug,
     * - opts.id,          // the id of saved chart query
     * - opts.searchParams
     */
    savedXAxisView: function(opts) {
      return baseUrl(opts) + "saved/" + opts.id + "/filter/" + addQuestionMark(opts.searchParams);
    },

    /* Requires:
     * - opts.projectSlug,
     * - opts.chartid,
     * - opts.searchParams
     */
    chartView: function(opts) {
      return baseUrl(opts) + "view/" + opts.chartid  + "/" + addQuestionMark(opts.searchParams);
    },

    /* Requires:
     * - opts.projectSlug,
     * - opts.id,          // the id of saved chart query
     * - opts.searchParams
     */
    savedChartView: function(opts) {
      return baseUrl(opts) + "saved/" + opts.id  + "/" + addQuestionMark(opts.searchParams);
    },

    /* This is a ajax view for open-flash-chart flash plugin.
     *  Requires:
     * - opts.projectSlug,
     * - opts.chartid,
     * - opts.searchParams,
     */
    chartdata: function(opts) {
      return baseUrl(opts) + "data/" + opts.chartid  + "/" + addQuestionMark(opts.searchParams);
    },

    /* Requires:
     * - opts.projectSlug,
     * - opts.id
     */
    deleteChart: function (opts) {
      return baseUrl(opts) + "ajax/delete/" + opts.id + "/";
    },

    /* Requires:
     * - opts.projectSlug,
     */
    newChart: function (opts) {
      return baseUrl(opts) + "new/";
    },

    /* Requires:
     * - opts.projectSlug,
     */
    chartList: function (opts) {
      return baseUrl(opts) + "ajax/list/";
    }
  }
})();


var Base = Class.extend({
  init: function (opts) {
    this.opts = opts;
  },

  buildParams: function(others) {
    return $.extend({
      searchParams: document.location.search
    }, this.opts, others || {});
  },

  bind: function () {}
});


var BaseWizzard = Base.extend({
  init: function (opts) {
    this._super(opts);
    this.nextButtonClickEvent = (function(that) {
      return function () {
	$('.next-button').attr('href', that.nextUrl());
      }
    })(this);
  },

  nextUrl: function () {
    return URLFor.dummy(this.buildParams());
  },

  backUrl: function () {
    return URLFor.dummy(this.buildParams());
  },

  bindNextButton: function () {
    $('.next-button').click(this.nextButtonClickEvent);
    this.nextButtonClickEvent();
  },

  bindBackButton: function () {
    $('.back-button').attr("href", this.backUrl());
  },

  bind: function () {
    this.bindNextButton();
    this.bindBackButton();
  }
});


/* ChoosingChartTypeView requires following env variables:
 * - opts.projectSlug
 *
 * Usage:
 *
 * var view = new ChoosingChartTypeView({ projectSlug: PROJECT_SLUG });
 * view.bind();
 */
var ChoosingChartTypeView = BaseWizzard.extend({
  init: function (opts) {
    this._super(opts);
    this.chartIDSelect = $('#id_chart');
  },

  buildParams: function (others) {
    return $.extend({
      chartid: this.chartIDSelect.val()
    }, this._super(), others || {});
  },

  bindBackButton: function () {},

  nextUrl: function () {
    return URLFor.xAxisView(this.buildParams());
  }
});


var ChartBaseView = Base.extend({
  init: function (opts) {
    this._super(opts);
    this.deleteChartEvent = (function (that) {
      return function () {
	return that.deleteChart($(this).attr('id'));
      }
    })(this);
  },

  deleteChart: function (id) {
    var that = this;
    var data = {
      csrfmiddlewaretoken: $('input[name="csrfmiddlewaretoken"]').val()
    };

    $.post(URLFor.deleteChart(that.buildParams({ id: id })), data, function(response) {
      if (!response.success) {
        $.notification.error(response.message);
        $.shortcuts.showErrors(response.data)
      } else {
        $.notification.notice(response.message);
	document.location.href = URLFor.chart(that.opts);
      }
    });
    return false;
  },

  bindList: function () {
    var that = this;
    $("#application-tree").load(URLFor.chartList(this.buildParams()), function () {
      $(".chart-search input")
	.focus()
	.livefilter({selector:'#application-tree a'});
      $('.chart-delete-button').click(that.deleteChartEvent);
    });
  },

  bindNewChartButton: function () {
    var that = this;
    $(".chart-add-button")
      .button({
	icons: {
          primary: "ui-icon-circle-plus"
	}
      })
      .click(function () {
	document.location.href = URLFor.newChart(that.opts);
      });
  },

  bind: function () {
    this.bindList();
    this.bindNewChartButton();
  }
});


/* FilterXAxisView requires following env variables:
 * - opts.projectSlug  - current project slug
 * - opts.chartid      - the chart type id
 *
 * Usage:
 *
 * var view = new FilterXAxisView({ projectSlug: PROJECT_SLUG, chartid: CHARTID });
 * view.bind();
 */
var FilterXAxisView = BaseWizzard.extend({
  nextUrl: function () {
    return URLFor.chartView(this.buildParams());
  },

  backUrl: function () {
    return URLFor.chartTypeView(this.buildParams());
  }
});


/* SavedChartFilterView requires following env variables:
 * - opts.projectSlug  - current project slug
 * - opts.chartid      - the chart type id
 *
 * Usage:
 *
 * var view = new SavedChartFilterView({ projectSlug: PROJECT_SLUG, chartid: CHARTID });
 * view.bind();
 */
var SavedChartFilterView = BaseWizzard.extend({
  nextUrl: function () {
    return URLFor.savedChartView(this.buildParams());
  },

  bindBackButton: function () {}
});


/* ChartView requires following env variables:
 * - opts.projectSlug   - current project slug
 * - opts.searchParams  - params as string
 * - opts.chartid       - the chart ID
 * - opts.searchParamsJSON
 *
 * Operation to override:
 * - override.bindBackButton,
 *
 * Usage:
 *
 * var view = ChartView({ searchParams: PARAMS });
 * view.bind();
 */
var ChartView = BaseWizzard.extend({
  backUrl: function () {
    return URLFor.xAxisView(this.buildParams());
  },

  bindOnPageSelect: function () {
    var that = this;
    $('#id_onpage').change(function () {
      var params = $.extend(that.opts.searchParamsJSON, {
	onpage: $(this).val(),
	page: 1               // on page is changing so we moved to first page
      });
      document.location = document.location.pathname + "?" + $.param(params);
    });
  },

  bindChartForm: function () {
    var that = this;
    $("#id_charttype").val(this.opts.chartid);
    $("#id_query").val(this.opts.searchParams);
    $(".chart-save-panel form").ajaxForm({
      success: function(response) {
	if(!response.success) {
          $.notification.error(response.message);
          $.shortcuts.showErrors(response.data)
	} else {
          $.notification.notice(response.message);
	  document.location.href = URLFor.savedChartView(that.buildParams({
	    id: response.data.id,
	    searchParams: response.data.query
	  }));
	}
      },
      beforeSubmit: function() {
	$.shortcuts.hideErrors();
      }
    });
  },

  bind: function () {
    this._super();
    this.bindOnPageSelect();
    this.bindChartForm();
  }
});


var SavedChartView = ChartView.extend({
  backUrl : function () {
    return URLFor.savedXAxisView(this.buildParams());
  }
});
