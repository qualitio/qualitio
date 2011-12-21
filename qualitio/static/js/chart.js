/* This file contains all of needed functions in chart wizzard views: */


/* Utils */
var URLFor = (function () {

  var addQuestionMark = function (params) {
    var p = (params || "");
    if ( ! /^\?/.test(p) && p !== "")
      p = "?" + p;
    return p;
  }

  return {
    /* Requires:
     * - opts.projectSlug,
     * - opts.chartid,
     */
    chartTypeView: function(opts) {
      return "/project/" + opts.projectSlug + "/chart/";
    },

    /* Requires:
     * - opts.projectSlug,
     * - opts.chartid,
     * - opts.searchParams
     */
    xAxisView: function(opts) {
      return "/project/" + opts.projectSlug + "/chart/filter/" + opts.chartid  + "/" + addQuestionMark(opts.searchParams);
    },

    /* Requires:
     * - opts.projectSlug,
     * - opts.chartid,
     * - opts.searchParams
     */
    chartView: function(opts) {
      return "/project/" + opts.projectSlug + "/chart/view/" + opts.chartid  + "/" + addQuestionMark(opts.searchParams);
    },

    /* This is a ajax view for open-flash-chart flash plugin.
     *  Requires:
     * - opts.projectSlug,
     * - opts.chartid,
     * - opts.searchParams,
     */
    chartdata: function(opts) {
      return "/project/" + opts.projectSlug + "/chart/data/" + opts.chartid  + "/" + addQuestionMark(opts.searchParams);
    }
  }
})();


/* ChoosingChartTypeView requires following env variables:
 * - opts.projectSlug
 *
 * Usage:
 *
 * var view = ChoosingChartTypeView({ projectSlug: PROJECT_SLUG });
 * view.bind();
 */
var ChoosingChartTypeView = (function(opts) {
  var chartidSelect = $("#id_chart");

  var applyLinkToButton = function() {
    var urlParams = $.extend({
      chartid: chartidSelect.val()
    }, opts); // projectSlug should be in opts!
    $(".filter-xaxis-button").attr("href", URLFor.xAxisView(urlParams));
  };

  return {
    bind: function() {
      chartidSelect.change(applyLinkToButton);
      applyLinkToButton();
    }
  }
});


var ChartBaseView = (function () {
  return {
    loadList: function () {
      $('#application-tree').load("/project/" + PROJECT_SLUG + "/chart/ajax/list/", function() {
	$(".chart-search input")
	  .focus()
	  .livefilter({selector:'#application-tree a'});
      });
    },

    bindNewChartButton: function () {
      $(".chart-add-button")
	.button({
	  icons: {
            primary: "ui-icon-circle-plus"
	  },
	  text: false
	})
	.click( function () {
	  document.location.href = "/project/" + PROJECT_SLUG + "/chart/new/";
	});
    }
  }
});


/* FilterXAxisView requires following env variables:
 * - opts.projectSlug  - current project slug
 * - opts.chartid      - the chart type id
 *
 * Usage:
 *
 * var view = FilterXAxisView({ projectSlug: PROJECT_SLUG, chartid: CHARTID });
 * view.bind();
 */
var FilterXAxisView = (function(opts) {
  var applyHref = function() {
      var urlParams = $.extend({
	  searchParams: document.location.search
      }, opts); // "projectSlug" and "chartid" should be in opts!
      $(".show-chart-button").attr("href", URLFor.chartView(urlParams));
      return true;
  };

  return {
    bind: function () {
      $('.cancel-button').attr("href", URLFor.chartTypeView(opts));
      $(".show-chart-button").click(applyHref);
      applyHref();
    }
  }
});


/* ChartView requires following env variables:
 * - opts.projectSlug   - current project slug
 * - opts.searchParams  - params as string
 * - opts.chartid       - the chart ID
 * - opts.searchParamsJSON
 *
 * Usage:
 *
 * var view = ChartView({ searchParams: PARAMS });
 * view.bind();
 */
var ChartView = (function (opts) {
  return {
    bind: function () {
      $('.back-button').attr("href", URLFor.xAxisView(opts));

      $('#id_onpage').change(function () {
	var params = $.extend(opts.searchParamsJSON, {
	  onpage: $(this).val(),
	  page: 1               // on page is changing so we moved to first page
	});
	document.location = document.location.pathname + "?" + $.param(params);
      });

      $("#id_charttype").val(opts.chartid);
      $("#id_query").val(opts.searchParams);

      $('.chart-save-panel form').ajaxForm({
	success: function(response) {
	  if(!response.success) {
            $.notification.error(response.message);
            $.shortcuts.showErrors(response.data)
	  } else {
            $.notification.notice(response.message);
	    document.location.href = "/project/" + PROJECT_SLUG + "/chart/saved/" + response.data.id + "/";
	  }
	},
	beforeSubmit: function() {
	  $.shortcuts.hideErrors();
	}
      });
    }
  }
});


$(function() {
  var view = ChartBaseView();
  view.loadList();
  view.bindNewChartButton();
});
