# Auction Site (Working title) ECS639U Group Coursework - Group 36

A full-stack Single Page Application built with Django for the backend API and Vue for the frontend (Vue router for frontend routing and Pinia for a global store).

**Group members:** Hadeel, Milad, Omar

## Contribution table
| Task | Hadeel | Milad | Omar |
|------|--------|-------|-------|
| Authentication system | | | |
| Pinia global store | | | |
| Q&A system (backend) | | | |
| Profile page (backend) | | | |
| Item creation (backend) | | | |
| Item listing and search (backend) | | | |
| API architecture (Django REST endpoints) | | | |
| Cron jobs and email system | | | |
| Vue router setup | | | |
| Q&A system (frontend) | | | |
| Profile page (frontend) | | | |
| Item creation (frontend) | | | |
| Item listing and search (frontend) | | | |
| Bidding system (backend) | | | |
| Bidding UI | | | |
| Data modelling (Users, Items, Bids, Question) | o | | |
| Backend type hints | | | |


## Local development

To run this project in your development machine, follow these steps:

1. Create and activate a conda environment

2. Install Python dependencies (main folder):

    ```console
    $ pip install -r requirements.txt
    ```

3. Create a development database:

    ```console
    $ python manage.py migrate
    ```

4. Install JavaScript dependencies (from 'frontend' folder):

    ```console
    $ npm install
    ```

5. If everything is alright, you should be able to start the Django development server from the main folder:

    ```console
    $ python manage.py runserver
    ```

6. and the Vue server from the 'frontend' sub-folder:

    ```console
    $ npm run dev
    ```

Alternatively, you can run both servers simultaneously from the 'frontend' sub-folder:

```console
$ npm run dev:all
```

7. Open your browser and go to http://localhost:5173/, where you will see the application. To see the Django server, go to http://localhost:8000/ 

## OpenShift deployment

Once your project is ready to be deployed you will need to 'build' the Vue app and place it in Django's static folder.

1. The build command in package.json and the vite.config.ts files have already been modified so that when running 'npm run build' (on Mac and Linux) the generated JavaScript and CSS files will be placed in the mainapp static folder, and the index.html file will be placed in the templates folder:

    ```console
    $ npm run build
    ```

    If using Windows run

    ```console
    $ npm run build-windows
    ```

2. You should then follow the instruction on QM+ on how to deploy your app on EECS's OpenShift live server.

## License

This code is dedicated to the public domain to the maximum extent permitted by applicable law, pursuant to [CC0](http://creativecommons.org/publicdomain/zero/1.0/).
