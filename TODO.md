# TODO

## README

* Add a "comprehensive overview of the project's goal, motivation and structure"
* Add section on how to set up and run the project

## user_input

* Remove match-case from `user_input()` if it really needs to be compatible with Python 3.7
* Add option to specify localhost port (maybe)

## data_scraping

* Change the way the Webdriver interacts with the "CSV" button (`get_damage_dealt()`, `get_healing_done()`) so we can completely remove anything related to cookies from our code
* Add dynamic waiting in `get_damage_dealt()` and `get_healing_done()` for consistency, too make sure the correct table is actually loaded before downloading it
* Think about the way we handle invalid group compositions (prompt new user input?)

## data_visualization

* `parse_colors()` could probably be done in a more compact way (not really important)
