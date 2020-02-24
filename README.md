# Project 4

Web Programming with Python and JavaScript


# Fidelity Blog



Inside this repo, you can find web application (made with Django framework) for Fidelity Blog and Social media

In this app, you can (**as user**)

* register and log in/out

* Create a Post

* Comment on posts

* Publish post, approve or delete comments

* Create a Post

* Greate a group

* Join and Leave group

* Post messages in a group

* Delete message 


 

Within admin panel, there is possibility of:

* managing registered users

* modifying Groups

* modifying Post

* modifying Comments

* modifying Group Post

* modifying Group Members



## Project Description


* **Virtual Evnironment**: Project4-env folder is the Virtual environment that was specifically created for the project4.

* **Fidelity Blog**: This is the django project that contains the django applications blog and groups.

* **blog app**: This is the django application that handles the Posting of aritcles for Fidelity Blog, the comments been made for each post and the messages beign sent to different groups. It contains the static files for the css and javascript files used for the entire project, numerous templates in the template files for both blog posts and group posts. it's model.py file has 3 classes (Post, PostGroup, Comment). It's form.py has 4 form classes including one for User creation. The views.py file contains the class views and obviously the urls.py file contains the url patterns that connects the views with the templates.

* **group app**: This is the django application that handles the Creation of groups intended for users to socialize on Fidelity Blog. Users can create a group, join a group, post on a group, leave a group and delete a post. It contains 4 template files including group_base.html file which extends blog's application base.html file. it's model.py file has 2 classes (Group and GroupMember). The views.py file contains the class views and obviously the urls.py file contains the url patterns that links the views to the templates.
