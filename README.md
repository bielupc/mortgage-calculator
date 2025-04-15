
<h1 align="center">
  Mortgage Calculator
  <br>
</h1>

<h4 align="center"><a href="https://mortgage-calculator.streamlit.app/" target="_blank">Financial tool</a> to calculate losses due to the change of yearly interest rate.</h4>

<br>
<p align="center">
<a href="https://www.linkedin.com/in/biel-altimira-tarter/"><img src="https://img.shields.io/badge/LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white"></a>
</p>

<p align="center">
  <a href="https://mortgage-calculator.streamlit.app/">
    <img src="mockup.png"
         alt="mockup">
  </a>
</p>

## 🔍 About

This mortgage calculator provides a way to calculate amortization tables for mortgages with `variable interest rates` with `any frequency of variation` and `early repayments`. The main goal of the app is to show how much extra interest money has been paid due to a variation of the real anual interest rate.



## 🏗️ Deployment

This project was deployed using [Streamlit](https://streamlit.io/), an easy library to share data apps. The website might not be available if not used regularly, so feel free to contact if redeployment is needed or try to test the code by yourself using the following section.
## 🔨 Installation

The project can be ran and inspected locally by installing all the necesary requirements from the `requirements.txt` file provided, which can install all the required packages into your current environment using: 

```bash
  pip install -r requirements.txt
```

Once the requirements have been met, run 

```bash
    streamlit run app.py
```

to start the app, and a browser window will apper with a visual explanation on how the website works.



    
## 🖱️ Usage

To use the app, you can simply follow the instruction in the video provided in catalan. Which simplifies to loading two excel files in `.xlsx` format and entering some variables, if you find the video confusing or do not understand catalan, here's an explanation on how this works.

### Interest rates file
The first one contains the interest reates applied at each revision. The format to be followed are three columns, the first one in `MM/YYYY` format containing the month and year of the revision and application of the new interest rate. The next two columns contain the real interest and the rounded interest rate expressed as a `%`and using the `coma` as the decimal separator.

Here's an example of three entries of the table.

| 11/2002 | 3,06 | 3,8  |
|---------|------|------|
| **11/2003** | **3,08** | **4,23** |
| **11/2004** | **2,98** | **3,01** |


### Early repayments file
The second file contains the early repayments applied at certain time during the payment of the mortgage. The format to be followed are two columns, the first one in `MM/YYYY` format containing the month and year when the early repayment was made. The second column will contain the amount of money that was paid. Bare in mind that the thousands separator is not needed and you should use a `coma` to indicate the decimal values. 

Also note that for the interests file, you need an entry for each quota revision, whereas for the early repayments, you just need an entry for the months money paid in advance.

Here's an example:
| 01/2002 | 4000 |
|---------|------|
| **07/2007** | **2000,32** |
| **06/2009** | **400,11** |

### Variables
Now you just need to enter the total mortgage capital, the payment term in years and the frequency of revisions in months. For example: 
- You might have to pay 100.000,34€
- in 20 years
- with a quota changing annually (enter 12)

### Statistics
After this, you will get a summary of your mortgage and a plot of all your data. Make sure to check for any mistakes. Right after, you will be able to see all the statistics and metrics of your losses due to the change of the two interests provided for every revision. It will display the amount of interest paid with the proper rate, the amount paid with the rounded interest and the difference together with a graph of this different for every payment at the indicated frequency.
## ⭐ Features


- The data can be imported and exported with excel spread sheets.
- The calculator can be used for mortgage conditions with variable interest rates.
- A way to handle early repayments is also implemented.
- Clear UI with clear conclusions of the extra money spent.



## 🚀 About Me
Check out more about my work in my [GitHub profile](https://github.com/BielAltimira/price) or visit my [LinkedIn profile](https://www.linkedin.com/in/biel-altimira-tarter/).


