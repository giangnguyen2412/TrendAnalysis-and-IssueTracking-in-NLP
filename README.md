# Trend Analysis and Issue Tracking in NLP with Python

## Trend Analysis
Given a collection of newspaper articles for three years:
```
Find the top 10 issues for each year and rank them based on prominence and salience 
Extract issues from the article collection  
Find a ranking method that can represent the prominence of the issues within the article collection 
Extract a description out of the articles that are related to an issue 
```
## Issue Tracking
From top issues
```
Pick 2 issues for analyzing  
Each issue identifying at least 10 events 
For each event, their outstanding attributes need to be extracted 
Identify two different types of events: inter-dependent and independent
```
## Getting Started
Please make sure that you already have the dataset files under data directory before running the code.
1. Install the Python package requirements using command
    pip install -r requirement.txt
```
OLLIE is a JAVA package which need to be placed with the same src directory. OLLIE could be found here: https://knowitall.github.io/ollie/
```
2. Run the programs
```
Move to src directory
Trend Analysis: run the code using command
python trend_analysis.py
When you are done, the result is in src/top_ten.txt. Looking at the file, you can see each 10 issues per year.
Issue tracking: run the code using command
python issue_tracking.py 
When the program is running, you can save the plots for each topic before continuing with the next topic. 
The plot could be seen in src/temp-plot.html
```
``` 
The programs ask you to use available parameters to speed up or not (See Speed Booster in report for details). By accepting,
you will you the paramters from the previous run. Otherwise, you will run as normal and It will take longer time.
```
## Prerequisites
Refer the requirement.txt for details

## Authors
* Giang. Nguyen
* Kalkbrenner Lydia
* Oberwegner Phillip

## License
This project is licensed under the MIT License - see the LICENSE.md file for details

