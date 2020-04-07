[![Build Status](https://travis-ci.org/tdunn891/milestone-4.svg?branch=master)](https://travis-ci.org/tdunn891/milestone-4)

## Project Purpose

TrackIt was developed to allow simple, effective tracking of issues, split into Bugs and Feature Requests. The site was developed to be suitable for all organisation types and would be deployed

## UX

### Strategy

Site Objective: Provide platform to track tickets (Bugs and Feature Reqests).

User Needs: Intuitive way to raise and track their issues through to completion

Opportunities/Problems table used to determine the strategic priorities UX efforts should address (in this order):

| Opportunity/Problem                             | Importance | Viability/Feasibility |
| ----------------------------------------------- | :--------: | :-------------------: |
| A. Track bugs and feature requests              |     5      |           5           |
| B. Contribute to to the closing of open tickets |     5      |           5           |
| C.                                              |     2      |           4           |
| D.                                              |     1      |           2           |

### Scope

#### Functional Specifications

In considering functional specifications, existing ticket and bug trackers were researched, including GitHub Issues, Jira. This helped to identify the key data fields and features users expect to see.

Feature Set:

- Tickets View: Filterable, sortable table of tickets.
- Raise Ticket: Raise a bug or feature.
- Edit Ticket: Edit own ticket if submitter, or any ticket if staff.
- Cancel Ticket: Cancel ticket if submitter, or any ticket if staff.
- Kanban (PRO) View: This popular agile tool provides a more visual representation tickets.
- Dashboard View: See various charts at a glance.
- Account View: Update personal details, including Profile Image.
- Checkout: Make a once-off credit card payment (Stripe) to unlock KANBAN view and unlimited ticket submissions.

#### Content Requirements

In order to provide the value of the above features, the following content is required:

- Input boxes for ticket filtering
- DC.js, D3.js and Crossfilter for charts on dashboard page.
- Dropdowns for adding and editing ticket fields.

### Structure

#### Interaction Design

Consistency & Predictability:

- A consistent colour scheme and navigation bar is present throughout the site.
- On smaller devices, navigation links collapse into 'burger' button

Feedback:

All interactive elements provide feedback to the user to encourage interaction and provide confirmation when actions are taken.

- Sort by dropdown has border transition on hover.
- Each record in tickets table changes colour opacity and cursor on hover.
- 'Upvote' button changes colour on hover.
- Navigation and pagination links change colour on hover.
- All buttons have border transition on hover.
- Form validation exists for relevant fields - field displays red 'Required' if invalid, green if valid.
- Django Messages are briefly displayed just under navbar to confirm user actions (eg after Login, Logout, Add Ticket, Edit Ticket, Upvote, Comment, Payment).

#### Information Architecture

The filtering and sorting panel is located on the left, a logical and intuitive position expected by users.

Pagination

Sections are on separate pages for to aide...

### Skeleton

#### Wireframes

Two sets of wireframes were created in the early development stage to inform the structure and layout for different device sizes.

[Desktop & Mobile Wireframes](https://github.com/tdunn891/milestone-4)

### Surface

Colours: A minimal, subtle colour scheme was employed so as not to distract from the main content.

Fonts: Easily readable font was a key consideration.

### User Stories

User stories:

- User 1 - "As a user who is only interested in tickets I have submitted myself, I want quick access to just my tickets."
- User 2 - "As a team leader who needs to see the status of aging high priority tickets, I want to graphically see which tickets need attention to close."
- User 3 - "As a user who prefers KANBAN-style columns for intuitive task tracking I would like the option to view my tickets in KANBAN view."
- User 4 - "As a user who can contribute to the resolution of an issue, I want to be able to leave a comment under a ticket."
- User 5 - "As a user who wants wants to draw attention to an existing ticket, I want to be able to upvote."
- User 6 - "As a team leader who wants to follow up with the assignee of a ticket, I want to be able to start an email from the ticket view."

## Features

### Existing Features

Users can:

- Feature 1: Submit a ticket - Bug or Feature Request.
- Feature 2: Edit their own ticket. Staff members can edit all tickets.
- Feature 3: View, search and filter list of tickets submitted by all users.
- Feature 4: View any ticket in detail, including Recent Activity.
- Feature 4: Upvote any ticket.
- Feature 5: Leave a comment on any ticket.
- Feature 6: View list of other users and their details.
- Feature 7: Update their own details, including First Name, Last Name, Zoom Meeting ID
- Feature 8: Upload a profile image.
- Feature 9: Derive ticket insights in interactive Dashboard view.
- Feature 10: View tickets in KANBAN View (PRO Feature).

### Features Left to Implement

- Potential Feature 1: Add filters in KANBAN View, including a toggle to show only My Tickets.
- Potential Feature 2: Limit upvotes to 1 per user per ticket. Add tooltip to upvote button listingj users who have upvoted.
- Potential Feature 3: Add phone number field to user profile with ability to click to call via 'callto:'.
- Potential Feature 4: Additional graphs in Dashboard view, including Age vs Priority bubble chart.
- Potential Feature 5: Make tickets in KANBAN View draggable, so that ticket status can be changed via dragging into other column.

## Database

Sqlite3 was used during development. For deployment, data was migrated to PostgreSQL.

### Data Models

#### Accounts App

User Model

The standard Django User model was employed: django.contrib.auth.models

In order to record additional user fields, a Profile model was used.

Profile Model

| Field               | Type          | Description                                          |
| :------------------ | :------------ | :--------------------------------------------------- |
| is_pro_user         | BooleanField  | If user has paid to upgrade to PRO account.          |
| pro_user_since_date | DateTimeField | Records date user went PRO.                          |
| image               | ImageField    | Profile image, which is referred to throughout site. |
| zoom_id             | CharField     |                                                      |

#### Tickets App

Ticket Model

| Field         | Type                          | Description                                                 |
| :------------ | :---------------------------- | :---------------------------------------------------------- |
| ticket_type   | CharField                     | 'Bug','Feature'                                             |
| summary       | CharField                     | Short summary of ticket                                     |
| created_date  | DateTimeField                 |                                                             |
| resolved_date | DateTimeField                 | Date and time set recorded when ticket is set to 'Resolved' |
| priority      | CharField                     | 'Low', 'Medium', 'High'                                     |
| submitted_by  | ForeignKey(User)              | Linked to User instance                                     |
| assigned_to   | ForeignKey(User)              | Linked to User instance                                     |
| description   | TextField                     |                                                             |
| tags          | 'TaggableManager' Django App  | External app to save comma-separated tags.                  |
| upvotes       | IntegerField                  | Count of upvotes.                                           |
| screenshot    | ImageField                    | Image file related to ticket.                               |
| history       | 'HistorialRecords' Django App | External app to record field changes.                       |

Comment Model

| Field        | Type               | Description                      |
| :----------- | :----------------- | :------------------------------- |
| ticket       | ForeignKey(Ticket) | Linked to Ticket instance        |
| user         | ForeignKey(User)   | Linked to User instance          |
| comment_body | CharField          | Comment body text                |
| date         | DateTimeField      | Date and time comment was posted |

Django REST Framework

An API was set up to form the tickets data source of the dashbord graphs.

#### Checkout App

Order Model

| Field           | Type      | Description |
| :-------------- | :-------- | :---------- |
| full_name       | CharField |             |
| phone_number    | CharField |             |
| country         | CharField |             |
| postcode        | CharField |             |
| town_or_city    | CharField |             |
| street_address1 | CharField |             |
| street_address2 | CharField |             |
| county          | CharField |             |
| date            | DateField |             |

OrderLineItem Model

| Field    | Type              | Description |
| :------- | :---------------- | :---------- |
| order    | ForeignKey(Order) |             |
| product  | CharField         |             |
| quantity | IntegerField      |             |

## Technologies Used

- [Autoprefixer CSS Online](https://autoprefixer.github.io/) : used to add vendor prefixes.
- [Balsamiq](https://balsamiq.com/) : used to create wireframes.
- [Bootstrap](https://bootstrap.com/) : used for responsive webpages.
- [Chrome Developer Tools](https://developers.google.com/web/tools/chrome-devtools) : used extensively to ensure device responsiveness.
- [crossfilter](https://github.com/crossfilter/crossfilter) : enables filters to be applied to all graphs.
- [CSS3](https://www.w3.org/Style/CSS/Overview.en.html) : styling language.
- [d3js.org](https://d3.js) : Javascript charting library.
- [DataTables.net](https://datatables.net) : used for pagination and filtering of tables.
- [dc.js](https://dc.js) : charting Javascript libary built on d3.js.
- [Django Crispy Forms](https://django-crispy-forms.readthedocs.io/) : used for Django form styling.
- [Django REST Framework](https://www.django-rest-framework.org/) : used for as API data source for dashboard charts.
- [Django Simple History](https://django-simple-history.readthedocs.io) : used for tracking changes to model fields.
- [Git](https://git-scm.com/) : used for version control.
- [GitHub](https://github.com) : code repository and source branch used in deployment.
- [Google Fonts](https://fonts.google.com/) : used for placeholder.
- [Heroku](https://www.heroku.com) : used for deployment.
- [HTML5](https://www.w3.org/html) : used for page structure.
- [JavaScript](https://developer.mozilla.org/en-US/docs/Web/JavaScript) :
- [jQuery](https://jquery.com/) : used to select and manipulate HTML elements.
- [Material Icons](https://material.io/) : used for icons and fonts.
- [Pillow](https://pillow.readthedocs.io) : used for proccessing images in database.
- [PostgreSQL](https://www.postgresql.org/) : used as relational database in production.
- [Stripe](https://stripe.com/) : used to accept payments.
- [Travis](https://travis-ci.org) : used for continuous integration.
- [VSCode](https://code.visualstudio.com) : preferred code editor.
- [W3C Validator](https://jigsaw.w3.org) : used to validate HTML & CSS.

## Testing

Extensive automatic and manual testing was conducted to ensure the site functions and looks well on all major browsers (Chrome, Firefox, Safari, Edge) and device sizes.

### Automated Testing

- Django testing framework was used.

### Desktop Testing (Manual)

The following manual tests passed:

Index Page

- If Basic user is logged in, 3 'Go PRO' buttons are displayed.
- If Pro user is logged in, 3 'Go PRO' buttons are hidden.

Tickets Page

- Global search input filters in all fields.
- Reset filters button reloads page.
- All field-specific search boxes filter correctly.
- Clicking headings orders by that field. Clicking again changes order direction.
- Pagination and 'Show x tickets' per page functions correctly.
- All columns are visible or accessible via horizontal scroll.
- Tooltips function on hover of Summary, Type, Status.
- Row colours represent status.
- Raise Ticket button takes user to Add Ticket page.

Dashboard Page

- All 6 charts display with adequate padding.
- All 6 charts be filtered on click, or range selection.
- Display updates to show how many tickets are filtered - eg. 12 of 25 Tickets.

KANBAN Page

- If user is not PRO user, redirect to Checkout page.
- 'Hide Cancelled' checkbox toggles Cancelled column.
- Ticket count and counts for each column (ticket status) are correct.
- Quick update status.

Add Ticket page

- If Basic user, message is displayed shows how many tickets have been submitted out of 10 in the current month. If limit has been reached, message is displayed and user is redirected to checkout page.
- Form is valid and submits even if Tags and Screenshot is blank.

View Ticket page

- Jumbotron colour correctly represents ticket status.
- Submitter and Assignee pill badges show user profile pictures if any, and on click a drop-right menu with 'mailto:' links Zoom links functioning.
- Upvote button shows upvote count and increments by 1 on click.
- On click, Quick Status dropdown links update the ticket status and display confirmation message.
- Edit ticket button takes user to the Edit Ticket form.
- If screenshot exists, following link shows the screenshot in a modal. Download button downloads image.
- Comments can be submitted.

Edit Ticket page

- Only submitter or staff can edit a ticket.
- Fields are pre-filled with existing values.
- Submitting form updates all fields.

Account page

- User Profile image can be changed via upload. Image is displayed with rounded border.
- First Name, Last Name can be updated via edit button.
- If user not Staff, requesting staff access button is displayed, which on click enables Staff access. Note: In a live environment, these requests would be sent to Admin for review before granting permission. For assessment purposes this permission is granted immediately so assessors can edit all tickets.
- Member Since and PRO Since (if PRO) shows correct dates.
- On click of Zoom Meeting ID, Zoom Personal Meeting Room is launched.

404 Error Page

- When an incorrect URL is entered, 404 Page is displayed
- Return home button takes user back to Home Page
- Navigation buttons function

### Mobile and Tablet Tests (Manual)

The above Desktop Tests were also conducted on mobile and tablet devices (via Chrome DevTools). In addition, the following mobile and tablet-specific tests were run:

Dashboard (Mobile)

- All graphs on dashboard page are readable.

The following tests failed:

| Issue No. | Test Name                                       | Issue                                   | Resolved? | Action Taken                                                            |
| :-------- | :---------------------------------------------- | :-------------------------------------- | :-------- | :---------------------------------------------------------------------- |
| 1         | Content is not squeezed or overlapping (Mobile) | Tickets table overflowing horizontally. | Yes       | Added Bootstrap class 'table-responsive' to enable horizontal scrolling |

### Code Validation

| Code                                                            | Result |
| :-------------------------------------------------------------- | :----- |
| CSS ([W3C](https://jigsaw.w3.org/css-validator/))               | PASS   |
| HTML ([W3C](https://validator.w3.org/))                         | PASS   |
| Javascript with no major errors ([jshint](https://jshint.com/)) | PASS   |
| Python ([jshint](https://pep8online.com/))                      | PASS   |

^ The following classes of errors were deemed not applicable, as the validator did not take into account Flask and Jinja templating:

## Deployment

### Heroku

The application was deployed to Heroku, via the following steps:

1. Ensure `requirements.txt` reflects all dependencies via `pip freeze > requirements.txt`
2. Create `Procfile` via `echo web: python app.py > Procfile`
3. `git add` above files, then commit and push to GitHub.
4. Heroku.com > Create new app > App name: django-issue-tracker-1, Region: Europe
5. Deploy > Deployment method > Link GitHub account
6. Select repository 'milestone-4'
7. Select branch: 'master'
8. Set Config Vars: Heroku Settings > Config Vars:

| Config Var            | Key                     |
| :-------------------- | :---------------------- |
| DATABASE_URL          | 'postgres database url' |
| DISABLE_COLLECTSTATIC | 1                       |
| SECRET_KEY            | 'your secret key'       |
| STRIPE_PUBLISHABLE    | 'from stripe'           |
| STRIPE_SECRET         | 'from stripe'           |

9. Manual Deploy > Deploy Branch (master)
10. Heroku Website > Open App

### Local Deployment

1. 'Clone or download' repository from https://github.com/tdunn891/milestone-4, or from command line:

   `git clone https://github.com/tdunn891/milestone-4`

2. If your IDE doesn't include a virtual environment, create one (see Python docs: [Creation of virtual environments](https://docs.python.org/3/library/venv.html):

   `python3 venv /path/to/new/virtual/environment`

3. Activate virtual environment:

   `source /path/to/new/virtual/environment`

4. Install dependencies in requirements.txt via 'pip':

   `pip -r requirements.txt`

5. Create local environment variables in project directory:

   `touch env.py`

   Import os at top of file, then set each environment variable default:

   `os.environ.setdefault("<variable>",<value>)`

| Config Var            |
| :-------------------- |
| DATABASE_URL          |
| DISABLE_COLLECTSTATIC |
| SECRET_KEY            |
| STRIPE_PUBLISHABLE    |
| STRIPE_SECRET         |

6. Run app:

   `python3 manage.py runserver`

7. Go to Local Host in browser to view:

   `http://127.0.0.1:8000/`

## Credits

### Content

All icons sourced from [Material Icons](https://material.io/resources/icons).

### Media

Images

### Acknowledgements

YouTube Tutorials: Pretty Printed

Big thanks to friends and family for help with testing and feedback.
