$(document).ready(function() {
	// Initialise all tooltips
	$(function() {
		$('[data-toggle="tooltip"]').tooltip();
	});

	// KANBAN JS
	if (window.location.pathname == '/tickets/kanban/') {
		// Toggle Cancelled column display
		$('#cancelled-checkbox').click(function() {
			$('.kanban-cancelled')
				.parent()
				.toggleClass('d-none');
		});
	}

	// USER lIST JS
	if (window.location.pathname == '/accounts/user_list/') {
		// Initialize DataTables
		$('#submitters-table').DataTable({
			language: {
				search: '_INPUT_',
				searchPlaceholder: 'Search...'
			},
			// Set template of pagination display
			oLanguage: {
				sLengthMenu: 'Show: _MENU_ users',
				sInfo: 'Showing: _START_-_END_ of _TOTAL_'
			}
		});
		$('#assignees-table').DataTable({
			language: {
				search: '_INPUT_',
				searchPlaceholder: 'Search...'
			},
			// Set template of pagination display
			oLanguage: {
				sLengthMenu: 'Show: _MENU_ users',
				sInfo: 'Showing: _START_-_END_ of _TOTAL_'
			}
		});
	}

	// TICKETS JS
	if (window.location.pathname == '/tickets/') {
		console.log('TICKETS PAGE');

		// Field Filtering: Insert a text input to each footer cell of table
		$('#tickets-table tfoot th').each(function() {
			var title = $(this).text();
			$(this).html('<input type="text" placeholder="Search ' + title + '" />');
		});

		let ticketsTable = $('#tickets-table').DataTable({
			// Add Global search box
			language: {
				search: '_INPUT_',
				searchPlaceholder: 'Search All...'
			},
			// Define Column widths
			columnDefs: [
				{ width: '16px', targets: [0, 2, 5, 6] },
				{ width: '340px', targets: [1] }
			],
			// Set template of pagination display
			oLanguage: {
				sLengthMenu: 'Show: _MENU_ tickets',
				sInfo: 'Showing: _START_-_END_ of _TOTAL_'
			}
		});
		// Apply the search
		// Source: https://datatables.net/examples/api/multi_filter.html
		ticketsTable.columns().every(function() {
			let that = this;
			$('input', this.footer()).on('keyup change clear', function() {
				if (that.search() !== this.value) {
					that.search(this.value).draw();
				}
			});
		});
		// Move to search boxes to head of table
		$('#tickets-table tfoot tr').appendTo('#tickets-table thead');
		// Set search box placeholders to blank
		$('#ticket-search-boxes th input').attr('placeholder', '');
		// Clickable row
		$('.clickable-row').on('click', function() {
			window.location = $(this).data('url');
		});
	}
});
