## CS50's Web Programming with Python and JavaScript

# Project 5 - Capstone

# _CourseMedia_: An Online Courses Platform

## Table of Content

1. [Introduction](#1-introduction)
1. [Distinctiveness and Complexity](#2-distinctiveness-and-complexity)
1. [What’s contained in each file](#3-whats-contained-in-each-file)
1. [How to run this application](#4-how-to-run-this-application)
1. [About this web application](#5-about-this-web-application)

## 1. Introduction

This web application consists of an online courses platform, where instructors can create courses with their corresponding quizzes, and students can enroll in those courses and take their quizzes: they pass or fail depending on the grade they have got. For specific courses, a certificate is granted upon completion and can be downloaded by the students. Every user has their own profile in which (depending on the user's role) several actions can be performed.

## 2. Distinctiveness and Complexity

In order to prove the **distinctiveness** and **complexity** of this project compared to the previous 5 projects of this course, I will list 10 key features I implemented:

1. **Forget Password Feature:** From specifying the 4 url paths Django provides for this feature along with their corresponding views functions, to customizing their 4 HTML templates, all the way to customizing the email template that is sent to users. Lastly, I ran an SMTP server on the console in order to test this whole process (by specifying EMAIL_BACKEND in settings.py).

1. **Custom User Model:** For the user model, I inherited from **AbstractUser()** class, and I added some extra user information in the same model. For that reason, I specified **REQUIRED_FIELDS**, which is "_a list of the field names that will be prompted for when creating a user via the createsuperuser management command_" (as mentioned [here](https://docs.djangoproject.com/en/4.2/topics/auth/customizing/)). This list should include any field name that can not be blank, in order to avoid errors while creating the superuser.

1. **File Upload Feature:** Specify in which directory to store the uploaded files (specify both **MEDIA_ROOT** in `settings.py` and **upload_to()** parameter in **ImageField()** class in `models.py`), and specify the url to access the uploaded file (**MEDIA_URL** in `settings.py`), and finally setting the **enctype** attribute inside the form tag in HTML to **multipart/form-data**.

1. **Compress Images Before Saving Them:** Overriding the save function in a Django Model and using the `Pillow` python module in order to compress uploaded images before saving them.

1. **Create a PDF File and Let Users Download It:** Used the `ReportLab` Python library in order to create a PDF file. Then I used Django's **FileResponse()** class with its **as_attachment** parameter set to True, in order to "_ask the browser to offer the file to the user as a download_" (as mentioned [here](https://docs.djangoproject.com/en/4.2/ref/request-response/)).

1. **Sort, Filter and Search Features:** In one of the web pages, where all objects of a given model are displayed, I implemented a complex sort/filter/search feature using: API call with Javascript, a Django views function to describe what should happen when that API is called, and the **HTML template tag** to display sorted and filtered objects.
   When sort and/or filter are applied by the user, I gather the sort and filter options selected and I make an API call with the sort and filter information as GET parameters in the url. In the backend, I extract the sort and filter information and I send a JsonResponse containing sorted and filtered serialized objects. When the API response is received in JavaScript, I populate, for every object, the content of the template tag created in HTML in order to add the sorted and filtered objects in the DOM.
   Lastly, I take into consideration the search query typed by the user (if there is any) to decide which objects to display on the web page.

1. **Used [DataTables](https://datatables.net/) To Create Interactive and Responsive HTML Tables:** I used DataTables (which requires jQuery) which applies a certain styling and enables sort/filter/search within the data of the table. I used [data rendering](https://datatables.net/examples/basic_init/data_rendering.html), which helped me customise how the data is displayed in the cells (changing text color, adding links to the text), as well as specifying what information DataTables will use in order to sort and filter the data of the table.

1. **Create Dynamic Form, Saving Its Data in JSON Format and Represent This JSON Data in an HTMl File:** Using JavaScript and **template tag** in HTML, I created a dynamic form in one of the web pages. In fact, there is a button at the end of the form, everytime it is clicked, a new section of the form is displayed.
   When the form is submitted, I extract all field values, apply some checking and merge them into a single data structure which is then saved to a JSON file.
   At a certain point in the web application, I load the content of the JSON file into a python dictionary and I represent that data in an HTML file.

1. **Responsive Web Application:** This web application is fully responsive, as I used CSS media queries to adapt the styling of the web application on different viewport sizes, from mobiles to screens above 1536px wide.

1. **Light Mode / Dark Mode:** Users can switch between Light mode and dark mode depending on their preference.

## 3. What’s Contained In Each File

E-Learning-Platform is the root directory. Here is the listing of the files/directories I created/added code in it:

- **requirements.txt:** This file contains Python packages that need to be installed in order to run this web application.
- **README.md**
- **quizzes directory:** This directory contains the quizzes files in JSON format. Every file is named by the {course instructor's username}\_{course id}.
- **media directory:** This directory contains 2 sub-directories:
  - **certificate_images directory:** Contains 2 image files that are necessary when I generate a course's certificate PDF file.
  - **courses_images directory:** The course's images are stored in this directory.
- **elearning directory:** Django project directory. The 2 files in this directory in which I added some code are:
  - **settings.py:** Specify the **MESSAGE_TAGS** dictionary, in which I assigned each Django message tag with a corresponding class. I also specified **MEDIA_ROOT** and **MEDIA_URL** for the upload files functionality, and **QUIZES_ROOT** to specify in which directory to store the courses' quizzes. Finally I specified **EMAIL_BACKEND** for running an SMTP server on the console.
  * **urls.py:** Specify the path to this Django application.
- **courses_platform directory:** Django app directory. It contains:
  - **static/courses_platform directory:** Contains css and js files divided in 2 directories: **components** directory which contains css and js files responsible of some components of specific web pages, and **pages** directory in which there are css and js files responsible of a whole web page.
    Additionally, in the static/courses_platform directory there are 3 css files:
    - **modern-normalize.css:** Normalize browsers' default style. Includes only normalizations for the latest Chrome, Firefox, and Safari ([source](https://github.com/sindresorhus/modern-normalize)).
    - **styles.css:** Defines variables for font size and colors, and style various HTML elements: body, input, textarea, select, button, image, and anchor.
    - **utils.css:** Mainly specify the styling of "my-container" class on different viewport sizes. It's a class given to the div element that wraps the entire body content of every web page in this web app.
  - **templates/courses_platform directory:** This directory contains all the HTML files of every web page in this web app, along with one directory named **includes** which contains **messages.html** where there is the HTML code of success/error/warning messages that appear to the user.
  - **urls.py:** Specify the paths required for the web app, along with their corresponding views function and name.
  - **views.py:** Defines Django forms and every views function is defined in this file.
  - **models.py:** Defines 2 models: User model and Course model. The fields in every model and the relationship between them is shown in the figure below.
    ![Image that shows the models, their fields and the relationship between the fields](images/database.png "Image showing the models, their fields and the relationship between the fields")
  - **admin.py:** Specify for every model, what fields to show in the admin interface.
  - **tests.py:** Define tests for the models and the relationship between them.

## 4. How to run this application

- Clone this repository
- `cd` into the root directory (E-Learning-Platform)
- Run the following command: `pip install -r requirements.txt`
- And finally, run the following command: `python manage.py runserver` and open the provided url in your browser

  I will provide 2 account credentials to sign in:

  - **An instructor account:** username: Christopher and Password: christopher
  - **A student account:** username: Jad and Password: jad

    Please note that the first letter of both usernames starts with an uppercase letter, however the first letter of both passwords starts with a lowercase letter.

## 5. About this web application

I will start by talking about some components in the web app that are common in all web pages.

- **Header Menu:** The header menu contains links that may change from a web page to another, and if there is a logged in user or not. The header menu is responsive: on small screen sizes it collapses into a hamburger menu.

- **Footer:** a basic footer with dummy infos that is always placed on the bottom of any page even when the page's content doesn't fill the page.

- **Courses Representation:** Every course in this web application is represented by a card, that displays the course's image, title, duration and level. When the card is clicked, users are taken to the **course page**.

In the following section, I will list all the web pages of this web app, and I will explain what each web page consists of.

- **Index Page:** Contains the following sections:
  - The first section greets the user, or provides a sign in / sign up link if no user is logged in.
  - "Our Top Courses section", that displays the 6 courses that have the most enrolled students. An `Explore All Courses` button takes users to the **all courses page**.
  - "About us" and "Connect With Us" sections.

* **Sign In Page:** Users type their username and password to sign in. There is a "Forgot your password?" link that let users reset their passwords. (see first point in [Distinctiveness and Complexity section](#2-distinctiveness-and-complexity) for implementation details)

* **Sign Up Page:** to sign up, users should provide their: first name, last name, username, email. They should also specify their role (student or instructor), and only if they choose the instructor option, the "Title" field appears, where instructors should specify their titles (i.e. Software Engineer at Example Company). Lastly, there is the "about Me" section, where users should introduce themselves and talk about their interests.

* **All Courses Page:** this page displays all courses available on the platform. Courses are sorted alphabetically (A->Z) by default.

  - Users can **search** for courses by _title_, by typing in a search query.
  - Users can **sort** courses _alphabetically from A->Z_, _alphabetically from Z->A_, by _most recent_ (depending on the course's creation date) and by _popularity_ (from the course with the highest number of enrolled students, to the least one).
  - Users can **filter** courses by _category_, _duration_, _language_ and _level_. More than one filter option can be applied at the same time.

    All 3 features work together, i.e. users can apply sort **and** filter options together at the same time, and if there is a search query typed, this will be taken into consideration before displaying to the user the sorted and/or filtered courses.

* **Course Page:** this page contains all information related to the course.
  First, here is the list of elements of that page that are always displayed, wether there is no logged in user, or wether the logged in user is a student or an instrutor:

  - Image
  - Title
  - Small description
  - Total number of students enrolled
  - Duration
  - Level
  - Language of teaching
  - If a certificate upon completion is provided or not
  - About this course, which is a detailed description of the course's content
  - Prerequisite: which is another course teached by the same instructor. Users can click on the prerequisite course and see its page.
  - Instructor: Users can click on the instructor name and go to its profile page.

  **If there is no logged in user:**

  - a `Log In to Enroll` button that takes users to the sign in page.

  **If the logged in user is a student:**

  - Similar courses section (if any): Only if there are courses from the same category, this section is displayed and contains 3 courses from the same category.

    **if the student is not enrolled in that course:**

    - an `Enroll Now` button: when clicked, the logged in user becomes enrolled in that course.

    **if the student is enrolled in that course:**

    - `Go to Course Content` button that takes the student to the course's content (this button is not functional for now, as I did not inlude courses contents for this project).

      **if the student did not take/pass the quiz yet:**

      - `Take the quiz` button that takes the student to the course's quiz page.

      **if the student passed the quiz of that course:**

      - "You completed this course!" phrase
      - `Download Certificate` button: when clicked, a certificate (PDF file) is downloaded for the user. For more infos on the implementation of this feature, see the fifth section in [Distinctiveness and Complexity](#2-distinctiveness-and-complexity) section above.

  **If the logged in user is an instructor:**

  - **if the instructor is the creator of that course:**

    - `Go to Course Content` button that should take the instructor to the course's content.
    - "Enrolled Students" section: this section contains a table created with [DataTables](https://datatables.net/) (for more infos on the implementation, see point 7 in [Distinctiveness and Complexity](#2-distinctiveness-and-complexity) section above). This table lists the usersame, first name and last name of all enrolled students. Instructors can click on a username and go to the student's profile page. Additionally, it shows the status of every enrolled student: if the student passed the quiz of that course, "Passed" is displayed. Otherwise "Enrolled" is displayed.

  - **if the instructor is not the creator of that course:** the view of that page is similar to the view if there is no logged in user, but without the `Log In to Enroll` button.

* **Instructor Profile Page:** There are 2 views for that page: the instructor is visiting their own profile page, or any other user accessing that page. Both views have the same components, which are the details about the instructor: the full name (followed by a medal icon if the instructor have 4+ enrolled students on the total of their courses), title, "about me", as well as the listing of the courses taught by that instructor. When the instructor visits their own profile, there are 2 additional buttons: `Edit Profile` which takes to the **Edit Profile Page**, and `New Course` which takes to the **Create Course Page**.

* **Create Course Page:** in that page, instructors can create a new course. They should specify its attributes such as the title, duration, level, etc., as well as a prerequisite: they choose one of the courses they teach to be a prerequisite for that new course. In addition to that, there is the "Create a Quiz" section. Instructors should create a quiz that consists of single choice questions. First, they specify the passing grade in percentage. Then they start by filling informations related to the first question of that quiz: question body, options (comma seperated), the index of the correct option. After that, instructors can add as many questions as they want, by clicking on the `Add a question` button. Every time this button is clicked, a new question section appears (for details about this implementation,see the 8th point in [Distinctiveness and Complexity](#2-distinctiveness-and-complexity) section above). The `Publish Course` button should be clicked to publish the course.

* **Quiz Page:** by clicking on the `take the quiz` button from a course's page, the student will be taken to the quiz page. On that page, the student can read the instructions of the quiz and the passing grade. After that, every question is displayed followed by its options, and students can only choose one option. Students click on the `Submit` button to submit their responses. 2 scenarios can happen here:

  - **Fail The Quiz:** the grade of the student is displayed, followed by `retake the quiz` button that re-display the quiz. Students can retake the quiz as many times as needed until they pass it. There is also a link that takes the student back to the course's page.
  - **Pass The Quiz:** A confetti animation starts and lasts for 5 seconds. The grade of the student is displayed, followed by a link to go back to the course's page.

* **Student Profile Page:** the student's profile page displays the first name and last name, followed by a trophy icon if the student completed 2+ courses. Next, there is the month and year of joining the platform and the about me section. When students visit their own profile, there is the additional `Edit Profile` button which takes to the **Edit Profile Page**. There is also 2 sections in that page:

  - **Completed courses:** the number of completed courses is displayed. If that number is greater than 0, a maximum of 2 completed courses titles (on small screens) or cards (on bigger screens) are displayed. If there are more than 2 completed courses, a _See all completed courses_ link will be displayed. This link takes to the **completed courses page** where all completed courses cards are displayed. At the top of that page, there is a link that takes users back to the student profile page.
  - **Currently enrolled courses:** the number of enrolled but not passed courses is displayed. The display of this section is similar to the completed courses section.

* **Edit Profile Page:** the `Edit Profile` button takes students or instructors to that page. They can edit their first name, last name, title (for instructors), and their "about me" section. Username and email fields are present as disabled fields that can not be edited. When the `Save Changes` button is clicked, the changes are saved in the database.
