// ******************************************
// Gauge for reporting
// Each scenario has a score
// We use a gauge to indicate the trust level
// ******************************************
var gauge = function(container) {
  var that = {};
  var config = {
    size						: 150,
    clipWidth					: 250,
    clipHeight					: 100,
    ringInset					: 20,
    ringWidth					: 40,

    pointerWidth				: 7,
    pointerTailLength			: 5,
    pointerHeadLengthPercent	: 0.8,

    minValue					: 0,
    maxValue					: 100,

    minAngle					: -90,
    maxAngle					: 90,

    transitionMs				: 4000,

    majorTicks					: 7,
    labelFormat					: d3.format(',g'),
    labelInset					: 10,

    arcColorFn					: d3.interpolateHsl(d3.rgb('#ff0000'), d3.rgb('#00ff00'))
  };


var range = undefined;
var r = undefined;
var pointerHeadLength = undefined;
var value = 0;

var svg = undefined;
var arc = undefined;
var scale = undefined;
var ticks = undefined;
var tickData = undefined;
var pointer = undefined;

var donut = d3.layout.pie();

function deg2rad(deg) {
  return deg * Math.PI / 180;
}

function newAngle(d) {
  var ratio = scale(d);
  var newAngle = config.minAngle + (ratio * range);
  return newAngle;
}

function configure() {
  range = config.maxAngle - config.minAngle;
  r = config.size / 2;
  pointerHeadLength = Math.round(r * config.pointerHeadLengthPercent);

  // a linear scale that maps domain values to a percent from 0..1
  scale = d3.scale.linear()
    .range([0,1])
    .domain([config.minValue, config.maxValue]);

  ticks = scale.ticks(config.majorTicks);
  tickData = d3.range(config.majorTicks).map(function() {return 1/config.majorTicks;});

  arc = d3.svg.arc()
    .innerRadius(r - config.ringWidth - config.ringInset)
    .outerRadius(r - config.ringInset)
    .startAngle(function(d, i) {
      var ratio = d * i;
      return deg2rad(config.minAngle + (ratio * range));
    })
    .endAngle(function(d, i) {
      var ratio = d * (i+1);
      return deg2rad(config.minAngle + (ratio * range));
    });
}
that.configure = configure;

function centerTranslation() {
  return 'translate('+r +','+ r +')';
}

function isRendered() {
  return (svg !== undefined);
}
that.isRendered = isRendered;

function render(newValue) {
  svg = d3.select(container)
    .append('svg:svg')
      .attr('class', 'gauge')
      .attr('width', config.clipWidth)
      .attr('height', config.clipHeight);

  var centerTx = centerTranslation();

  var arcs = svg.append('g')
      .attr('class', 'arc')
      .attr('transform', centerTx);

  arcs.selectAll('path')
      .data(tickData)
    .enter().append('path')
      .attr('fill', function(d, i) {
        return config.arcColorFn(d * i);
      })
      .attr('d', arc);

  var lg = svg.append('g')
      .attr('class', 'label')
      .attr('transform', centerTx);
  lg.selectAll('text')
      .data(ticks)
    .enter().append('text')
      .attr('transform', function(d) {
        var ratio = scale(d);
        var newAngle = config.minAngle + (ratio * range);
        return 'rotate(' +newAngle +') translate(0,' +(config.labelInset - r) +')';
      })
      .text(config.labelFormat);

  var lineData = [ [config.pointerWidth / 2, 0],
          [0, -pointerHeadLength],
          [-(config.pointerWidth / 2), 0],
          [0, config.pointerTailLength],
          [config.pointerWidth / 2, 0] ];
  var pointerLine = d3.svg.line().interpolate('monotone');
  var pg = svg.append('g').data([lineData])
      .attr('class', 'pointer')
      .attr('transform', centerTx);

  pointer = pg.append('path')
    .attr('d', pointerLine/*function(d) { return pointerLine(d) +'Z';}*/ )
    .attr('transform', 'rotate(' +config.minAngle +')');

  update(newValue === undefined ? 0 : newValue);
}
that.render = render;

function update(newValue, newConfiguration) {
  if ( newConfiguration  !== undefined) {
    configure(newConfiguration);
  }
  var ratio = scale(newValue);
  var newAngle = config.minAngle + (ratio * range);
  pointer.transition()
    .duration(config.transitionMs)
    .ease('elastic')
    .attr('transform', 'rotate(' +newAngle +')');
}
that.update = update;

configure();

render();

return that;
};
