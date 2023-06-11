"""
******************************************************************************************
** COMP517 Continuous Assessment Task 2 - Bank Accounts                                 **
** NAME: RAHUL NAWALE                                                                   **
** STUDENT ID - 201669264                                                               **
** TASK - Design and implement two classes in Python: BasicAccount and PremiumAccount.  **
**                                                                                      **
******************************************************************************************
       %%%%       %%%%%     %%%        %%%  %%% %%%%     %%%%%%%%%  %%%  %%%%%%%%
     %%%  %%%   %%%    %%%  %%% %%  %% %%%  %%%     %%%  %%         %%%      %%%%
     %%%        %%%    %%%  %%%   %%   %%%  %%%     %%%  %%%%%      %%%      %%%
     %%%        %%%    %%%  %%%        %%%  %%% %%%%          %%%   %%%     %%%
     %%%  %%%   %%%    %%%  %%%        %%%  %%%               %%%   %%%    %%%
      %%%%        %%%%%     %%%        %%%  %%%          %%%%%      %%%   %%%
===========================================================================================
"""

# Libraries
import random  # Random variable generator.
import datetime  # Supply classes for manipulating dates and times.


# Class for Basic Account
# This class Stores and includes Basic account information like Name, Balance etc.
# This class also contains further functions e.g. deposit, withdraw etc.
class BasicAccount:
    accNumCount = 0 # Static variable to assign series of account number.
    cards = list()  # list to hold all Card numbers.

    # Initializer giving the account name and opening balance.
    def __init__(self, name, current_balance):
        self.name = name  # Name of account holder
        self.balance = current_balance  # Account Balance
        BasicAccount.accNumCount += 1  # Account number increments
        self.acNum = BasicAccount.accNumCount

    # function for deposit
    # Deposits the stated amount into the account, and adjusts the balance appropriately.
    def deposit(self, amount):
        self.amount = amount  # Amount to deposit

        # Adding deposited amount to initial balance
        if self.amount > 0:
            self.balance = self.balance + self.amount
        else:
            print("Please provide a positive amount")  # Deposits must be a positive amount.

        # Overdraft is considered only for Premium Accounts
        if type(self) == PremiumAccount:
            if self.balance < 0:
                self.overdraft = True
            else:
                self.overdraft = False

    # function for withdraw
    # Withdraws the stated amount from the account
    def withdraw(self, amount):

        self.amount = amount

        # Check balance before withdrawing
        if type(self) == BasicAccount:
            if self.amount > self.balance:
                print("Can not withdraw £{}".format(self.amount))  # Insufficient Balance
            else:
                self.balance = self.balance - self.amount
                # prints a message of “<Name> has withdrawn £<amount>. New balance is £<amount>”.
                print("{} has withdrawn £{}. New balance is £{}\n".format(self.name, self.amount, self.balance))

        # for Premium account
        else:
            self.overallBalance = self.balance + self.overdraftLimit

            if self.amount > self.overallBalance:
                print("Can not withdraw £{}".format(self.amount))
            else:
                self.balance -= self.amount
                if self.balance < 0:
                    self.overdraft = True
                else:
                    self.overdraft = False
                # prints a message of “<Name> has withdrawn £<amount>. New balance is £<amount>”.
                print("{} has withdrawn £{}. New balance is £{}\n".format(self.name, self.amount, self.balance))

    # function for Available Balance.
    # Returns the total balance that is available in the account as a float.
    # It should also take into account any overdraft that is available.
    def getAvailableBalance(self):
        return float(self.balance)

    # function for balance in the account.
    # returns the balance of the account as a float.
    # If the account is overdrawn, then it should return a negative value.
    def getBalance(self):
        return float(self.balance)

    # Should print to screen the balance of the account.
    # If an overdraft is available, then this should also be printed.
    # And it should show how much overdraft is remaining.
    def printBalance(self):
        print("Balance of your account is: £{} ".format(self.balance))

    # function for Name.
    # Returns the name of the account holder as a string.
    def getName(self):
        return f"{self.name}"

    # function for Account Number.
    # Returns the account number as a string.
    def getAcNum(self):
        return f"{self.acNum}"

    # function for New Card.
    # Creates a new card number, with the expiry date being 3 years to the month from now.
    # (e.g., if today is 1/12/21, then the expiry date would be (12/24)).
    def issueNewCard(self):
        while True:
            self.cardNum = str(random.randint(0, pow(10, 16) - 1)).zfill(16)
            if self.cardNum not in BasicAccount.cards:
                BasicAccount.cards.append(self.cardNum)
                break
        expiry_date = datetime.datetime.now() + datetime.timedelta(days=3 * 365)
        expiry_month = expiry_date.month
        expiry_year = int(expiry_date.strftime("%y"))
        self.cardExp = (expiry_month, expiry_year)

    # function for Close Account
    # To be called before deleting of the object instance.
    # Returns any balance to the customer (via the withdraw method) and returns True.
    # Returns False if the customer is in debt to the bank
    def closeAccount(self):
        if self.balance < 0:
            # prints message “Can not close account due to customer being overdrawn by £<amount>”.
            print("Can not close account due to customer being overdrawn by £{}".format(self.balance))
            returnValue = False
        else:
            self.withdraw(self.balance)
            returnValue = True

        return returnValue

    def __str__(self):
        return f"Account Details:\nAccount holder's name: {self.name}\nAccount balance: {self.balance} "


class PremiumAccount(BasicAccount):

    # Initializer giving the account name, opening balance, and overdraft limit (0 or above).
    def __init__(self, name, current_balance, previous_overdraft):
        BasicAccount.__init__(self, name, current_balance)
        self.overdraftLimit = previous_overdraft
        self.overdraft = False

    # function for Overdraft Limit
    # Sets the overdraft limit to the stated amount
    def setOverdraftLimit(self, updated_limit):
        self.overdraftLimit = updated_limit

    # function for Available Balance.
    # Returns the total balance that is available in the account as a float.
    # It should also take into account any overdraft that is available.
    def getAvailableBalance(self):
        return float(self.balance + self.overdraftLimit)

    # Should print to screen the balance of the account.
    # If an overdraft is available, then this should also be printed.
    # And it should show how much overdraft is remaining.
    def printBalance(self):
        if self.overdraft == True:
            print(
                "Balance of your account : {} \n and an overdraft is possible with a limit of £{}.\nYour overdraft "
                "balance is  £{} ".format(
                    self.balance, self.overdraftLimit, self.overdraftLimit + self.balance))
        else:
            print(
                "Balance of your account : {} and an overdraft is possible.\nYour overdraft limit and overdraft "
                "balance is  £{} ".format(
                    self.balance, self.overdraftLimit))

    # function for Close Account
    # This function will simply do the relevant "housekeeping" in the account, and return a Boolean value.
    def closeAccount(self):
        if self.overdraft == True:
            print("Can not close account due to customer being overdrawn by £{}".format(abs(self.balance)))
            returnValue = False
        else:
            self.withdraw(self.balance)
            returnValue = True
        return returnValue

    # Implementation of string methods for each class
    def __str__(self):
        return f"Account Details:\nAccount holder's name: {self.name}\nAccount balance: {self.balance}\n" \
               f"Overdraft available {self.overdraftLimit} "

