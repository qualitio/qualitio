/* This file requires following files / libs to be included:
   - "simple.inheritance.js"
   - "chart.js"
   - "underscore.js" (bind function is used)
*/


var JQPlotChartHandler = Class.extend({
  init: function (opts) {
    this.opts = opts;
  },

  loadPlot: function () {
    $.ajax({
      async: true,
      url: URLFor.chartdata(this.opts),
      dataType: "json",
      success: _.bind(function (response) {
	console.log(response);
	return this.onSuccess(response);
      }, this)
    });
  },

  onSuccess: function (response) {
    // inherit and change
  },

  bind: function () {
    this.loadPlot();
    $(window).resize(_.bind(function () {
      $('#chart *').remove();
      this.loadPlot();
    }, this));
  }
});


var PieChart = JQPlotChartHandler.extend({
  onSuccess: function (response) {
    $('#loading-info').remove();

    var plot = $.jqplot('chart', response.data, {
      title: response.options.title,

      seriesDefaults: {
	renderer: $.jqplot.PieRenderer,
	rendererOptions: {
          barMargin: 30,
          fillToZero: true,
          showDataLabels: true
	},
      },

      legend: {
        labels: response.options.legendLabels || [],
	show: true,
	location: 'e',
	placement: 'outside'
      }
    });
  }
});


var BarChart = JQPlotChartHandler.extend({
  onSuccess: function (response) {
    $('#loading-info').remove();

    var plot = $.jqplot('chart', response.data, {
      title: response.options.title,
      stackSeries: response.options.stackBar,

      axesDefaults: {
        tickRenderer: $.jqplot.CanvasAxisTickRenderer ,
        tickOptions: {
          angle: 30,
          fontSize: '10pt'
        },
      },

      seriesDefaults:{
	renderer: $.jqplot.BarRenderer,
	rendererOptions: {
          barMargin: 30,
          fillToZero: true
	},
      },

      axes: {
	xaxis: {
          renderer: $.jqplot.CategoryAxisRenderer,
          ticks: response.options.xaxisNames
	},
	yaxis: {
          padMin: 0,
          max: response.options.yaxismax,
          autoscale: true
	},
      },

      legend: {
        labels: response.options.legendLabels || [],
	show: true,
	location: 'e',
	placement: 'outside'
      }
    });
  }
});