// $(document).ready(function() {
// 	$('#datatabletest').DataTable();
// });

// Fetch data from django rest API
fetch('http://localhost:8000/tickets/api/tickets')
	.then(response => {
		return response.json();
	})
	.then(data => {
		console.log(data);

		// date parsing test
		// const dateFormatSpecifier = '%m/%d/%Y';
		const dateFormatSpecifier = '%Y-%m-%dT%H:%M:%S.%f%Z';
		const dateFormat = d3.timeFormat(dateFormatSpecifier);
		const dateFormatParser = d3.timeParse(dateFormatSpecifier);
		const numberFormat = d3.format('.2f');

		data.forEach(d => {
			// CREATED DATE parsed
			d.created_date_dd = dateFormatParser(d.created_date);
			// Day month year
			d.created_date_day = d3.timeDay(d.created_date_dd);
			// Month
			d.created_date_month = d3.timeMonth(d.created_date_dd);
			// Month
			d.created_date_year = d3.timeYear(d.created_date_dd);
			// RESOLVED DATE parsed, if resolved
			if (d.resolved_date) {
				// Parsed date
				d.resolved_date_dd = dateFormatParser(d.resolved_date);
				// Day month year
				d.resolved_date_day = d3.timeDay(d.resolved_date_dd);
				// Month
				d.resolved_date_month = d3.timeMonth(d.resolved_date_dd);
				// Year
				d.resolved_date_year = d3.timeYear(d.resolved_date_dd);
			}
		});

		drawGraphs(data);
	});

function drawGraphs(data) {
	let ndx = crossfilter(data);
	drawTicketTypeRowChart(ndx);
	drawPriorityPieChart(ndx);
	drawStatusRowChart(ndx);
	drawUpvotesRowChart(ndx);
	drawStatusByMonthBarChart(ndx);
	showFilteredCount(ndx);
	showAverageDaysToResolve(ndx);
	// drawDataTable(ndx);
	// showAgePriorityScatterPlot(ndx);
	// test, not useful?
	// showAgedRowChart(ndx);
	dc.renderAll();
}

// Not useful?
function showAgedRowChart(ndx) {
	let agedDim = ndx.dimension(d => d.age);
	let agedGroup = agedDim.group();

	dc.rowChart('#agedRowChart')
		.width(500)
		.height(130)
		.gap(2)
		// .renderTitleLabel(true)
		.titleLabelOffsetX(413)
		.label(d => d.key + ': ' + d.value)
		// .rowsCap(5)
		.useViewBoxResizing(true)
		.dimension(agedDim)
		.group(agedGroup);
}

// Average days until resolution
function showAverageDaysToResolve(ndx) {
	// Custom reduce Average function
	function reduceAvg(dimension, type) {
		return dimension.groupAll().reduce(
			function(p, v) {
				p.count++;
				p.total += v[type];
				p.average = p.total / p.count;
				return p;
			},

			function(p, v) {
				p.count--;
				p.total -= v[type];
				p.average = p.total / p.count;
				return p;
			},

			function() {
				return {
					count: 0,
					total: 0,
					average: 0
				};
			}
		);
	}
	// groupAll averages groups
	// let ageGroup = reduceAvg(ndx, 'age');
	let ageGroup = reduceAvg(ndx, 'days_to_resolve');
	dc.numberDisplay('#average-days-to-resolve')
		// .group(group)
		.group(ageGroup)
		.valueAccessor(function(d) {
			return d.average;
		});
}

// Test open tickets count
function displayOpenTicketsCount(ndx) {
	// let openDim = ndx.dimension(d => d.status);
	let openGroup = ndx.groupAll();
	print_filter(openGroup);

	dc.numberDisplay('#open-tickets-count')
		.group(openGroup)
		.valueAccessor(function(d) {
			if (d.status == 'Resolved') {
				return d;
			}
		});
}

// Status by month
function drawStatusByMonthBarChart(ndx) {
	let dateCreatedDim = ndx.dimension(d => d.created_date_day);
	let statusGroup = dateCreatedDim
		.group()
		.reduce(reduceAdd, reduceRemove, reduceInitial);

	function reduceAdd(i, d) {
		i[d.status] = (i[d.status] || 0) + 1;
		return i;
	}
	function reduceRemove(i, d) {
		i[d.status] = (i[d.status] || 0) - 1;
		return i;
	}
	function reduceInitial() {
		return {};
	}

	// Stacked bar chart status by month
	stackedBar = dc
		.barChart('#statusByMonthBarChart')
		.width(800)
		.height(375)
		.dimension(dateCreatedDim)
		.group(statusGroup, 'New', d => d.value['New'])
		.stack(statusGroup, 'In Progress', d => d.value['In Progress'])
		.stack(statusGroup, 'Resolved', d => d.value['Resolved'])
		.stack(statusGroup, 'Cancelled', d => d.value['Cancelled'])
		.xAxisLabel('Date Submitted', 25)
		.yAxisLabel('Number of Tickets', 25)
		.useViewBoxResizing(true)
		.renderHorizontalGridLines(true)
		.ordinalColors(['lightblue', 'orange', 'green', 'grey'])
		.renderTitle(true)
		.title(function(d) {
			return [
				d.key + '\n',
				'New: ' + (d.value['New'] || '0'),
				'In Progress: ' + (d.value['In Progress'] || '0'),
				'Resolved: ' + (d.value['Resolved'] || '0'),
				'Cancelled: ' + (d.value['Cancelled'] || '0')
			].join('\n');
		})
		.margins({ top: 30, left: 60, right: 20, bottom: 70 })
		.x(d3.scaleTime().domain([new Date(2020, 01, 15), new Date(2020, 03, 03)]))
		.elasticX(true)
		.alwaysUseRounding(true)
		.xUnits(d3.timeDays)
		.xAxis();
}

// TicketType Pie Chart
function drawTicketTypeRowChart(ndx) {
	let ticketTypeDim = ndx.dimension(d => d.ticket_type);
	let ticketTypeGroup = ticketTypeDim.group();

	dc.rowChart('#ticketTypeRowChart')
		.width(500)
		.height(130)
		.gap(2)
		.titleLabelOffsetX(413)
		.label(d => d.key + ': ' + d.value)
		.rowsCap(8)
		.useViewBoxResizing(true)
		.dimension(ticketTypeDim)
		.group(ticketTypeGroup);
}

// Priority Pie Chart
function drawPriorityPieChart(ndx) {
	let priorityDim = ndx.dimension(d => d.priority);
	let priorityGroup = priorityDim.group();

	// Priority row Chart
	dc.rowChart('#priorityRowChart')
		.width(500)
		.height(130)
		.gap(2)
		.titleLabelOffsetX(413)
		.label(d => d.key + ': ' + d.value)
		.useViewBoxResizing(true)
		.dimension(priorityDim)
		.group(priorityGroup);
}

// Status Pie Chart
function drawStatusRowChart(ndx) {
	let statusDim = ndx.dimension(d => d.status);
	let statusGroup = statusDim.group();

	// Open/Closed
	let openClosedDim = ndx.dimension(function(d) {
		if (d.status == 'Resolved' || d.status == 'Cancelled') {
			return 'Closed';
		} else {
			return 'Open';
		}
	});
	let openClosedGroup = openClosedDim.group();

	print_filter(statusGroup);
	print_filter(openClosedGroup);

	// Status Row Chart
	dc.rowChart('#statusRowChart')
		.width(500)
		.height(200)
		.gap(2)
		.titleLabelOffsetX(413)
		.label(d => d.key + ': ' + d.value)
		.ordinalColors(['green', 'orange', 'lightblue', 'grey'])
		.useViewBoxResizing(true)
		.dimension(statusDim)
		.group(statusGroup);

	// Open/Closed Status Pie Chart
	dc.pieChart('#open-closed-tickets-pie-chart')
		// .radius(40)
		.minAngleForLabel(0.2)
		.dimension(openClosedDim)
		.group(openClosedGroup)
		// .ordinalColors(['orange', 'green'])
		.useViewBoxResizing(true)
		.height(170)
		// .width(800)
		.label(d => d.key + ': ' + d.value);
	// .innerRadius(10);

	// Pie chart
	// dc.pieChart('#statusPieChart')
	// 	.radius(180)
	// 	.minAngleForLabel(0.2)
	// 	.dimension(statusDim)
	// 	.group(statusGroup)
	// 	.ordinalColors(['lightblue', 'orange', 'green', 'grey'])
	// 	.height(295)
	// 	.width(500)
	// 	.label(d => d.key + ': ' + d.value)
	//    .innerRadius(40)

	// .internalLabels(50)
	// .drawPaths(true)
	// .cx(330)
	// .cy(150)
	// .legend(
	// 	dc
	// 		.legend()
	// 		.x(30)
	// 		.y(65)
	// 		.autoItemWidth(true)
	// 		.itemHeight(32)
	// 		.gap(12)
	// )
	// .useViewBoxResizing(true);
}

// Assigned To Row Chart
function drawAssignedToRowChart(ndx) {
	let assignedToDim = ndx.dimension(dc.pluck('assigned_to'));
	let assignedToGroup = assignedToDim.group().reduceCount();

	dc.rowChart('#assignedToRowChart')
		.width(500)
		.height(330)
		.gap(2)
		.renderTitleLabel(true)
		.titleLabelOffsetX(413)
		.label(function() {
			return '';
		})
		.rowsCap(5)
		.useViewBoxResizing(true)
		.dimension(assignedToDim)
		.group(assignedToGroup);
}

// Most Upvoted Tickets
function drawUpvotesRowChart(ndx) {
	let summaryDim = ndx.dimension(dc.pluck('summary'));
	let upvotesGroup = summaryDim.group().reduceSum(d => +d.upvotes);

	dc.rowChart('#upvotesRowChart')
		.width(500)
		.height(330)
		.gap(2)
		// .renderTitleLabel(true)
		// .titleLabelOffsetX(413)
		.label(d => d.key + ': ' + d.value)
		.rowsCap(8)
		.useViewBoxResizing(true)
		// .d3.axis.tickFormat()
		.dimension(summaryDim)
		.group(upvotesGroup);
}

function showAgePriorityScatterPlot(ndx) {
	let dim = ndx.dimension(function(d) {
		return [d.priority, d.age];
	});
	let group = dim.group();

	// print_filter(group);

	dc.bubbleChart('#age-priority-scatter-plot')
		// dc.scatterPlot('#age-priority-scatter-plot')
		.width(800)
		.height(300)
		.yAxisLabel('Priority')
		.xAxisLabel('Age')
		.useViewBoxResizing(true)
		.x(d3.scaleLinear().domain([0, 30]))
		// .brushOn(true)
		.brushOn(false)
		.clipPadding(30)
		// .symbolSize(10)
		// .y(d3.scaleOrdinal().domain(['Low', 'Medium', 'High']))
		.y(d3.scaleOrdinal().domain(['Low', 'Medium', 'High']))
		// .y(d3.scaleOrdinal())
		// Bubble
		.colors(d3.schemeRdYlGn[9])
		.colorDomain([0, 30])
		.colorAccessor(d => d.value)
		// .colors(d3.scale.category10())
		.keyAccessor(d => d.key[1])
		.valueAccessor(d => d.key[0])
		.radiusValueAccessor(d => d.value)
		.maxBubbleRelativeSize(0.08)
		.r(d3.scaleLinear().domain([0, 10]))
		.title(d => 'Num tix with this priority and age: ' + d.value)
		.label(d => d.value + ' : ' + d.key)
		.dimension(dim)
		.group(group);
}

function showFilteredCount(ndx) {
	let all = ndx.groupAll();
	dc.dataCount('#filtered-count')
		.crossfilter(ndx)
		.groupAll(all)
		.html({
			some:
				" <a href='javascript:dc.filterAll(); dc.redrawAll();'>Reset</a> " +
				'<i class="material-icons">filter_list</i> ' +
				'<strong>%filter-count</strong> of <strong>%total-count</strong> Tickets',
			all:
				'<i class="material-icons">filter_list</i> ' +
				'<strong>%filter-count</strong> of <strong>%total-count</strong> Tickets'
		});
}
/* <a href='javascript:dc.filterAll(); dc.redrawAll();' > Reset</a> */
// Reset all charts
$('.reset').click(function() {
	dc.filterAll();
	dc.redrawAll();
});

// Print filter
// * testing only
function print_filter(filter) {
	var f = eval(filter);
	if (typeof f.length != 'undefined') {
	} else {
	}
	if (typeof f.top != 'undefined') {
		f = f.top(Infinity);
	} else {
	}
	if (typeof f.dimension != 'undefined') {
		f = f
			.dimension(function(d) {
				return '';
			})
			.top(Infinity);
	} else {
	}
	console.log(
		filter +
			'(' +
			f.length +
			') = ' +
			JSON.stringify(f)
				.replace('[', '[\n\t')
				.replace(/}\,/g, '},\n\t')
				.replace(']', '\n]')
	);
}
