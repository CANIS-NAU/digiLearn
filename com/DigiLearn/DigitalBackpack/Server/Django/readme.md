# Django Project Files
Listed below are the directories associated with the Digital Backpack server backend.

##### digipack
The digipack folder contains the Django core project files.  
  

##### commanager
The commanager app contains code to support the "client/server communication manager" (CCM). Metadata will be sent between the client and the server to communicate important information such as: the connection date, requested data, and requested data size. This information can then be used to determine what data is missing when connections are disrupted. This server-client communication will be implemented by utilizing Websockets, which allow for bi-directional communication. The CCM relies on Django channels.  
  

##### clientqueue
The clientqueue app will handle asynchronous processing as requests are made by the user. Tasks can be queued and offloaded in the background. The client queue relies on Celery and RabbitMQ.  
  

# Technologies
Listed below are the technologies associated with the server backend of the Digitial Backpack project.

##### Python
Python is a high-level object-oriented programming language, and the primary language used for the server backend.

  *Version: Python 3.8.5*

##### Django
Django is an open-source web framework written in Python. It helps secure and maintain websites as it reduces the amount of work for web development. Django comes with many features "out of the box", but is still highly customizable making it ideal for this project. 

  *Version: Django 3.1.6*
