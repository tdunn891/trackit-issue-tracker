// Fetch source data for charts from Django REST API
fetch('https://django-issue-tracker-1.herokuapp.com/tickets/api/tickets')
	.then((response) => {
		return response.json();
	})
	.then((data) => {
		// Parse datetime
		const dateFormatSpecifier = '%Y-%m-%dT%H:%M:%S.%f%Z';
		const dateFormatParser = d3.timeParse(dateFormatSpecifier);

		data.forEach((d) => {
			// CREATED DATE parsed
			d.created_date_dd = dateFormatParser(d.created_date);
			// Day month year
			d.created_date_day = d3.timeDay(d.created_date_dd);
			// Month
			d.created_date_month = d3.timeMonth(d.created_date_dd);
			// Month
			d.created_date_year = d3.timeYear(d.created_date_dd);
			// If ticket status is resolved, parse RESOLVED DATE
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
	// Crossfilter data
	let ndx = crossfilter(data);

	// Pass crossfiltered data to charts
	drawTicketTypeRowChart(ndx);
	drawPriorityPieChart(ndx);
	drawStatusRowChart(ndx);
	drawUpvotesRowChart(ndx);
	drawStatusByMonthBarChart(ndx);
	showFilteredCount(ndx);

	// Render all charts
	dc.renderAll();
}

// Status by Month Bar Chart
function drawStatusByMonthBarChart(ndx) {
	let dateCreatedDim = ndx.dimension((d) => d.created_date_day);
	let statusGroup = dateCreatedDim
		.group()
		.reduce(reduceAdd, reduceRemove, reduceInitial);

	// Custom reducer
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
		.width(700)
		.height(300)
		.dimension(dateCreatedDim)
		.group(statusGroup, 'New', (d) => d.value['New'])
		.stack(statusGroup, 'In Progress', (d) => d.value['In Progress'])
		.stack(statusGroup, 'Resolved', (d) => d.value['Resolved'])
		.stack(statusGroup, 'Cancelled', (d) => d.value['Cancelled'])
		.xAxisLabel('Date Submitted', 25)
		.yAxisLabel('Number of Tickets', 25)
		.useViewBoxResizing(true)
		.renderHorizontalGridLines(true)
		.ordinalColors(['lightblue', 'orange', 'green', 'grey'])
		.renderTitle(true)
		.title(function (d) {
			return [
				d.key + '\n',
				'New: ' + (d.value['New'] || '0'),
				'In Progress: ' + (d.value['In Progress'] || '0'),
				'Resolved: ' + (d.value['Resolved'] || '0'),
				'Cancelled: ' + (d.value['Cancelled'] || '0'),
			].join('\n');
		})
		.margins({ top: 30, left: 60, right: 20, bottom: 70 })
		.x(d3.scaleTime().domain([new Date(2020, 01, 10), new Date(2020, 06, 01)]))
		.elasticX(true)
		.alwaysUseRounding(true)
		.xUnits(d3.timeDays)
		.xAxis();
}

// TicketType Pie Chart
function drawTicketTypeRowChart(ndx) {
	let ticketTypeDim = ndx.dimension((d) => d.ticket_type);
	let ticketTypeGroup = ticketTypeDim.group();

	dc.rowChart('#ticketTypeRowChart')
		.width(440)
		.height(160)
		.gap(16)
		.titleLabelOffsetX(413)
		.label((d) => d.key + ': ' + d.value)
		.rowsCap(8)
		.useViewBoxResizing(true)
		.dimension(ticketTypeDim)
		.group(ticketTypeGroup);
}

// Priority Pie Chart
function drawPriorityPieChart(ndx) {
	let priorityDim = ndx.dimension((d) => d.priority);
	let priorityGroup = priorityDim.group();

	// Priority row Chart
	dc.rowChart('#priorityRowChart')
		.width(440)
		.height(160)
		.gap(6)
		.titleLabelOffsetX(413)
		.label((d) => d.key + ': ' + d.value)
		.useViewBoxResizing(true)
		.dimension(priorityDim)
		.group(priorityGroup);
}

// Status Pie Chart
function drawStatusRowChart(ndx) {
	let statusDim = ndx.dimension((d) => d.status);
	let statusGroup = statusDim.group();

	// Open/Closed Dimension
	let openClosedDim = ndx.dimension(function (d) {
		if (d.status == 'Resolved' || d.status == 'Cancelled') {
			return 'Closed';
		} else {
			return 'Open';
		}
	});

	// Open/Closed Group
	let openClosedGroup = openClosedDim.group();

	// Status Row Chart
	dc.rowChart('#statusRowChart')
		.width(440)
		.height(160)
		.gap(2)
		.titleLabelOffsetX(413)
		.label((d) => d.key + ': ' + d.value)
		.ordinalColors(['green', 'grey', 'orange', 'lightblue'])
		.useViewBoxResizing(true)
		.dimension(statusDim)
		.group(statusGroup);

	// Open/Closed Status Pie Chart
	dc.pieChart('#open-closed-tickets-pie-chart')
		.minAngleForLabel(0.2)
		.dimension(openClosedDim)
		.group(openClosedGroup)
		.useViewBoxResizing(true)
		.height(150)
		.label((d) => d.key + ': ' + d.value);
}

// Most Upvoted Tickets
function drawUpvotesRowChart(ndx) {
	let summaryDim = ndx.dimension(dc.pluck('summary'));
	let upvotesGroup = summaryDim.group().reduceSum((d) => +d.upvotes);

	dc.rowChart('#upvotesRowChart')
		.width(460)
		.height(210)
		.gap(2)
		.label((d) => d.key + ': ' + d.value)
		.rowsCap(8)
		.useViewBoxResizing(true)
		.dimension(summaryDim)
		.group(upvotesGroup);
}

// Filtered records count
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
				'<strong>%filter-count</strong> of <strong>%total-count</strong> Tickets',
		});
}

// Reset all charts
$('.reset').click(function () {
	dc.filterAll();
	dc.redrawAll();
});
