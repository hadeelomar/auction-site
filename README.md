# <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
<path d="m14.5 12.5-8 8a2.119 2.119 0 1 1-3-3l8-8"/>
<path d="m16 16 6-6"/>
<path d="m8 8 6-6"/>
<path d="m9 7 8 8"/>
<path d="m21 11-8-8"/>
</svg> Bido - ECS639U Group Coursework - Group 36

A full-stack auction site, SPA, built with Django for the backend API and Vue for the frontend (Vue router for frontend routing and Pinia for a global store).

**Group members:** Hadeel, Milad, Omar

## Contribution

- **Hadeel**: Led coordination and UI direction, implemented authentication, editable profile page, deployment to OpenShift, and cron/email winner notification system, plus enhanced notification preferences with real-time in-app notifications and automated email queuing.
- **Milad**: Implemented item details experience including bidding UI, plus Q&A and bidding models/endpoints and their frontend integration, plus Google OAuth authentication and comprehensive internationalisation with 10+ languages and RTL support.
- **Omar**: Implemented auction item models/endpoints and search endpoint, and built the browse and create auction pages including live Ajax search, plus enhanced security with specific domain configuration, CSRF protection, and comprehensive social sharing features with QR codes and analytics.

## Requirements Fulfillment

| Criteria | Implementation | How We Went Above and Beyond |
|----------|----------------|---------------------------|
| **App deployed to Openshift with auto emails and cron jobs** | Full OpenShift deployment with automated email system using Django management commands and cron jobs | Enhanced with dual email notifications (winner + seller), comprehensive logging, automated cron setup command, and professional HTML email templates |
| **User signup and login with Django AbstractUser** | Complete authentication system using Django's built-in User model with custom fields | Added Google OAuth integration configuration, rate limiting for login attempts, and enhanced security with CSRF protection |
| **Editable profile page included** | Full profile management with custom fields (profile image, email, date of birth) and Ajax updates | Enhanced with real-time validation, notification preferences, and seamless Ajax form submission with loading states |
| **Create new items and search for available items** | Comprehensive auction creation with image upload and advanced Ajax search functionality | Added social sharing features with QR codes and share analytics tracking, advanced filtering (category, price, status), and relevance-based search ranking |
| **Question and replies about an item** | Full Q&A system with updates and notifications visible to all users | Enhanced with WebSocket real-time notifications, paginated question display, and comprehensive moderation features |
| **Correct modelling of application data** | Proper Django models with relationships, constraints, and indexes | Enhanced with notification models, share analytics models, comprehensive data validation, optimised database queries, and proper foreign key relationships |
| **Good use of Vue router and Pinia global store** | Complete SPA with Vue Router and Pinia for state management | Added advanced routing with authentication guards, real-time notification system, persistent state management, and comprehensive error handling |
| **Ajax used throughout SPA using fetch API** | Consistent use of fetch API for all backend communication with no page refreshes | Enhanced with comprehensive error handling, loading states, CSRF token management, and real-time data updates |
| **Full use of static types both in Python and Vue** | Complete TypeScript implementation in Vue and comprehensive type hints in Python | Enhanced with complete type coverage across entire codebase, custom interfaces for all data models, proper function signatures, linting tools (mypy, flake8, black), and pre-commit hooks for code quality |

## Test Data Setup

To create comprehensive test data for demonstration and testing:

```console
# Create 5 test users, 10 auctions, bids, and Q&A content
python manage.py create_test_data

# Setup automated cron job for auction closing
python manage.py setup_cron
```

## Admin Features

Access comprehensive admin features:

```console
# View system statistics
curl http://localhost:8001/api/system/stats

# Export auction data as CSV
curl http://localhost:8001/api/auctions/export

# Check system health
curl http://localhost:8001/api/system/health
```

## Test Users

The following test users are created with password `testpass123`:

- **john.doe@example.com** - John Doe
- **jane.smith@example.com** - Jane Smith  
- **mike.wilson@example.com** - Mike Wilson
- **sarah.jones@example.com** - Sarah Jones
- **alex.brown@example.com** - Alex Brown

## Deployment Information

- **OpenShift URL**: https://group36-web-apps-ap22223.apps.a.comp-teach.qmul.ac.uk
- **Admin Username**: admin
- **Admin Password**: [Set during deployment]


## Local Development

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

5. If everything is alright, you should be able to start the Django ASGI server from the main folder:

    ```console
    $ python run_asgi.py
    ```

6. and the Vue server from the 'frontend' sub-folder:

    ```console
    $ npm run dev
    ```

Alternatively, you can run both servers simultaneously from the 'frontend' sub-folder:

```console
$ npm run dev:all
```

7. Open your browser and go to http://localhost:5173/, where you will see the application. To see the Django server, go to http://localhost:8001/ 

## OpenShift Deployment

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

This code is dedicated to the public domain to the maximum extent permitted by applicable law, pursuant to [CC0](http://creativecommons.org/publicdomain/zero/1.0/].
