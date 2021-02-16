# Django Project Files
Listed below are the directories associated with the Digital Backpack server backend.

- **digipack**
The digipack folder contains the Django core project files.

- **commanager**
The commanager app contains code to support the "client/server communication manager" (CCM). Metadata will be sent between the client and the server to communicate important information such as: the connection date, requested data, and requested data size. This information can then be used to determine what data is missing when connections are disrupted. This server-client communication will be implemented by utilizing Websockets, which allow for bi-directional communication. The CCM relies on Django channels. 

- **clientqueue**
The client queue app will handle asynchronous processing as requests are made by the user. Tasks can be queued and offloaded in the background. The client queue relies on Celery and RabbitMQ.

# Technologies
Listed below are the technologies associated with the server backend of the Digitial Backpack project.

- **Python**
Python is a high-level object-oriented programming language, and the primary language used for the server backend.

*Version: Python 3.8.5*

- **Django**
Django is an open-source web framework written in Python. It helps secure and maintain websites as it reduces the amount of work for web development. Django comes with many features "out of the box", but is still highly customizable making it ideal for this project. 

*Version: Django 3.1.6*

- **Channels**
Channels is an augment for Django which allows for handling of Websocket protocols as well as HTTP. This gives asynchronous support for tasks, which is a crucial mechanism for the Digital Backpack project.

*Version: Channels 3.0.3*

- **Celery**
Celery is an asynchronous task queue manager for Python.

*Version: Celery 5.0.5*

- **RabbitMQ**
RabbitMQ is a message broker necessary for the Celery task queue.

*Version: RabbitMQ 3.8.2*
