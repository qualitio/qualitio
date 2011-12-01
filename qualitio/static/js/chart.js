/* This file contains all of needed functions in chart wizzard views: */


/* Utils */
var URLFor = {
  /* Requires:
   * - opts.projectSlug,
   * - opts.chartid,
   */
  chartTypeView: function(opts) {
    return "/project/" + opts.projectSlug + "/chart/" + opts.chartid + "/";
  },

  /* Requires:
   * - opts.projectSlug,
   * - opts.chartid,
   * - opts.searchParams
   */
  xAxisView: function(opts) {
    return "/project/" + opts.projectSlug + "/chart/" + opts.chartid  + "/chartview/?" + opts.searchParams;
  },

  /* This is a ajax view for open-flash-chart flash plugin.
   *  Requires:
   * - opts.projectSlug,
   * - opts.chartid,
   * - opts.searchParams,
   */
  chartdata: function(opts) {
    return "/project/" + opts.projectSlug + "/chart/" + opts.chartid  + "/chartdata/?" + opts.searchParams;
  }
};


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

  var urlParams = $.extend({
    chartid: chartidSelect.val()
  }, opts); // projectSlug should be in opts!

  var applyLinkToButton = function() {
    $(".create-chart").attr("href", URLFor.chartTypeView(urlParams));
  };

  return {
    bind: function() {
      chartidSelect.change(applyLinkToButton);
      applyLinkToButton();
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
  var urlParams = $.extend({
    searchParams: document.location.search
  }, opts); // "projectSlug" and "chartid" should be in opts!

  return {
    bind: function () {
      $("#show-chart").click(function() {
	$(this).attr("href", URLFor.xAxisView(urlParams));
	return true;
      });
    }
  }
});


/* ChartView requires following env variables:
 * - opts.searchParams  - should be provided as variable eg PARAMS
 *
 * Usage:
 *
 * var view = ChartView({ searchParams: PARAMS });
 * view.bind();
 */
var ChartView = (function (opts) {
  return {
    bind: function () {
      $('#id_onpage').change(function () {
	var params = $.extend(opts.searchParams, {
	  onpage: $(this).val(),
	  page: 1               // on page is changing so we moved to first page
	});
	document.location = document.location.pathname + "?" + $.param(params);
      });
    }
  }
});
