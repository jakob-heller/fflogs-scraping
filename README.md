<img align="right" width="80" height="80" src="docs/img/fflogs_icon.png" alt="fflogs icon">

# fflogs-scraping
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
5. [Documentation](#docs)
6. [Why Selenium?](#selenium)
7. [Why Dash?](#dash)

<a name="introduction"></a>
## Introduction

<a name="goal"></a>
### Goal and Motivation

The website fflogs.com allows extensive analysis of combat data from the video game Final Fantasy XIV, including metrics like "damage done" and "healing". While you are able to analyze date over whole log files that were uploaded; looking at, and summarizing data across multiple logs is not possible. This project's purpose is to implement this functionality in a limited manner.  

It should be able to
1. take user inputs, indicating what logs to analyze and other parameters,
2. scrape "damage" and "healing" data from all logs,
3. summarize/ merge the data in an appropriate way and
4. visualize it.

<a name="structure"></a>
### Structure

```
fflogs-scraping
├── src
│   ├── fflogs-scraping
│   │   ├── data
│   │   │   ├── assets
│   │   │   │   └── style.css
│   │   │   ├── csv
│   │   │   │   └── placeholder.csv
│   │   │   ├── __init__.py
│   │   │   ├── combination.py
│   │   │   ├── scraping.py
│   │   │   └── visualization.py
│   │   ├── __init__.py
│   │   ├── __main__.py
│   │   ├── main.py
│   │   └── user_input.py
│   ├── geckodriver.exe
│   └── ublock_origin-1.43.0.xpi
├── .gitignore
├── LICENSE.txt
├── MANIFEST.in
├── README.rst
├── requirements.txt
├── setup.cfg
└── setup.py
```

<a name="reqs"></a>
## Requirements

* Python 3.10
> `user_input.py` makes use of the `match-case` syntax ([structural pattern matching](https://docs.python.org/3/whatsnew/3.10.html)). This was introduced in Python 3.10.

* Selenium
* BeautifulSoup4
> `data.scraping` methods make use of both [Selenium](https://www.selenium.dev/documentation/webdriver/) and [BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/bs4/doc/).
> Conveniently, fflog entries offer `download csv` buttons for all their tables. We can utilize those with Selenium so that we don't have to manually fetch table data from html.
> We still use beautifulsoup to fetch the group composition from html.

* Pandas

* Firefox
> Since we use a Firefox webdriver we need a full-install of [Firefox](https://www.mozilla.org/en-US/firefox/new/).

* Geckodriver
> For our Firefox webdriver to run, Geckodriver needs to be installed. More on information on this in [Getting Started](#start). (a Chrome Webdriver would need Chromedriver)

<a name="start"></a>
## Getting Started

<a name="windows"></a>
### Windows
To use this package, directly install the conda environment from the .yml, using

```
conda env create -f environment.yml
```

Activate the environment

```
conda activate fflogs3.10
```

Navigate to the `src` directory and run

```
python fflogs-scraping
```

To work on this package, please install the dependencies from `requirements.txt` in your (Python 3.10) environment, using

```
pip install -r requirements.txt
```
This includes `sphinx` for creating the documentation and `tox` for testing.
### Unix/macOS
Geckodriver needs to be installed for the Firefox Webdriver to work. On Windows, it is sufficient for the executable to be in the working directory. On other operating systems that might not work. Please refer to [this](https://askubuntu.com/questions/870530/how-to-install-geckodriver-in-ubuntu) post for solutions.

After having installed geckodriver, continue as described in [Windows](#windows).

<a name="expl"></a>
## Example

For the example we will look at the predefined logs 2. The set consists of 2 logs that have boss kills in them ([1](https://www.fflogs.com/reports/hacvwXKb8mFYrAdx), [2](https://www.fflogs.com/reports/LnjBh2tfZRyv8rpD)).

<a name="input"></a>
### User Input
On run we are prompted with a user input:  
<img src="docs/img/input_prompt.png" alt="User Input Prompt" width="600"/>  
The available parameters should be explained sufficiently. Since we want to analyze boss kills from set 2 in this example, we input "2" and "kills". If you want to see the scraping process, you can input "show" and the webdriver will be visible.  "config" shows the parameters that will be returned. Input "run" to start the scraping.

<img src="docs/img/first_input.gif" alt="Example User Input" width="600"/>  

<a name="scraping"></a>
### Scraping

We can now take a look at what the scraping process (implemented in `data.scraping`) is going to do. The following will be repeated for every url we provide (2 times in this case). If we open the [first](https://www.fflogs.com/reports/hacvwXKb8mFYrAdx) log and click on "All Kills (2)" we land on this summary page:  
> Note: The webdriver isn't actually clicking anywhere - it navigates by modifying the url. I just explain it like this so you can retrace its steps more easily.
<img src="docs/img/summary_page.png" alt="Summary Page" width="600"/>  

On this page, the contents of the "Raid Composition" table will be fetched to make sure that the group composition in every log is the same. We check classes/jobs instead of player names - these are indicated by the icons and colors (to understand the reasons for this is not important for this project).  

<img src="docs/img/composition_table.png" alt="Composition table" width="600"/>  

Next, the webdriver navigates do the subpage for "damage done". We can get there by clicking on the "Damage Done" tab.  

<img src="docs/img/damage_done_tab.png" alt="Damage Done tab" width="600"/>  

On this page, the webdriver is simply going to download the main table as a csv file, using the "CSV" button on the bottom right. It then repeats the same for the "healing done" suppage.  

<img src="docs/img/damage_done_page.png" alt="Damage Done page" width="600"/>  

<a name="sum"></a>
### Data Summary

In `data.combination` the csv files just downloaded will be read into pandas dataframes and summarized.

<a name="viz"></a>
### Data Visualization

When all this is finished, the terminal will show where the Dash app is running:  
<img src="docs/img/finished_processing.gif" alt="Dash started" width="600"/>  

Open this (e.g. in your browser) and you will see this dashboard with sortable columns:
<img src="docs/img/dashboard.gif" alt="Dashboard" width="600"/>  

<a name="docs"></a>
## Documentation
The code was written and documented following the [Google Python Style Guide](https://google.github.io/styleguide/pyguide.html).
> There are 5 single lines where the line length of 80 (as required by both Pep8 and Google Style) was exceeded, because I decided that in those few cases, splitting the line would harm readability more than it would help.
> Note that docstring conventions in Google Style are slightly different from PEP257 - the first line for example, should be descriptive-style, rather than imperative-style. This may or may not be marked as wrong by your linter.

You can find the documentation [here](https://fflogs-scraping.readthedocs.io/en/latest/index.html). It was built using [Sphinx](https://www.sphinx-doc.org/en/master/index.html) and is hosted on [readthedocs](https://docs.readthedocs.io/en/stable/index.html).


<a name="selenium"></a>
## Why Selenium?
In hindsight, this is a good question. Since fflogs offers a "Download CSV" functionality for all of its tables, it seemed to be the most intuitive way for me to implement a program that "just clicks on that button". While it is true that you need Selenium for this kind of functionality, just fetching the table data from html would have been much more effective in all terms, but especially runtime.  

If I would start this project now, I would not use Selenium. Setting up a Webdriver, installing an adblocker only to click on some buttons, where you could just have fetched 2 tables instead is kind of "overkill". Even though it hurts, I will probably create a version completely without Selenium in the future.

<a name="dash"></a>
## Why Dash?
When beginning this project I said that I'd like to visualize the merged data, preferably somewhat interactively. I started with using Plotly as introduced in the lecture and while looking something up in its documentation, I read about Dash. It sounded interesting enough to give it a try; in the end it let me visualize the data in exactly the way I wanted (sortable table with an in-cell bar chart, like on the original website).
