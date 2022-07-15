# fflogs-study-project
Scrape [fflog](https://www.fflogs.com/) entries for damage done and healing done tables, combine data from multiple logs and then visualize using a dash dashboard.

## Requirements

* Python 3.10
> `user_input.py` makes use of the `match-case` syntax ([structural pattern matching](https://docs.python.org/3/whatsnew/3.10.html)). This was introduced in Python 3.10.

* Selenium
* BeautifulSoup4
> `data_scraping.py` methods make use of both [Selenium](https://www.selenium.dev/documentation/webdriver/) and [BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/bs4/doc/).
> Conveniently, fflog entries offer `download csv` buttons for all their tables. We can utilize those with Selenium so that we don't have to manually fetch table data from html.
> We still use beautifulsoup to fetch the group composition from html.

* Pandas

## Example

For the example we will look at the predefined logs 2. The set consists of 2 logs that have boss kills in them ([1](https://www.fflogs.com/reports/hacvwXKb8mFYrAdx), [2](https://www.fflogs.com/reports/LnjBh2tfZRyv8rpD)).

### User Input
On run we are prompted with a user input:  
<img src="img/input_prompt.png" alt="User Input Prompt" width="600"/>  
The available parameters should be explained sufficiently. Since we want to analyze boss kills from set 2 in this example, we input "2" and "kills". If you want to see the scraping process, you can input "show" and the Webdriver will be visible.  "config" shows the parameters that will be returned.    
<img src="img/first_input.gif" alt="Example User Input" width="600"/>  
Text.  
<img src="img/finished_processing.gif" alt="Dash started" width="600"/>  

## (README is still WIP – this is just the preliminary project description)

# Combination (and Visualization) of Logs uploaded to FFlogs.com[^1]


## Goal (and context)

There exists a tool to collect and upload extensive combat data in the online video game “Final Fantasy XIV”. [FFlogs.com](https://www.fflogs.com/), the site where these log files are uploaded then allows in-depth analysis of this data. It already offers sufficient tools to filter and visualize data by itself ([here](https://www.fflogs.com/reports/a:VrNFghvTcL3J48WK#fight=4&type=summary) is an example log) but there is one shortcoming that I would like to address:

While the website is able to summarize combat data over the whole log file, analyzing multiple files at once is not possible.  \
I would like to create a tool that (1) lets me indicate what logs (usually separated into days) I want to have summarized, (2) accesses/ scrapes the data (only limited metrics), (3) summarizes it in an appropriate way and (4) visualizes it (preferably somewhat interactively).


## Required Steps (4)


### (Step 0:)

Generate and upload data. Since there are hundreds of thousands of logs already available (and I regularly upload some myself) this should not be an issue at all.


### Step 1:

User input. The user has to provide the logs that should be analyzed in some kind of way – either by their direct links or by specifying dates. Since a fancy user interface is not a priority, this can stay in the console (no extra libraries needed).


### Step 2:

Access and scrape data. This step will use scraping libraries like _Requests_ and _Beautiful Soup_; _Selenium _might be necessary as well.  \
Here I need to decide what data I actually want to include in my final visualization – I will probably start with only including the basic metrics “Damage Done” and “Healing Done”. This can always be adjusted to include more metrics when the project is at a further state.


### Step 3:

Clean up and summarize data. This step will use the appropriate libraries introduced in the course, namely _numpy_ and _pandas_.


### Step 4:

Visualize data. This step will use _matplotlib_, but libraries like _plotly_ to create a more interactive visualization also seem reasonable.


<!-- Footnotes themselves at the bottom. -->
## Notes

[^1]:
     There exists an equivalent site for the game “World of Warcraft” which is probably better known – what I am planning should work for both, but I chose FFlogs since that’s what I actually use myself.
