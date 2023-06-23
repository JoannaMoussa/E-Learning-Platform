## CS50's Web Programming with Python and JavaScript

# Project 5 - Capstone

# _CourseMedia_: An Online Courses Platform

This web application consists of an online courses platform, where instructors can create courses and their appropriate quiz, and students can enroll in those courses and pass them if they get a grade equal or above the passing grade defined by the instructor.

## Distinctiveness and Complexity

In order to prove the **distinctiveness** and **complexity** of this project compared to the previous 5 projects of this course, I will list 10 key features I implemented:

- **Forget Password Feature:** I learned how to implement the forget password feature. From specifying the 4 URL paths Django provides for this feature along with their appropriate views functions, to customizing their 4 appropriate HTML templates, all the way to customizing the email template that is sent to users. Lastly, I ran an SMTP server on the console in order to test this whole process (by specifying EMAIL_BACKEND in settings.py).

- **Used a custom user model:** For the user model, I inherited from `AbstractUser()` class, and I added some extra user information in the same model. For that reason, I specified `REQUIRED_FIELDS`, which is "_a list of the field names that will be prompted for when creating a user via the createsuperuser management command_" (as mentioned [here](https://docs.djangoproject.com/en/4.2/topics/auth/customizing/)). This list should include any field name that can not be blank, in order to avoid errors while creating the superuser.

- **Let users upload an image:** I learned how to add the feature of file upload in my web application. From specifying to Django in which directory I want to store the uploaded files (specify both `MEDIA_ROOT` in `settings.py` and `upload_to()` parameter in `ImageField()` class in the model), to specifying the URL to access the uploaded file (`MEDIA_URL` in `setting.py`), all the way to setting the `enctype` attribute inside the form tag in HTML to `multipart/form-data`.

- **Compress images before saving them:** I overrode the save function in a Django Model and used the `Pillow` python module in order to compress uploaded images before saving them.

- **Create a pdf file and let users download it:** I learned how to use the `ReportLab` Python library in order to create a pdf file. Then I used Django's `FileResponse()` class with its `as_attachment` parameter set to True, in order to "_ask the browser to offer the file to the user as a download_" (as mentioned [here](https://docs.djangoproject.com/en/4.2/ref/request-response/)).

- **Sort, Filter and Search Features:** In one of my web pages, where all objects of a given model are displayed, I implemented a complex sort/filter/search feature using API call with Javascript, a Django views function to describe what should happen when that API is called, and the HTML template tag to display sorted and filtered objects.
  When sort and/or filter are applied by the user, I gather the sort and filter options selected and I make an API call with the sort and filter informations as GET parameters in the URL. In the backend, I extract the sort and filter informations and as a response, I send a JsonResponse containing sorted and filtered serialized objects. When the API response is recieved in JavaScript, I populate, for every object, the content of the template tag created in HTML in order to add the sorted and filtered objects in the DOM.
  Lastly, I take into consideration the search query typed by the user (if there is any) to decide which objects to display on the web page.

- **Used [DataTables](https://datatables.net/) to create interactive and responsive HTML tables:** I learned how to use DataTables (which requires jQuery) to make a more interesting table, both on the design level and feature level, as DataTables applies a certain styling and enables sorting, filtering and searching within the data of the table. But the default styling and features wasn't enough for me, so I also learned [data rendering](https://datatables.net/examples/basic_init/data_rendering.html), which helped me customise how the data will be displayed in the cells (changing text color, adding links to the text), as well as specifying what information DataTables will use in order to sort and filter the data of the table.

- **Create dynamic form, saving its data in JSON format and represent this JSON data in an HTMl file:** Using JavaScript and the `template` tag in HTML, I was able to create a dynamic form in one of my web pages. In fact, there is a button at the end of the form, everytime it is clicked, a new section of the form is displayed.
  When the form is submitted, I extract all field values, apply some checking, merge them into a single data structure which is then saved to a JSON file.
  In a certain point in the web application, I load the content of the JSON file into a python dictionary and I represent that data in an HTML file.

- **Responsive web application:** This web application is fully responsive, as I used CSS media queries to adapt the styling of my web application on different viewport sizes.

- **Light mode / dark mode:** Users can switch between Light mode and dark mode depending on their preference.

## What’s contained in each file I created

E-Learning-Platform is the base directory. Here is the listing of the files/directories I created/added code in it:

- **README.md**
- **quizes directory:** this directory contains the quizes files in JSON format. Every file is named by the {course instructor's username}\_{course id}.
- **media directory:** this directory contains 2 sub-directories:
  - **certificate_images directory:** contains 2 image files that are necessary when I generate a course's certificate pdf file.
  - **courses_images directory:** every course has its own image. These images are stored in this directory.
- **elearning directory:** it's the directory of the Django project. The 2 files in this directory in which I added some code are:
  - **settings.py:** I mainly specified the `MESSAGE_TAGS` dictionary, in which I assigned each Django message tag with a corresponding class. I also specified `MEDIA_ROOT` and `MEDIA_URL` for the upload files functionality, and `QUIZES_ROOT` to specify in which directory to store the courses' quizes. Finally I specified `EMAIL_BACKEND` for running an SMTP server on the console.
  * **urls.py:** In that file, I specified the path to my Django application.
- **courses_platform directory:** it's the directory of this django app. It contains:
  - **static/courses_platform directory:** In this directory, there is the css and js files divided between 2 directories: `components` directory which contains css and js files related to some components of a specific web page, and `pages` directory in wich there are css and js files responsible of a whole web page.
    Additionaly, in the static/courses_platform directory there are 3 css files:
    - **modern-normalize.css:** Normalize browsers' default style. Includes only normalizations for the latest Chrome, Firefox, and Safari ([source](https://github.com/sindresorhus/modern-normalize)).
    - **styles.css:** in this file I defined variables for font size and colors, and I applied styling to various HTML elements: body, input, textarea, select, button, image, and anchor.
    - **utils.css:** in this file, I mainly specified the styling of "my-container" class on different viewport sizes, which is a class given to the div element that wraps the entire body content of every web page in this web app.
  * **templates/courses_platform directory:** this directory contains all the html files of every web page in this web app, along with one directory named `includes` which contains messages.html where there is the html code of success/error/warning messages that appear to the user.
  * **urls.py:** in this file, I specified all the paths required for my web app, along with their appropriate views function name, and their appropriate name.
  * **views.py:** in this file, I defined all Django forms I need for my web app. Also, every views function is defined in this file.
  * **models.py:** in this file, I defined 2 models: User model and Course model. The fields in every model and the relationship between them is shown in the figure below.
    ![Image that shows the models, their fields and the relationship between the fields](media/database_image/database.png "Image showing the models, their fields and the relationship between the fields")
  * **admin.py:** in this file, I specified for every model, what fields to show in the admin interface.
  * **tests.py:** in this file, I defined tests that aim to test the models I created.

How to run your application.

Any other additional information the staff should know about your project.

If you’ve added any Python packages that need to be installed in order to run your web application, be sure to add them to a requirements.txt file!

(future work ?)
