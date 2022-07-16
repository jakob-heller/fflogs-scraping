<img align="right" width="80" height="80" src="img/fflogs_icon.png" alt="fflogs icon">

# fflogs-study-project
Scrape [fflog](https://www.fflogs.com/) entries for damage done and healing done tables, combine data from multiple logs and then visualize using a dash dashboard.

# Table of contents
1. [Introduction](#introduction)
    1. [Goal and Motivation](#goal)
    2. [Structure](#structure)
2. [Requirements](#reqs)
3. [Getting Started](#start)
4. [Example](#expl)
    1. [User Input](#input)
    2. [Scraping](#scraping)
    3. [Data Summary](#sum)
    4. [Data Visualization](#viz)

<a name="introduction"></a>
## Introduction

<a name="goal"></a>
### Goal and Motivation

<a name="structure"></a>
### Structure

<a name="reqs"></a>
## Requirements

* Selenium
* BeautifulSoup4
> `data_scraping.py` methods make use of both [Selenium](https://www.selenium.dev/documentation/webdriver/) and [BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/bs4/doc/).
> Conveniently, fflog entries offer `download csv` buttons for all their tables. We can utilize those with Selenium so that we don't have to manually fetch table data from html.
> We still use beautifulsoup to fetch the group composition from html.

* Pandas

* Firefox
> Since we use a Firefox Webdriver we need a full-install of Firefox.

<a name="start"></a>
## Getting Started

To use this package, simply clone the repository and install the dependencies in `requirements.txt` in you environment. Navigate to the `src` directory and run

```
python fflogs-study-project
```

<a name="expl"></a>
## Example (screenshots outdated)

For the example we will look at the predefined logs 2. The set consists of 2 logs that have boss kills in them ([1](https://www.fflogs.com/reports/hacvwXKb8mFYrAdx), [2](https://www.fflogs.com/reports/LnjBh2tfZRyv8rpD)).

<a name="input"></a>
### User Input
On run we are prompted with a user input:  
<img src="img/input_prompt.png" alt="User Input Prompt" width="600"/>  
The available parameters should be explained sufficiently. Since we want to analyze boss kills from set 2 in this example, we input "2" and "kills". If you want to see the scraping process, you can input "show" and the Webdriver will be visible.  "config" shows the parameters that will be returned. (Note: 'y' and 'q' in the screenshots have been replaced by 'run' and 'exit', respectively)

<img src="img/first_input.gif" alt="Example User Input" width="600"/>  

<a name="scraping"></a>
### Scraping

We can now take a look at what the scraping process (implemented in `data_scraping.py`) is going to do. The following will be repeated for every url we provide (2 times in this case). If we open the [first](https://www.fflogs.com/reports/hacvwXKb8mFYrAdx) log and click on "All Kills (2)" we land on this summary page:  
> Note: The Webdriver isn't actually clicking anywhere - it navigates by modifying the url. I just explain it like this so you can retrace its steps more easily.
<img src="img/summary_page.png" alt="Summary Page" width="600"/>  

On this page, the contents of the "Raid Composition" table will be fetched to make sure that the group composition in every log is the same. We check classes/jobs instead of player names - these are indicated by the icons and colors (to understand the reasons for this is not important for this project).  

<img src="img/composition_table.png" alt="Composition table" width="600"/>  

Next, the Webdriver navigates do the subpage for "damage done". We can get there by clicking on the "Damage Done" tab.  

<img src="img/damage_done_tab.png" alt="Damage Done tab" width="600"/>  

On this page, the Webdriver is simply going to download the main table as a csv file, using the "CSV" button on the bottom right. It then repeats the same for the "healing done" suppage.  

<img src="img/damage_done_page.png" alt="Damage Done page" width="600"/>  

<a name="sum"></a>
### Data Summary

In `data_combination.py` the csv files just downloaded will be read into pandas dataframes and summarized.

<a name="viz"></a>
### Data Visualization

When all this is finished, the terminal will show where the Dash app is running:  
<img src="img/finished_processing.gif" alt="Dash started" width="600"/>  

Open this (e.g. in your browser) and you will see this dashboard with sortable columns:
<img src="img/dashboard.gif" alt="Dashboard" width="600"/>  
