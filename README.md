# Automated Cookie Clicker Bot
This Python program utilises the powerful browser automation capabilities of Selenium WebDriver to develop a strategy to play the popular Cookie Clicker game (links provided below). Users can create their very own cookie clicker bot by using the class defintion from `cookie_clicker.py` (see Project Files) to implement a game strategy to generate the greatest number of cookies in the shortest span of time. This can be devised through optimising the choice of buying upgrades based on game variables provided by class attributes.

Manually play the classic version of the Cookie Clicker game: https://orteil.dashnet.org/experiments/cookie/

Link to Selenium WebDriver: https://www.selenium.dev/documentation/webdriver/getting_started/install_library/

## Prerequisites
- Python 3.x installed on your machine.
- Required Python packages installed:
  - Selenium WebDriver:

`>> pip install selenium`
- Ensure you have Chrome installed on your system.

## Project Files
1. `main.py`: create and execute your own algorithmic cookie clicker strategy by utilising the cookie clicker bot.
2. `cookie_clicker.py`: defines the main `CookieClickerBot()` class housing the necessary logic to implement web scraping and buying upgrades for the web browser game.

## Usage
Run the `main.py` file to see a bot implemented with a simple strategy play the cookie clicker game.

## Objectives & Strategy
- When instantiating your bot, specify a target cookies value to reach, specified using the `cookies_target` input parameter.
- The objective is to devise a temporal upgrade buying algorithm to generate the target cookies in the fastest amount of time.
- Utilising its class attributes, a cookie clicker bot can buy upgrades based on various factors such as resource availability, cost-effectiveness, and impact on performance.
- An example default strategy is implemented as `simple_strategy()`, which buys the most affordable upgrade available at specified intervals.

## Outputs
- While running the program, messages can be printed to your terminal or command window by calling the `print_stats()` method:
```
time elapsed: 05:21 (320.86 secs)
total webdriver clicks: 3,095 (9.65 clicks/s)
----------------------------------------
target cookies to generate: 25,000
total cookies generated: 11,912 (13,088 remaining)
----------------------------------------
current cookies: 132
upgrades bought: 43 (5,602 cookies spent)
cookies/second value: 16.4
```
- When your bot generates the target number of cookies, a text file can be created, by calling the `final_stats()` method, which shows you the final statistics of your strategy, including the time taken as well as the number and type of upgrades bought during the automated process:
```
FINAL STATISTICS:

- 'simp_strat_bot' generated 25,184 cookies in 08:15.
- 54 upgrades were bought from spending 10,495 cookies.
- The final 'cookies/second' rate value reached was 35.8 clicks/s.
- 4,704 total webdriver clicks were processed (9.50 clicks/s).

UPGRADES BREAKDOWN:
{
  "Cursor": 34,
  "Grandma": 17,
  "Factory": 3
}
```
