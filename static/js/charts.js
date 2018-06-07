
google.charts.load('current', { packages: [ 'corechart' ]});

function drawChart(rawData, container) {
  var data = new google.visualization.DataTable();
  data.addColumn('string', 'Category');
  data.addColumn('number', 'Min');
  data.addColumn('number', 'Average');
  data.addColumn('number', 'Max');

  
  var rows = Object.keys(rawData).map(label => [ label, rawData[label].min, rawData[label].avg, rawData[label].max ]);
  console.log(rows);
  data.addRows(rows);


  var view = new google.visualization.DataView(data);
  // duplicate 1 column as a dummy data series, and add intervals to it
  view.setColumns([0, 1, {
      id: 'min',
      type: 'number',
      role: 'interval',
      calc: function (dt, row) {
          return dt.getValue(row, 1);
      }
  }, {
      id: 'avg',
      type: 'number',
      role: 'interval',
      calc: function (dt, row) {
          return dt.getValue(row, 2);
      }
  }, {
      id: 'max',
      type: 'number',
      role: 'interval',
      calc: function (dt, row) {
          return dt.getValue(row, 3);
      }
  }, 1, 2, 3]);

  var chart = new google.visualization.LineChart(container);
  chart.draw(view, {
      height: 400,
      width: 600,
      lineWidth: 0,
      intervals: {
          style: 'boxes'
      },
      legend: {
          position: 'none'
      },
      series: {
          0: {
              // dummy data series, controls color of intervals
              visibleInLegend: false,
              color: 'blue',
              enableInteractivity: false
          },
          1: {
              // min series options
          },
          2: {
              // average series options
          },
          3: {
              // max series options
          }
      }
  });
}
