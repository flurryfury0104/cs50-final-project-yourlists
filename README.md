# YourLists: A Shopping List and Todo List Web App

&nbsp;
## A CS50 Final Project
Made as a [final project](https://cs50.harvard.edu/x/2020/project/) for the course [CS50's Introduction to Computer Science](https://www.edx.org/course/cs50s-introduction-to-computer-science), *YourLists* helps users manage their shopping lists as well as todo lists. *YourLists* is a Flask app deployed on [Heroku](https://www.heroku.com/) and can be accessed at https://yourlists.herokuapp.com/.

*YourLists* utilizes some elements provided by CS50 for the [Finance](https://cs50.harvard.edu/x/2020/tracks/web/finance/) web app project, which are the file `layout.html` and the methods `apology()`, `login_required()`, `login()`, `logout()`.

&nbsp;
## Using *YourLists*
### Logging In
*YourLists* provides basic functionalities for users to  **register**, **log in**, **change password**, **log out**.

### Home Page
Once registered and logged in, users will be directed to *YourLists*'s home page to view all existing lists. List that are due on the current date or are past their due dates will be emphasized in red.

Users can **add** Shopping Lists and Todo Lists. The default list is `Untitled` and `without duedate`.

Users have the actions to **complete** and **delete** a list. There are also **delete all** buttons for quick delete actions.

User can click on uncompleted lists to view and/or edit their details.

![Image of homepage](screenshots/Homepage.png)

### Inside a Shopping List
Users can manage smaller **items** inside a Shopping List. Users can also **edit** the name and due date of a Shopping List and save the changes by clicking the `Done` button on the top right corner.

![Image of Shopping List Details](screenshots/EditShoppingList.png)

### Inside a Todo List
The inside of a Todo List is very similar to that of a Shopping List, with additional due dates for individual items.

![Image of Todo List Details](screenshots/EditTodoList.png)

&nbsp;
## The Database
*YourLists* utilizes [Heroku's Postgres add-on](https://www.heroku.com/postgres) for database management. The [PostgreSQL](https://www.postgresql.org/) database connected to Heroku is created with [pgAdmin](https://www.pgadmin.org/) using the schema below:

```
CREATE TABLE public.users
(
    id integer NOT NULL DEFAULT nextval('users_id_seq'::regclass),
    username text COLLATE pg_catalog."default" NOT NULL,
    hash text COLLATE pg_catalog."default" NOT NULL,
    CONSTRAINT users_pkey PRIMARY KEY (id)
)

CREATE TABLE public.shopping
(
    shoppingid integer NOT NULL DEFAULT nextval('"shopping_shoppingId_seq"'::regclass),
    userid integer NOT NULL,
    listname text COLLATE pg_catalog."default" NOT NULL,
    duedate date,
    completed boolean NOT NULL DEFAULT false,
    deleted boolean NOT NULL DEFAULT false,
    transacted timestamp without time zone NOT NULL,
    completedtime timestamp without time zone,
    CONSTRAINT shopping_pkey PRIMARY KEY (shoppingid)
)

CREATE TABLE public.todo
(
    todoid integer NOT NULL DEFAULT nextval('"todo_todoId_seq"'::regclass),
    userid integer NOT NULL,
    listname text COLLATE pg_catalog."default" NOT NULL,
    duedate date,
    completed boolean NOT NULL DEFAULT false,
    deleted boolean NOT NULL DEFAULT false,
    transacted timestamp without time zone NOT NULL,
    completedtime timestamp without time zone,
    CONSTRAINT todo_pkey PRIMARY KEY (todoid)
)

CREATE TABLE public.shopitem
(
    itemid integer NOT NULL DEFAULT nextval('shopitem_itemid_seq'::regclass),
    shoppingid integer NOT NULL,
    itemname text COLLATE pg_catalog."default" NOT NULL,
    completed boolean NOT NULL DEFAULT false,
    deleted boolean NOT NULL DEFAULT false,
    transacted timestamp without time zone NOT NULL,
    completedtime timestamp without time zone,
    CONSTRAINT shopitem_pkey PRIMARY KEY (itemid)
)

CREATE TABLE public.todoitem
(
    itemid integer NOT NULL DEFAULT nextval('todoitem_itemid_seq'::regclass),
    todoid integer NOT NULL,
    itemname text COLLATE pg_catalog."default" NOT NULL,
    duedate date,
    completed boolean NOT NULL DEFAULT false,
    deleted boolean NOT NULL DEFAULT false,
    transacted timestamp without time zone NOT NULL,
    completedtime timestamp without time zone,
    CONSTRAINT todoitem_pkey PRIMARY KEY (itemid)
)
```
