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
      return "/project/" + opts.projectSlug + "/chart/" + opts.chartid  + "/" + addQuestionMark(opts.searchParams);
    },

    /* Requires:
     * - opts.projectSlug,
     * - opts.chartid,
     * - opts.searchParams
     */
    chartView: function(opts) {
      return "/project/" + opts.projectSlug + "/chart/" + opts.chartid  + "/chartview/" + addQuestionMark(opts.searchParams);
    },

    /* This is a ajax view for open-flash-chart flash plugin.
     *  Requires:
     * - opts.projectSlug,
     * - opts.chartid,
     * - opts.searchParams,
     */
    chartdata: function(opts) {
      return "/project/" + opts.projectSlug + "/chart/" + opts.chartid  + "/chartdata/" + addQuestionMark(opts.searchParams);
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

  var urlParams = $.extend({
    chartid: chartidSelect.val()
  }, opts); // projectSlug should be in opts!

  var applyLinkToButton = function() {
    $(".filter-xaxis-button").attr("href", URLFor.xAxisView(urlParams));
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
      $('.cancel-button').attr("href", URLFor.chartTypeView(opts));

      $(".show-chart-button").click(function() {
	$(this).attr("href", URLFor.chartView(urlParams));
	return true;
      });
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
    }
  }
});
