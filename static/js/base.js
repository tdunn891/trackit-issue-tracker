$(document).ready(function () {
	// Initialise all tooltips
	$(function () {
		$('[data-toggle="tooltip"]').tooltip();
	});

	// KANBAN JS
	if (window.location.pathname == '/tickets/kanban/') {
		// Nav link active
		$('#kanban-nav-link').toggleClass('active');

		// Toggle Cancelled column display
		$('#cancelled-checkbox').click(function () {
			$('.kanban-cancelled').parent().toggleClass('d-none');
			// Toggle responsive classes on columns to ensure clean display
			$('.kanban-col').toggleClass('col-md-3');
			$('.kanban-col').toggleClass('col-md-4');
		});
	}

	// REGISTRATION JS
	if (window.location.pathname == '/accounts/register/') {
		$('#register-nav-item').toggleClass('d-none');
		// $('#id_email').focus();
	}

	// LOGIN JS
	if (window.location.pathname == '/accounts/login/') {
		$('#login-nav-item').toggleClass('d-none');
		$('#id_username').focus();
	}

	// DASHBOARD JS
	if (window.location.pathname == '/tickets/dashboard/') {
		$('#dashboard-nav-link').toggleClass('active');
	}

	// USER lIST JS
	if (window.location.pathname == '/accounts/user_list/') {
		// Nav link active
		$('#user-list-nav-link').toggleClass('active');

		// Initialize DataTables
		$('#submitters-table').DataTable({
			language: {
				search: '_INPUT_',
				searchPlaceholder: 'Search...',
			},
			// Set template of pagination display
			oLanguage: {
				sLengthMenu: 'Show: _MENU_ users',
				sInfo: 'Showing: _START_-_END_ of _TOTAL_',
			},
		});
		$('#assignees-table').DataTable({
			language: {
				search: '_INPUT_',
				searchPlaceholder: 'Search...',
			},
			// Set template of pagination display
			oLanguage: {
				sLengthMenu: 'Show: _MENU_ users',
				sInfo: 'Showing: _START_-_END_ of _TOTAL_',
			},
		});
		// Focus on search input
		$('#submitters-table_filter > label > input').focus();
	}

	// TICKETS JS
	if (window.location.pathname == '/tickets/') {
		// Nav link active
		$('#tickets-nav-link').toggleClass('active');

		// Field Filtering: Insert a text input to each footer cell of table
		$('#tickets-table tfoot th').each(function () {
			let title = $(this).text();
			$(this).html('<input type="text" placeholder="Search ' + title + '" />');
		});

		let ticketsTable = $('#tickets-table').DataTable({
			// Add Global search box
			language: {
				search: '_INPUT_',
				searchPlaceholder: 'Search All...',
			},
			// Define Column widths
			columnDefs: [
				{ width: '410px', targets: [1] },
				{ width: '120px', targets: [3, 4] },
				{ width: '40px', targets: [0, 2, 5, 6] },
				{ width: '100px', targets: [7, 8] },
			],
			// Set template of pagination display
			oLanguage: {
				sLengthMenu: 'Show: _MENU_ tickets',
				sInfo: 'Showing: _START_-_END_ of _TOTAL_',
			},
		});
		// Apply the search
		// Source: https://datatables.net/examples/api/multi_filter.html
		ticketsTable.columns().every(function () {
			let that = this;
			$('input', this.footer()).on('keyup change clear', function () {
				if (that.search() !== this.value) {
					that.search(this.value).draw();
				}
			});
		});
		// Move to search boxes to head of table
		$('#tickets-table tfoot tr').appendTo('#tickets-table thead');
		// Set search box placeholders to blank
		$('#ticket-search-boxes th input').attr('placeholder', '');
		// Go to View Ticket via Clickable row
		$('.clickable-row').on('click', function () {
			window.location = $(this).data('url');
		});
		// Focus on Search Bar
		$('#tickets-table_filter > label > input').focus();
	}

	// PROFILE JS
	if (window.location.pathname == '/accounts/profile/') {
		// Active nav link
		$('#profile-nav-link').toggleClass('active');

		// Update First Name
		$('#first-name-update').on('click', function () {
			$('#first-name-form').toggleClass('d-none');
			$('#current-first-name').toggleClass('d-none');
			$('#cancel-first-name').toggleClass('d-none');
			$(this).toggleClass('d-none');
			$('#first-name-input').focus();
		});
		// Cancel update First Name
		$('#cancel-first-name').on('click', function () {
			$('#first-name-form').toggleClass('d-none');
			$('#current-first-name').toggleClass('d-none');
			$('#first-name-update').toggleClass('d-none');
			$(this).toggleClass('d-none');
		});
		// Update Last Name
		$('#last-name-update').on('click', function () {
			$('#last-name-form').toggleClass('d-none');
			$('#current-last-name').toggleClass('d-none');
			$('#cancel-last-name').toggleClass('d-none');
			$(this).toggleClass('d-none');
			$('#last-name-input').focus();
		});
		// Cancel update Last Name
		$('#cancel-last-name').on('click', function () {
			$('#last-name-form').toggleClass('d-none');
			$('#current-last-name').toggleClass('d-none');
			$('#last-name-update').toggleClass('d-none');
			$(this).toggleClass('d-none');
		});
		// Update ZoomID
		$('#zoomid-update').on('click', function () {
			$('#zoomid-form').toggleClass('d-none');
			$('#current-zoomid').toggleClass('d-none');
			$('#cancel-zoomid').toggleClass('d-none');
			$(this).toggleClass('d-none');
			$('#zoomid-input').focus();
		});
		// Cancel ZoomID
		$('#cancel-zoomid').on('click', function () {
			$('#zoomid-form').toggleClass('d-none');
			$('#current-zoomid').toggleClass('d-none');
			$('#zoomid-update').toggleClass('d-none');
			$(this).toggleClass('d-none');
		});
		// Toggle image upload form field
		$('#profile-image').on('click', function () {
			$('#profile-image-form').removeClass('d-none');
		});
		$('#id_image').on('click', function () {
			$('#save-profile-image-btn').removeClass('d-none');
		});
	}
});
