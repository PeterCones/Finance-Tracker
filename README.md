# 💰 Finance-Tracker  
> *“Track smarter, spend wiser — take control of your finances.”*

![Python](https://img.shields.io/badge/Python-3.x-blue?logo=python)
![Django](https://img.shields.io/badge/Django-Framework-green?logo=django)
![Status](https://img.shields.io/badge/Status-In%20Development-yellow)
![License](https://img.shields.io/badge/License-MIT-lightgrey)

---

## 📘 About  
**Finance-Tracker** is a full-stack Django web application built for managing personal finances through **budget tracking**, **expense monitoring**, and **goal management**.  

It was developed as part of the *AI Augmented Full Stack Bootcamp* Capstone Project, demonstrating core competencies in full-stack design, CRUD development, version control, and AI-augmented productivity.

> 🧩 *Repository:* [PeterCones/Finance-Tracker](https://github.com/PeterCones/Finance-Tracker)
> 🧩 *Live Deployment:* [PeterCones/Finance-Tracker]([https://github.com/PeterCones/Finance-Tracker](https://finance-tracker-production-ol-090f27f23bf4.herokuapp.com/accounts/login/?next=/))
---

## 🧭 Table of Contents
- [Agile Methodology](#-agile-methodology)
- [UX Design Process](#-ux-design-process)
- [Features](#-features)
- [Tech Stack](#-tech-stack)
- [Deployment](#️-deployment-on-heroku)
- [Testing](#-testing)
- [Project Structure](#-project-structure)
- [Use Cases & User Stories](#-use-cases--user-stories)
- [Learning Outcomes Mapping](#-learning-outcomes-mapping-lo1lo8)
- [AI Usage Reflection](#-ai-usage-reflection-lo8)
- [Security & Submission Checklist](#️-security--submission-checklist)
- [Contributing & Credits](#-contributing--credits)
- [License](#-license)

---

## 🎥 Demo / Screenshots  

<img width="1300" height="1145" alt="image" src="https://github.com/user-attachments/assets/7202e1e8-c13f-45a4-a417-0486ee480f98" />

<img width="1300" height="1145" alt="image" src="https://github.com/user-attachments/assets/81f182e6-e95a-402d-b07a-b67771ec142a" />
 
<img width="1300" height="1145" alt="image" src="https://github.com/user-attachments/assets/9f26dcdc-8fbf-4ff3-af3f-40619b7c8959" />

<img width="1300" height="1145" alt="image" src="https://github.com/user-attachments/assets/7d72b53c-31d5-4855-8912-d7d38da59070" />



---

## ✨ Features  
✅ Secure user authentication (Register, Login, Logout)  
✅ Role-based access control (User / Admin)  
✅ CRUD operations for:
  - 💸 Accounts  
  - 🧾 Transactions  
  - 📊 Budgets  
  - 🎯 Financial Goals  
✅ Budget progress indicators with live visual feedback  
✅ Mobile-responsive design with accessible forms  
✅ Flash message notifications for key actions  
✅ Unit tests for models & key views  
✅ AI-assisted documentation and code generation (reflective use under LO8)

---

## 🛠️ Tech Stack  

| Layer | Technology |
|-------|-------------|
| **Frontend** | HTML5, CSS3, JavaScript (Vanilla / Progress bar API) |
| **Backend** | Python 3.x, Django |
| **Database** | SQLite (development) / PostgreSQL (production) |
| **Hosting** | 🔧 *Insert hosting platform here* |
| **Version Control** | Git + GitHub |
| **AI Tools** | ChatGPT, GitHub Copilot (for assisted generation & debugging) |

---

## ⚙️ Installation & Setup  

### ☁️ Deployment on Heroku

This project was deployed on **Heroku**, pulling directly from the `main` branch of the **GitHub repository**. The following guide outlines the complete configuration and deployment process.

---

### 🧩 Prerequisites

Before you begin, ensure your project meets these requirements.

- [x] **Secure Environment Variables**: All sensitive data (e.g., `SECRET_KEY`, `DATABASE_URL`) is handled by environment variables and **never** hard-coded. The `.gitignore` file must exclude any local environment files (like `.env`).
- [x] **Production-Ready Settings**: The `DEBUG` variable in `settings.py` is set to `False`.
- [x] **Required Packages**: The `requirements.txt` file includes `gunicorn` for serving the application and `whitenoise` for handling static files.

---

### ⚙️ Configuration for Deployment

Follow these steps to prepare your Django project for a Heroku environment.

1.  **Create the `Procfile`**

    In the root directory of your project, create a file named `Procfile` (with no file extension). This file tells Heroku how to run your application.

    ```
    web: gunicorn FinanceTracker.wsgi
    ```

    > [!NOTE]
    > Replace `FinanceTracker.wsgi` with `{your_project_name}.wsgi` if your Django project has a different name.

2.  **Specify the Python Version**

    Create a `.python-version` file in the root directory to lock the Python runtime on Heroku.

    ```
    python-3.11.9
    ```

3.  **Update Django Settings (`settings.py`)**

    Modify your `settings.py` to allow requests from your Heroku app's domain.

    ```python
    # settings.py

    ALLOWED_HOSTS = ['your-app-name.herokuapp.com', '127.0.0.1']

    CSRF_TRUSTED_ORIGINS = ['https://*.herokuapp.com']
    ```

    > [!TIP]
    > 🔧 Replace `your-app-name` with the actual name of your Heroku application.

4.  **Configure Static Files for Production**

    Define `STATIC_ROOT` in `settings.py` to specify where Django will collect all static assets for deployment.

    ```python
    # settings.py

    STATIC_ROOT = BASE_DIR / 'staticfiles'
    ```

    Next, run the `collectstatic` command. This will create a `staticfiles` directory and copy all static files into it.

    ```bash
    python manage.py collectstatic
    ```

5.  **Commit and Push to GitHub**

    Stage, commit, and push all your configuration changes to the GitHub repository.

    ```bash
    git add .
    git commit -m "feat: Configure project for Heroku deployment"
    git push origin main
    ```

---

### 🚀 Deploying to Heroku

With your repository prepared, you can now deploy it live.

1.  **Create a New Heroku App**
    - Log in to your **Heroku Dashboard**.
    - Click **"New"** → **"Create new app"**.
    - Choose a unique app name and select your preferred region.

2.  **Set Environment Variables (Config Vars)**
    - In your app's dashboard, navigate to the **"Settings"** tab.
    - Find the **"Config Vars"** section and click **"Reveal Config Vars"**.
    - Add the necessary key-value pairs.

    | Key | Value |
    | :--- | :--- |
    | `DATABASE_URL` | 🔧 `your_production_database_url` |
    | `SECRET_KEY` | 🔧 `your_secure_production_secret_key` |

    > [!WARNING]
    > **Never** use your development `SECRET_KEY` in production. Generate a new, unique key for your live application.

3.  **Connect GitHub and Deploy**
    - Navigate to the **"Deploy"** tab.
    - Under "Deployment method," click **GitHub** and connect your account.
    - Search for your `Finance-Tracker` repository and connect it.
    - Scroll down to the **"Manual deploy"** section.
    - Ensure the correct branch (e.g., `main`) is selected.
    - Click **"Deploy Branch"**.

Heroku will now build your application by installing dependencies, collecting static files, and launching the web server defined in your `Procfile`. Once complete, your application will be live! 🎉



### 👥 Use Cases & User Stories

This section outlines the key actions and goals that users can achieve with the Finance-Tracker application. The primary user role is the **Registered User**, who wants to manage their personal finances effectively.

### Core User: The Financial Planner

As a **Registered User**, I want to be able to...

---

#### 🔐 1. Account Management & Security

* **Register for an account:** So that I can create a secure, private space to manage my personal finances.
    * *Scenario:* A new user visits the site, clicks "Register," fills in their details (username, email, password), and creates an account. They are then automatically logged in and redirected to their dashboard.
* **Log in to my account:** So that I can access my financial dashboard and manage my data securely.
    * *Scenario:* A returning user enters their credentials on the login page to gain access to their personalized dashboard.
* **Log out of my account:** So that I can protect my financial information when I am finished using the application.
    * *Scenario:* A user clicks the "Logout" button to securely end their session, ensuring their data remains private.



---

#### 📊 2. Managing Budgets

* **Create a new budget:** So that I can set spending limits for different categories (e.g., "Groceries," "Transport," "Entertainment") on a monthly basis.
    * *Scenario:* A user navigates to the "Budgets" section, creates a new budget named "Groceries," and allocates £250 for the current month.
* **View all my budgets:** So that I can get a clear overview of all my spending categories and their limits at a glance.
    * *Scenario:* The user's budget page displays cards or a list for "Groceries," "Transport," and "Entertainment," showing the allocated amount for each.
* **See my spending progress for a budget:** So that I can track how much I have spent against my limit in real-time.
    * *Scenario:* The "Groceries" budget card displays a progress bar showing that £110 of the £250 has been spent, clearly indicating how much is remaining.
* **Edit an existing budget:** So that I can adjust my spending limits if my financial circumstances change.
    * *Scenario:* The user realizes they need more for transport this month, so they edit their "Transport" budget to increase the limit from £100 to £120.
* **Delete a budget:** So that I can remove categories that are no longer relevant to my spending.
    * *Scenario:* A user stops using a subscription service and deletes the corresponding "Subscriptions" budget category.

---

#### 💸 3. Tracking Transactions

* **Log a new transaction (expense or income):** So that I can maintain an accurate record of where my money is going and coming from.
    * *Scenario:* After buying groceries, a user adds a new transaction for £45.50, assigning it to the "Groceries" budget category.
* **View a history of all my transactions:** So that I can review my past spending and income over time.
    * *Scenario:* A user visits the "Transactions" page and sees a chronological list of all their entries, including the date, description, amount, and associated budget.
* **Edit a transaction:** So that I can correct any mistakes I made when logging my spending.
    * *Scenario:* The user accidentally entered £54.50 instead of £45.50 for a transaction and quickly edits the entry to correct the amount.
* **Delete a transaction:** So that I can remove duplicate or incorrect entries.
    * *Scenario:* A user accidentally logged the same transaction twice and deletes the duplicate entry to clean up their records.

---

#### 🎯 4. Setting Financial Goals

* **Create a financial goal:** So that I can set a target for something I want to save for, like a holiday or a new laptop.
    * *Scenario:* A user creates a new goal called "Holiday to Spain," setting a target amount of £1,000.
* **View my progress towards a goal:** So that I can see how close I am to reaching my target and stay motivated.
    * *Scenario:* The "Holiday to Spain" goal page shows that the user has saved £400 out of the required £1,000, with a progress bar visually representing this.
* **Update or delete a goal:** So that I can change my savings targets as my priorities shift.
    * *Scenario:* The user decides to save for a more expensive trip and edits the "Holiday to Spain" goal, increasing the target amount to £1,500.


## 🧪 Testing

A thorough testing strategy was implemented to ensure the reliability, functionality, and stability of the Finance-Tracker application. The approach combined both automated unit tests for the backend logic and a comprehensive suite of manual tests for user-facing features.

---

### Automated Testing

Automated tests were written using Django's built-in `TestCase` framework to validate the core backend logic. The primary focus was on ensuring data integrity and the correctness of business logic.

**Key Areas Covered:**

* **Model Integrity**: Tests were created to ensure that the `Budget`, `Transaction`, and `Goal` models save data correctly, handle relationships properly (e.g., linking a transaction to a budget), and that model methods (like calculating budget progress) return accurate results.
* **View Permissions**: Tests verify that critical views are protected. For example, unauthenticated users are redirected from the dashboard to the login page, and a user cannot view or edit the financial data of another user.
* **Form Validation**: Unit tests check that forms for creating and editing budgets, transactions, and goals correctly validate user input, rejecting invalid data (e.g., non-numeric amounts, empty required fields).

**How to Run the Tests:**

To execute the automated test suite, run the following command from the project's root directory:

```bash
python manage.py test

--

| Test Case ID | Feature           | Test Scenario                                                                   | Expected Result                                                                  | Actual Result | Status |
| ------------ | ----------------- | ------------------------------------------------------------------------------- | -------------------------------------------------------------------------------- | ------------- | ------ |
| TC-AUTH-01   | Authentication    | A new user registers with valid credentials.                                    | The account is created, the user is logged in, and redirected to the dashboard.  | As expected   | ✅      |
| TC-AUTH-02   | Authentication    | An existing user attempts to log in with an incorrect password.                 | Access is denied, and a user-friendly error message is displayed.                | As expected   | ✅      |
| TC-BUD-01    | Budgets CRUD      | A user creates a new budget, views it, updates the amount, and then deletes it. | All CRUD operations perform successfully, and the UI updates immediately.        | As expected   | ✅      |
| TC-TRN-01    | Transactions CRUD | A user logs a new expense and assigns it to a budget.                           | The transaction is saved, and the corresponding budget's progress bar updates.   | As expected   | ✅      |
| TC-GOAL-01   | Goals CRUD        | A user creates a new savings goal with a target amount.                         | The goal is successfully created and displayed on the goals page.                | As expected   | ✅      |
| TC-FORM-01   | Form Validation   | A user attempts to submit a form with a required field left empty.              | The form is not submitted, and an inline validation error is shown.              | As expected   | ✅      |
| TC-RESP-01   | Responsive Design | The application is viewed on a mobile device (e.g., iPhone 12 viewport).        | The layout adapts correctly, navigation is accessible, and all text is readable. | As expected   | ✅      |


## 📂 Project Structure

The Finance-Tracker project follows a standard Django application structure, promoting modularity and maintainability. The codebase is organized into distinct apps, each responsible for a specific domain of functionality.

### Directory Tree

Below is a high-level overview of the project's directory structure:

---

### Component Breakdown

This structure was chosen to create a clear separation of concerns, which is a key principle of object-oriented design and is reflected in the learning outcomes.

| Directory / File | Purpose |
| :--- | :--- |
| **`FinanceTracker/`** | The main Django project directory containing site-wide configurations. |
| **`accounts/`** | [cite_start]A Django app dedicated to user authentication and management, fulfilling the role-based access requirements. [cite: 8, 9] |
| **`budgets/`** | [cite_start]This app contains the models, views, and templates for all budget-related CRUD (Create, Read, Update, Delete) functionality. [cite: 6, 7] |
| **`transactions/`** | [cite_start]Handles all logic related to financial transactions, linking them to specific budgets and users. [cite: 6, 7] |
| **`goals/`** | [cite_start]A dedicated app for managing user-defined financial goals. [cite: 6, 7] |
| **`static/`** | [cite_start]Stores all static files, such as CSS for styling and JavaScript for front-end interactivity, ensuring a clean and responsive user interface. [cite: 4, 5] |
| **`templates/`** | [cite_start]Holds the HTML files that render the front-end pages, enabling a consistent and user-friendly design. [cite: 4, 5] |
| **`manage.py`** | The command-line utility for interacting with the Django project, used for running the server, migrations, and tests. |
| **`requirements.txt`**| Lists all project dependencies, making installation and deployment straightforward and repeatable. |
| **`Procfile` & `.env`**| [cite_start]Files used to configure the deployment environment on Heroku and manage secret keys securely. [cite: 14, 15] |


## 🎯 Learning Outcomes Mapping (LO1–LO8)

This section explicitly maps the project's features and documentation to the learning outcomes detailed in the **AI Augmented FullStack Bootcamp** marking criteria. This is intended to help assessors easily locate evidence for each requirement.

---

| Learning Outcome | Description | Evidence within Project |
| :--- | :--- | :--- |
| **LO1: Plan & Design** | [cite_start]Apply Agile methodology and UX/UI principles to design a responsive Full-Stack Django application. [cite: 4] | [cite_start]**Front-End**: The UI is built with semantic HTML and custom CSS, ensuring a responsive layout for various screen sizes[cite: 5]. [cite_start]<br> **Database**: The project uses custom Django models for all core features[cite: 70]. [cite_start]<br> **Documentation**: The UX design process is detailed in this README, adhering to the project's initial design goals[cite: 36]. |
| **LO2: Data & Logic** | [cite_start]Develop a data model and implement business logic with full CRUD functionality and user notifications. [cite: 37] | [cite_start]**Database Model**: A well-organised database schema is implemented with models for `Accounts`, `Budgets`, `Transactions`, and `Goals`[cite: 38]. [cite_start]<br> **CRUD**: The application provides user-friendly interfaces for creating, reading, updating, and deleting records for all core features[cite: 38]. [cite_start]<br> **Notifications**: Django's messaging framework is used to provide clear on-screen notifications to the user after key actions (e.g., "Budget successfully created.")[cite: 39]. |
| **LO3: Auth & Permissions** | [cite_start]Implement role-based authentication, authorization, and permission features. [cite: 40] | [cite_start]**Role-Based Login**: The application supports user registration and a login system. [cite: 41] [cite_start]<br> **Login State**: The navigation bar and page content dynamically change to reflect the user's login state and role[cite: 42]. [cite_start]<br> **Access Control**: Views are protected to prevent unauthenticated users from accessing restricted content, redirecting them to the login page if they attempt to do so[cite: 42]. |
| **LO4: Testing** | [cite_start]Design and execute manual or automated tests to evaluate the application's functionality and document the results. [cite: 43] | [cite_start]**Python Tests**: Automated unit tests were written for backend models and views to ensure data integrity and logic correctness. [cite: 44] [cite_start]<br> **Documentation**: The testing strategy, including a detailed manual test case summary, is documented in the "Testing" section of this README file[cite: 45]. |
| **LO5: Version Control** | [cite_start]Utilise Git and GitHub for version control, documenting the development process with meaningful commits and secure code management. [cite: 46] | [cite_start]**Git & GitHub**: The project's development history is documented through regular, descriptive commits in the GitHub repository. [cite: 47] [cite_start]<br> **Secure Code**: No passwords or sensitive keys are committed to the repository; secrets are managed using environment variables and a `.gitignore` file[cite: 48]. |
| **LO6: Deployment** | [cite_start]Deploy the application to a cloud-based platform, ensuring functionality and security. [cite: 49] | [cite_start]**Cloud Deployment**: The application was successfully deployed to Heroku and is fully functional. [cite: 50] [cite_start]<br> **Documentation**: The "Deployment" section of this README provides a clear, step-by-step guide on how to deploy the application[cite: 50]. [cite_start]<br> **Security**: The deployed application runs with `DEBUG=False` and uses environment variables for all sensitive keys[cite: 51]. |
| **LO7: Object-Based Concepts** | [cite_start]Demonstrate the use of object-based concepts by designing and implementing custom data models. [cite: 52] | [cite_start]**Custom Data Models**: The project features a custom data model designed specifically for its requirements, including the `Budget`, `Transaction`, and `Goal` models[cite: 57, 58]. [cite_start]These are implemented using Django's Object-Relational Mapping (ORM)[cite: 63]. |
| **LO8: AI Tool Usage** | [cite_start]Leverage AI tools to assist in the software development process and reflect on their impact. [cite: 59] | [cite_start]**AI-Assisted Development**: AI tools were used to generate boilerplate code, assist in debugging logic, and create skeletons for unit tests. [cite: 60, 65, 84] [cite_start]<br> **Reflection**: The "AI Usage Reflection" section of this README provides a concise summary of how AI influenced the development workflow and improved efficiency[cite: 84]. |


🤖 AI Usage Reflection (LO8)
Throughout the development of Finance-Tracker, AI tools like GitHub Copilot and ChatGPT were integrated into the workflow as a collaborative partner. The goal was not to replace the development process, but to augment it, leading to increased efficiency, faster problem-solving, and more robust code. All AI-generated output was critically reviewed, tested, and adapted to fit the project's specific needs.

1. Code Generation & Scaffolding
AI was instrumental in accelerating the creation of boilerplate and repetitive code structures, allowing more time to be spent on custom business logic.

Scaffolding Django Views: I used GitHub Copilot to generate the initial class structure for standard CRUD (Create, Read, Update, Delete) views. For example, when creating the BudgetUpdateView, Copilot suggested the complete UpdateView class, including the model, form_class, template_name, and success_url attributes. This skeleton was then manually customized.

Creating Django Forms: For the TransactionForm, an AI assistant was prompted to generate a ModelForm, including the Meta class and the list of fields. This provided a solid foundation that was then refined with custom widgets and validation logic.

2. Debugging & Code Optimization
AI proved to be an invaluable resource for troubleshooting complex issues, particularly within the Django ORM.

Optimizing Database Queries: A key intervention was in optimizing the main dashboard view, which calculated the total spending for multiple budgets. My initial implementation suffered from the "N+1 query problem," causing a separate database query for every budget in the loop. By providing the view's code to an AI assistant, it identified this performance bottleneck and suggested refactoring the queryset to use select_related and Django's annotate with Sum. This single change dramatically reduced the number of database queries from dozens to just one, significantly improving page load time.

Resolving Logic Errors: During development, a bug occurred where budget progress bars were not updating correctly. I used an AI tool to review the view logic and the template's conditional statements. The AI helped identify a subtle type mismatch error in the context data being passed to the template, a fix that might otherwise have taken much longer to diagnose manually.

3. UX & Design Assistance
While I am not a designer, AI helped bridge the gap by providing suggestions for creating a clean and intuitive user interface.

Responsive Layout Ideas: I prompted an AI assistant for different CSS Flexbox and Grid layouts to structure the main dashboard. It provided several responsive patterns for arranging the budget cards, which I adapted to create the final, mobile-friendly design.


User-Friendly Messaging: To improve the user experience, AI was used to generate clear and concise user notification messages (e.g., for successful form submissions or errors), ensuring the tone was consistent and helpful throughout the application.


4. Automated Test Creation
GitHub Copilot was used to assist in writing unit tests, ensuring key functionalities were covered.

Generating Test Skeletons: Copilot was particularly effective at generating the basic structure for test cases. For instance, it generated initial tests to confirm that key views returned a 200 OK status code for authenticated users and a 302 Found (redirect) for unauthenticated users.

Refining Assertions: While Copilot provided the initial test functions, they were manually refined. For example, a generated test for the dashboard view was extended to include more specific assertions, such as self.assertContains() to check if a specific budget's name appeared in the rendered HTML, thus verifying the context data was passed correctly. This demonstrates a basic understanding of the test logic generated by Copilot.


Overall Impact on Workflow
This AI-augmented workflow proved highly effective. It reduced the time spent on routine tasks and complex debugging, allowing me to focus on higher-level architectural decisions and feature implementation. It fostered a more efficient development cycle, where AI acted as a constant sounding board for ideas and a powerful tool for overcoming technical hurdles.

🛡️ Security & Submission Checklist
This checklist was followed before the final submission to ensure the repository is clean, secure, and ready for assessment, aligning with best practices for production deployment.

[x] Remove Sensitive Data: The repository and its commit history have been checked to ensure no passwords, API keys, or other sensitive information are present.

[x] Configure .gitignore: The .gitignore file is properly configured to exclude sensitive files, such as .env and db.sqlite3, from version control.

[x] Use Environment Variables: All secret keys, including Django's SECRET_KEY and the DATABASE_URL, are managed securely using environment variables and are not hard-coded.

[x] Disable Debug Mode: The DEBUG setting in settings.py is confirmed to be set to False in the deployed production environment to prevent exposing sensitive configuration details.

[x] Remove Development Database: The local db.sqlite3 file has been removed from the final version of the repository. The production database is managed by Heroku.


🤝 Contributing & Credits
Contributing
Contributions are welcome, but as this is a student project, the scope for external additions is limited. If you have suggestions or wish to report a bug, please open an issue on the GitHub repository.

If you wish to fork the repository and work on your own version, please follow these steps:

Fork the Project: Click the "Fork" button at the top right of this page.

Create your Feature Branch: git checkout -b feature/AmazingFeature

Commit your Changes: git commit -m 'Add some AmazingFeature'

Push to the Branch: git push origin feature/AmazingFeature

Open a Pull Request

Credits and Acknowledgements
A special thank you to the following resources that were used in the creation of this project:

Images: The user interface and promotional images used in this project were sourced from the Frutiger Aero Archive. Their collection was invaluable for achieving the project's aesthetic goals.

Django Framework: The project is built on the powerful and flexible Django web framework.

Heroku: The application is deployed and hosted on the Heroku cloud platform.

📄 License
This project is licensed under the MIT License. This means you are free to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the software.

See the LICENSE file for more details.

Copyright (c) 2025 Peter Cones
