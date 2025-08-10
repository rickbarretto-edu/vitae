# Vitae's User Guide

This guide is intended for non-technical users working in an already configured environment.
If you need to use Vitae without worrying about installations or command-line interfaces, this is your go-to manual.

## Download

You can download the application from the **Releases** section of our [GitHub repository](https://github.com/lasicuefs/curricFilter).
The application is portable, meaning it does not require any installation.

After downloading, you will see several files in the folder.
The only files you need to know about as a final user are:

- `vitae.exe` – The application launcher.
- `vitae.toml` – The configuration file.

## Setup Vitae.toml

Before running Vitae for the first time, you will need to set up a few database parameters.
Your system administrator will provide these values.

```toml
[postgres.user]
name = "database-user"          # Postgres User's name
password = "database-password"  # Postgres User's password

[postgres.database]
host = "127.0.0.1"              # Database's host, generally "127.0.0.1" or "0.0.0.0"
port = 5432                     # Database's port, generally "5432"
name = "vitae"                  # Database's name, your admin should use "vitae", preferably
```

Once this is setup, you do **not** need to change this settings anymore.

## Launching the Application

As any other desktop application, just double-click on `vitae.exe`, and then, it's working.
This may take 5s to 7s to be fully loaded.

## Features

![Guide](guide.png)

1. Search Bar: Enter the researcher’s name or ID
2. Filters: Filter by Country, State, Education, or Area
3. Submission: Perform the search
4. Sorting: Sort in alphabetical order
5. Profile: Click the profile to export it to Lucy Lattes
6. External Profile: Open the researcher’s profile on Lattes, or Orcid if available

Additional navigation:
* A Load More” button appears at the bottom of the page to load more results.
* A “Go to Top” button appears on the right side.
* A “Back” button appears on the left to return to the previous page.

## FAQ

### **Q:** Why in Portuguese

**A:** This application was developed primarily for Brazilian users, whose native language is Portuguese. If there is demand from English-speaking users, we may add full English support in a future release.

### **Q:** Vitae keeps running even after closing it

**A:** For the compiled version, the backend may continue running in the background after the window is closed. If this happens, open Windows' **Task Manager**, search for `vitae.exe`, and end the process manually.