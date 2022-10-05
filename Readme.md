# Widgets

This is the Widget application. It can be reached by visiting https://rickycharpentier.com

This Widget application has five main functions: 

    • List all Widgets.

    • Create a new Widget by entering Name and Number of Parts values.
    
    • Create a new Widget with random values for Name and Number of Parts.
    
    • View and Update a Widget.
    
    • Delete a Widget.

#### Additions

I've added a few features to this site. Firstly, the ability to create a random widget, as opposed to manually entering information. Also, the homepage displays the first
ten widgets in order of most recently updated, as well as how many total widgets exist and a button to view all widgets. Lastly, I've limited the entry of the widget name to
64 characters.

#### Notes

This Widget application is written in Python and Flask, and persisted to a Postgres database using SQLAlchemy as the ORM.