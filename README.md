[![Minimum Python Version](https://img.shields.io/badge/Python-3.7%2B-yellow)](https://www.python.org/downloads/)
[![Minimum PostgreSQL Version](https://img.shields.io/badge/PostgreSQL-10%2B-blue)](https://www.postgresql.org/download/)
[![Minimum pgAdmin version](https://img.shields.io/badge/pgAdmin-4-blue)](https://www.pgadmin.org/download/)

This project involves a data-baced web application accessing a small artificial dataset about university study.

# Getting Started

The project requires the following to be set up already:

- [Python 3.7+](https://www.python.org/downloads/)
- [PostgreSQL 10+](https://www.postgresql.org/download/)
- [pgAdmin 4](https://www.pgadmin.org/download/)
- [`ssh` key pair](https://docs.github.com/en/enterprise-server@3.4/authentication/connecting-to-github-with-ssh/generating-a-new-ssh-key-and-adding-it-to-the-ssh-agent)

## Load the required database schema

Download the required database schema: [`unidbschema.sql`](https://canvas.sydney.edu.au/courses/43727/modules/items/1733778).

> ***IMPORTANT!***
You need to connect to the university network to connect the database server.
You need to be either on campus, or follow the instructions [here](https://sydneyuni.service-now.com/sm/?id=kb_article_view&sys_kb_id=836b51e6dbeb6010ea7d0793f3961901) to connect to the university VPN.
If you are in mainland China, follow [this instruction](https://secure-client.sydney.edu.au/) to connect to the FortClient VPN provided by the university.

### pgAdmin

Open pgAdmin and enter your master password (the password you set up during the installation).
Right click "Server", click on "Register" and then "Server".
Once a dialogue is opened, click on "Connection" tab.
Fill in the **hostname**, **maintenance database**, **username** and **password** as stated in your PostgreSQL login email.
Then click "Connect".

Once connected, in the left panel, unfolder the server you have created, unfold "Databases".
Scoll down to find the one with the database name matching the maintenance database name you typed in in the previous step.

Launch the query tool.
In the query window, open `unidbschema.sql` you downloaded previously.
Run the code.
You should see the schema `unidb` appearing under `schema` after you unfold your database.

### Command Line

`cd` to the folder `unidbschema.sql` file is downloaded to.
Use a terminal to run the following code:

```bash
psql -h soitpw11d59.shared.sydney.edu.au -d <maintenance-database-name> -U <username> -f unidbschema.sql
# replace <maintenance-database-name> and <username> with the corresponding details stated in your PostgreSQL login email.
```

Enter your password stated in the email as required.

## Connect to the server
Use a terminal to connect to the university server using `ssh`.

```bash
ssh abcd1234@ucpu0.ug.cs.usyd.edu.au # Replace abcd1234 with your own Unikey
```

At the prompt for password, give your Unikey password.

Git Clone this repository **on the server** using `git clone`.

## Install the required packages

You need some Python packages to be installed so that you can run the application.
To install these packages, in the terminal, run the following code:

```bash
bash install.sh
```

## Set up the initialisation file

Create `config.ini` using any text editor you like, so that the program will know which database server to connect to.

A sample `config.ini` file is given as below.
You need to change `<host>`, `<username>` and `<password>` to the PostgreSQL login stated in the email.
Change `<port_number>` to the last 3 digit of your SID.

```ini
[DATABASE]
host = <host>
user = <username>
password = <password>
database = <database> # the data owner's database

[FLASK]
port = <port_number>
```

Click "File" and "Save" to save the file.

## Execute the program

In the terminal which has already connected to the server, run the following command:

```bash
./threetier.command
```

If you get a permission denied error, you need to first give permission to execute by running the following command:

```bash
chmod +x ./threetier.command
```

After you run the command, open the link specified in the terminal on a web browser to browse the project interface.
