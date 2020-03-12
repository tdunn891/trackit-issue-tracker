## Project Purpose

TrackIt was developed to allow simple, effective tracking of tickets.

## UX

### Strategy

Site Objective: Provide platform to track tickets (Bugs and Feature Reqests).

User Needs: Intuitive way to raise and track their issues through to completion

Opportunities/Problems table used to determine the strategic priorities UX efforts should address (in this order):

| Opportunity/Problem                | Importance | Viability/Feasibility |
| ---------------------------------- | :--------: | :-------------------: |
| A. Track bugs and feature requests |     5      |           5           |
| B. b                               |     5      |           5           |
| C. c                               |     2      |           4           |
| D. d                               |     1      |           2           |

### Scope

#### Functional Specifications

In considering functional specifications, I researched existing ticket and bug trackers, including GitHub issues, placeholder. This helped to identify the key data fields and features users expect to see.

Feature Set:

- Tickets View: Filterable, sortable table of tickets.
- Raise Ticket: Ability to raise a bug or feature.
- Edit Ticket: Ability to edit own ticket if submitter, or any ticket if staff.
- Cancel Ticket: Ability to cancel ticket if submitter, or any ticket if staff.
- Kanban View: This popular agile tool provides tickets in a more visual way.
- Dashboard View: Ability to see various charts at a glance.

#### Content Requirements

In order to provide the value of the above features, the following content is required:

- Checkboxes for filtering
- Dropdowns for sorting and for form input

### Structure

#### Interaction Design

Consistency & Predictability:

- A consistent colour scheme and navigation bar is present throughout the site
- On smaller devices, navigation links collapse into 'burger' button

Feedback:

All interactive elements provide feedback to the user to encourage interaction and provide confirmation when actions are taken.

- Checkbox labels change colour on hover.
- Sort by dropdown has border transition on hover.
- Each record in the table changes background colour and cursor on hover.
- 'Like' button changes colour on hover.
- Icons: medal, timer, water temp provide tooltip additional information on hover.
- Navigation links change colour on hover.
- Pagination links have background colour change on hover.
- All buttons have border transition on hover.
- All buttons have wave effect on click.
- Form validation exists for relevant fields - field displays red 'Required' if invalid, green if valid.
- 'Toast' messages are briefly displayed to show confirmation of user actions.

#### Information Architecture

The filtering and sorting panel is located on the left, a logical and intuitive position expected by users.

Pagination

Sections are on separate pages for to aide...

### Skeleton

#### Wireframes

Two sets of wireframes were created in the early development stage to inform the structure and layout for different device sizes.

[Desktop & Mobile Wireframes](placeholder)

### Surface

Colours:

Fonts:

### User Stories

User stories:

- User 1 - "As a user who
- User 2 - "As a user who
- User 3 - "As a user who
- User 4 - "As a user who
- User 5 - "As a user who

How their needs are met:

- User 1's needs are met by the ability to
- User 2's needs are met by the ability to
- User 3's needs are met by the ability to
- User 4's needs are met by the ability to
- User 5's needs are met by the ability to

## Features

### Existing Features

- Feature 1: User can view brews and apply filters and sorting. Clicking on a brew reveals additional information, including brewer position, brew time, water temperature and process
- Feature 2: User can contribute a brew. Range sliders and dropdown boxes were employed for input validation purposes, which is essential for effective filtering and sorting
- Feature 3: User can edit an existing brew
- Feature 4: User can delete an existing brew. On click of delete button, a modal is presented to ask for confirmation
- Feature 5: User can 'like' a brew, which increments the likes count by 1

### Features Left to Implement

- Potential Feature 1:
- Potential Feature 2:
- Potential Feature 3:
- Potential Feature 4:

## Database

The relational SQL database sqLite was employed.

### Tables

The database has the following tables:

| Field   | Type     | Description                   |
| :------ | :------- | :---------------------------- |
| \_id    | ObjectId | ID is auto-created by MongoDB |
| barista | String   | Name of barista or user       |

## Technologies Used

- [Autoprefixer CSS Online](https://autoprefixer.github.io/) : used to add vendor prefixes.
- [Balsamiq](https://balsamiq.com/) : used to create wireframes.
- [Bootstrap](https://bootstrap.com/) : used for responsive webpages.
- [Chrome Developer Tools](https://developers.google.com/web/tools/chrome-devtools) : used extensively to ensure device responsiveness.
- [CSS3](https://www.w3.org/Style/CSS/Overview.en.html) : styling language.
- [Favicon Generator](https://www.favicon-generator.org) : used to create a 16x16 icon, displayed next to page title in browser.
- [Git](https://git-scm.com/) : used for version control.
- [GitHub](https://github.com) : used to host code repository and to deploy project (via GitHub Pages).
- [Google Fonts](https://fonts.google.com/) : used for placeholder.
- [HTML5](https://www.w3.org/html) : used for page structure.
- [JavaScript](https://developer.mozilla.org/en-US/docs/Web/JavaScript) :
- [jQuery](https://jquery.com/) : used to select and manipulate HTML elements.
- [Material Icons](https://material.io/) : used for icons and fonts.
- [VSCode](https://code.visualstudio.com) : preferred code editor.
- [W3C Validator](https://jigsaw.w3.org) : used to validate HTML & CSS.

## Testing

Extensive automatic and manual testing was conducted to ensure the site functions and looks well on all major browsers (Chrome, Firefox, Safari, Edge) and device sizes.

### Automated Testing

- placeholder

### Desktop Testing (Manual)

Brew Browser Page

- placeholder

Add Brew page

- placeholder

Edit Brew page

- placeholder

404 Error Page

- When an incorrect URL is entered, 404 Page is displayed with image
- Return home button takes user back to Home Page
- Navigation buttons function

### Mobile and Tablet Tests (Manual)

The above Desktop Tests were also conducted on mobile and tablet devices (via Chrome DevTools). In addition, the following mobile and tablet-specific tests were run:

Brew Browser Page (Mobile)

- placeholder

The following tests failed:

| Issue No. | Test Name                                       | Issue                                                                        | Resolved? | Action Taken                                                             |
| :-------- | :---------------------------------------------- | :--------------------------------------------------------------------------- | :-------- | :----------------------------------------------------------------------- |
| 1         | Content is not squeezed or overlapping (Mobile) | Brew Browser table has overlapping horizontal content, even with small text. | Yes       | Added materialise class 'hide-on-med-and-down' to bean and grinder icons |

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

1. Heroku.com > Create new app > App name: aeropress-hub, Region: Europe
2. Deploy > Deployment method > Link GitHub account
3. Select repository 'milestone-4'
4. Select branch: 'master'
5. Set Config Vars: Heroku Settings > Config Vars:
   - IP: 0.0.0.0
   - PORT: 5000
   - !UPDATE! MONGO_URI: mongodb+srv://[user]:[password]@myfirstcluster-bgxgx.mongodb.net/aeropress?retryWrites=true&w=majority
6. Manual Deploy > Deploy Branch (master)
7. Heroku Website > Open App

### Local Deployment

1. 'Clone or download' repository from https://github.com/tdunn891/milestone-4, or from command line:

   `git clone https://github.com/tdunn891/milestone-4`

2. If your IDE doesn't include a virtual environment, create one (see Python docs: [Creation of virtual environments](https://docs.python.org/3/library/venv.html):

   `python3 venv /path/to/new/virtual/environment`

3. Activate virtual environment:

   `source /path/to/new/virtual/environment`

4. Install dependencies in requirements.txt via 'pip':

   `pip -r requirements.txt`

5. Run app:

   `python3 app.py`

6. Go to Local Host in browser to view:

   `http://127.0.0.1:5500/`

## Credits

### Content

### Media

Images
Icons

### Acknowledgements

Tutorials

Big thanks to friends and family for help with testing and feedback.
