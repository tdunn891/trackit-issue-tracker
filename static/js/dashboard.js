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
		drawGraphs(data);
	});

function drawGraphs(data) {
	let ndx = crossfilter(data);
	drawTicketTypePieChart(ndx);
	drawPriorityPieChart(ndx);
	drawAssignedToRowChart(ndx);
	drawStatusPieChart(ndx);
	drawUpvotesRowChart(ndx);
	drawStatusByMonthBarChart(ndx);
	// drawDataTable(ndx);
	dc.renderAll();
}

// Status by month
function drawStatusByMonthBarChart(ndx) {
	var dateCreatedDim = ndx.dimension(d => d.created_date.substring(0, 10));
	var statusGroup = dateCreatedDim
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

	print_filter(statusGroup);

	// Stacked bar chart status by month
	dc.barChart('#statusByMonthBarChart')
		.width(470)
		.height(350)
		.dimension(dateCreatedDim)
		.group(statusGroup, 'New', d => d.value['New'])
		.stack(statusGroup, 'In Progress', d => d.value['In Progress'])
		.stack(statusGroup, 'Resolved', d => d.value['Resolved'])
		.xAxisLabel('Date', 25)
		.yAxisLabel('Number of Tickets', 25)
		.useViewBoxResizing(true)
		.xUnits(dc.units.ordinal)
		.renderHorizontalGridLines(true)
		.ordinalColors(['grey', 'orange', 'green'])
		.gap(60)
		.renderTitle(true)
		.title(function(d) {
			return [
				d.key + '\n',
				'New: ' + (d.value['New'] || '0'),
				'In Progress: ' + (d.value['In Progress'] || '0'),
				'Resolved: ' + (d.value['Resolved'] || '0')
			].join('\n');
		})
		.margins({ top: 30, left: 60, right: 20, bottom: 70 })
		.x(d3.scaleOrdinal());
}

// TicketType Pie Chart
function drawTicketTypePieChart(ndx) {
	let ticketTypeDim = ndx.dimension(d => d.ticket_type);
	let ticketTypeGroup = ticketTypeDim.group();

	// Pie chart
	dc.pieChart('#ticketTypePieChart')
		.radius(120)
		.minAngleForLabel(0.2)
		.dimension(ticketTypeDim)
		.group(ticketTypeGroup)
		.ordinalColors(['#0D324D', '#73EEDC'])
		.height(295)
		.width(500)
		.label(d => d.key + ': ' + d.value)
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
		.useViewBoxResizing(true);
}

// Priority Pie Chart
function drawPriorityPieChart(ndx) {
	let priorityDim = ndx.dimension(d => d.priority);
	let priorityGroup = priorityDim.group();

	// Priority Pie chart
	dc.pieChart('#priorityPieChart')
		.radius(120)
		.minAngleForLabel(0.2)
		.dimension(priorityDim)
		.group(priorityGroup)
		.ordinalColors(['green', 'orange', 'red'])
		.height(295)
		.width(500)
		.label(d => d.key + ': ' + d.value)
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
		.useViewBoxResizing(true);
}

// Status Pie Chart
function drawStatusPieChart(ndx) {
	let statusDim = ndx.dimension(d => d.status);
	let statusGroup = statusDim.group();

	// Pie chart
	dc.pieChart('#statusPieChart')
		.radius(120)
		.minAngleForLabel(0.2)
		.dimension(statusDim)
		.group(statusGroup)
		.ordinalColors(['grey', 'orange', 'green'])
		.height(295)
		.width(500)
		.label(d => d.key + ': ' + d.value)
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
		.useViewBoxResizing(true);
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
		.rowsCap(5)
		.useViewBoxResizing(true)
		.dimension(summaryDim)
		.group(upvotesGroup);
}

// Test datatable
// function drawDataTable(ndx) {
// 	let dimension = ndx.dimension(d => d.dim);
// 	// let group1 = dimension.groupAll();
// 	// let group1 = dimension.group();

// 	let table1 = dc
// 		.dataTable('#datatabletest')
// 		// .tableview('#datatabletest')
// 		.dimension(dimension)
// 		.height(200)
// 		.width(200)
// 		.size(Infinity)
// 		.columns(['summary', 'ticket_type', 'priority', 'status', 'upvotes']);
// }

// Reset all chart
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
