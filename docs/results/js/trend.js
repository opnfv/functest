// ******************************************
// Trend line for reporting
// based on scenario_history.txt
// where data looks like
// date,scenario,installer,detail,score
// 2016-09-22 13:12,os-nosdn-fdio-noha,apex,4/12,33.0
// 2016-09-22 13:13,os-odl_l2-fdio-noha,apex,12/15,80.0
// 2016-09-22 13:13,os-odl_l2-sfc-noha,apex,18/24,75.0
// .....
// ******************************************
// Set the dimensions of the canvas / graph
var trend_margin = {top: 20, right: 30, bottom: 50, left: 40},
  trend_width = 300 - trend_margin.left - trend_margin.right,
  trend_height = 130 - trend_margin.top - trend_margin.bottom;

// Parse the date / time
var parseDate = d3.time.format("%Y-%m-%d %H:%M").parse;

// Set the ranges
var trend_x = d3.time.scale().range([0, trend_width]);
var trend_y = d3.scale.linear().range([trend_height, 0]);

// Define the axes
var trend_xAxis = d3.svg.axis().scale(trend_x)
  .orient("bottom").ticks(2).tickFormat(d3.time.format("%m-%d"));

var trend_yAxis = d3.svg.axis().scale(trend_y)
  .orient("left").ticks(2);

// Define the line
var valueline = d3.svg.line()
  .x(function(d) { return trend_x(d.date); })
  .y(function(d) { return trend_y(d.score); });

var trend = function(container, trend_data) {

    var trend_svg = d3.select(container)
    .append("svg")
      .attr("width", trend_width + trend_margin.left + trend_margin.right)
      .attr("height", trend_height + trend_margin.top + trend_margin.bottom)
    .append("g")
            .attr("transform",
              "translate(" + trend_margin.left + "," + trend_margin.top + ")");

    // Scale the range of the data
    trend_x.domain(d3.extent(trend_data, function(d) { return d.date; }));
    trend_y.domain([0, d3.max(trend_data, function(d) { return d.score; })]);

    // Add the X Axis
    trend_svg.append("g")
        .attr("class", "x axis")
        .attr("transform", "translate(0," + trend_height + ")")
        .call(trend_xAxis);

    // Add the Y Axis
    trend_svg.append("g")
        .attr("class", "y axis")
        .call(trend_yAxis);

    // Add the valueline path.
    trend_svg.append("path")
        .attr("class", "line")
        .attr("d", valueline(trend_data))
    .attr("stroke", "steelblue")
    .attr("fill", "none");
 
    trend_svg.selectAll(".dot")
      .data(trend_data)
      .enter().append("circle")
      .attr("r", 2.5)
        .attr("cx", function(d) { return trend_x(d.date); })
        .attr("cy", function(d) { return trend_y(d.score); });   

     return trend;
}
