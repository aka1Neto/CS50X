# WALL-ET
## Video Demo:  <URL https://youtu.be/ikdAOyf02xc>
## Description:
Wallet is a web app that helps you to manage your monthly bugdet.

## Understanding:
It is important to say that this project is based in the finance project.

### Helpers
It is a python file with functions that will help along the project.

#### Apology
Redirects the user to error page and describes what was the error commited.

#### Login Required
Ensures that the user will be only able to use the application if they are logged in.

#### Rates
If symbol is provided returns a dictionary with currencies and its respective three-letters code. Otherwise, returns the currencies three-letter codes and its respective rate based in the Euro currency.

#### Generate Color
Generates a random color that later will be used in the expense/income chart.

#### USD
Takes a number as input and return it as USD value.

#### Check Password
Checks if the password has more than eight characters and if it has at least one number, one uppercase letter and a lowercase letter.

### App

#### Register 
It firstly asks the user for an username, a password and a confirmation for this password and a initial balance. Then, it checks if the username provided already exists in the database. After that, we have some passwords checks, if the password is equal to the confirmation, if the check_password function returns true and if the balance field was filled and if somehow that check fails, the balance will be set at zero dollars. Finally, it inserts this data into the users table, the password is not inserted itself, but a unique hash, then it redirects the user to a registered page.

#### Login
Clears any past user id then gets an username and a password, checks if this username exist in the users table and if it does verifies if the password hash matchs with that respective username hash and then takes the user to the homepage.

#### Log Out
Clears any past user id then redirects the user to login page.

#### Index
The app homepage, it shows to user the month transactions and a chart that contains the user's incomes and expenses.

#### Income
Asks the user to add a income, specifing its name and value and if the value is an actual number, the data is inserted into the income table and into the history table and the value is added to the cash value in the users table. It also creates a chart with the month incomes.

#### Expense
Asks the user to add a expense, specifing its name and value and if the value is an actual number, the data is inserted into the expense table and into the history table and the value is subtracted to the cash value in the users table. It also creates a chart with the month expenses.

#### History
Displays the user's transactions history

#### Conversor
Asks the user for current currency, the value and a target currency then it outputs the converted value to the user.