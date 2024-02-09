from selenium import webdriver
from selenium.webdriver.common.by import By
import time, json, os


def clear_screen():
    """
    Clears the screen before every print message in the terminal.
    """
    os.system('cls' if os.name == 'nt' else 'clear')


class CookieClickerBot:

    def __init__(self, bot_name: str, cookies_target: int, toggle_nums=True):
        self.name = bot_name  # bot name to refer to in final message text file
        self.target = cookies_target  # number of generated cookies until game completion
        self._toggle_numbers(toggle_nums)  # toggle on/off numbers display
        self.url = "https://orteil.dashnet.org/experiments/cookie/"  # Chrome website URL for cookie clicker game
        self.driver = self._create_webdriver()  # Selenium WebDriver
        # ********* gameplay statistics ********* #
        self.start_time = time.time()  # starting time of instantiation
        self.webdriver_clicks = 0  # running count of all clicks made by webdriver
        self.bought_upgrades = 0  # running count of no. of bought upgrades
        self.cookies_spent = 0  # running count of cookies spent on upgrades
        self.total_cookies = 0  # running count of all time cookies generated
        self.text_file = f"{self.name}_stats.txt"  # text file name containing the final stats after a given run
        # ********* attributes to be scraped ********* #
        self.money = 0  # count of current cookies available
        self.clicks_rate = 0  # current cookies/second value obtained from upgrades
        self.upgrades = self._scrape_upgrades()  # current prices for each upgrade (dictionary)

    def _toggle_numbers(self, flag=True) -> None:
        """If set to False, toggle numbers is turned off by clicking 'Numbers Off' button in browser."""
        if not flag:
            self.driver.find_element(
                by=By.ID,
                value="toggleNumbers"
            ).click()
        return None

    def _create_webdriver(self) -> webdriver:
        """Returns a WebDriver instance for controlling a Chrome web browser."""
        opts = webdriver.ChromeOptions()  # configure options
        opts.add_experimental_option("detach", True)  # webdriver session to be kept open until closed by command
        driver = webdriver.Chrome(options=opts)  # create webdriver instance
        driver.get(url=self.url)  # open specified URL in a Chrome browser
        return driver

    def _scrape_upgrades(self) -> dict:
        """Scrapes all upgrade elements and stores the names and pricing in a dictionary"""
        elements = self.driver.find_elements(
            by=By.CSS_SELECTOR,
            value="#store div b"
        )[:-1]  # last element seems to be empty
        names = [" ".join(ele.text.split()[:-2]) for ele in elements]  # names of all upgrades as list items
        prices = [int(ele.text.split()[-1].replace(",", "")) for ele in elements]  # changing prices of all upgrades
        upgrades = {}
        for i in range(1, len(elements) + 1):
            upgrades[names[i - 1]] = {  # use upgrade name as the key
                "upgrade no.": i,  # hierarchy of upgrades
                "price": prices[i - 1]  # updating price
            }
        return upgrades

    def click_cookie(self) -> None:
        """Clicks the main cookie button."""
        self.driver.find_element(
            by=By.ID,
            value="cookie"
        ).click()
        self.webdriver_clicks += 1

    def update_scrapes(self) -> None:
        """Scrapes values from browser to update all running counts and stats."""
        self.upgrades = self._scrape_upgrades()  # update upgrade prices within dictionary
        self.money = int(self.driver.find_element(by=By.ID, value="money").text.replace(",", ""))
        self.total_cookies += self.money  # update all time cookies generated
        self.clicks_rate = float(self.driver.find_element(by=By.ID, value="cps").text.split()[-1].replace(",", ""))

    def print_stats(self) -> None:
        """Prints the current stats of the game to be displayed within intervals."""
        clear_screen()
        elapsed_time = self.calc_elapsed_time()
        cookies_left = self.target - self.total_cookies
        print(f"\ntime elapsed: {self.digital_elapsed_time()} ({elapsed_time:.2f} secs)")
        print(f"total webdriver clicks: {self.webdriver_clicks:,} ({self.webdriver_clicks / elapsed_time:.2f} clicks/s)")
        print("-" * 40)
        print(f"target cookies to generate: {self.target:,}")
        print(f"total cookies generated: {self.total_cookies:,} ({cookies_left:,} remaining)")
        print("-" * 40)
        print(f"current cookies: {self.money:,}")
        print(f"upgrades bought: {self.bought_upgrades} ({self.cookies_spent:,} cookies spent)")
        print(f"cookies/second value: {self.clicks_rate}")

    def calc_current_time(self) -> float:
        """Returns the current running time in seconds since 1st Jan 1970, using the time module."""
        elapsed_time = self.calc_elapsed_time()
        return elapsed_time - self.start_time

    def calc_elapsed_time(self) -> float:
        """Returns the calculated elapsed time since instantiating the cookie clicker bot."""
        return time.time() - self.start_time

    def digital_elapsed_time(self) -> str:
        """Returns the current elapsed time in digital padded string format."""
        elapsed_time = self.calc_elapsed_time()  # elapsed time in seconds
        minutes = round(elapsed_time // 60)
        seconds = round(elapsed_time % 60)  # take remainder as seconds
        return f"{minutes:02}:{seconds:02}"

    def buy_upgrade(self, upgrade_name: str) -> None:
        """Buys a given upgrade by scraping its element on the browser and clicking it."""
        upgrade = self.driver.find_element(
            by=By.ID,
            value=f"buy{upgrade_name}"  # element value found through name format
        )
        upgrade.click()
        self.cookies_spent += self.upgrades[upgrade_name]["price"]  # update cookies spent before price change
        self.bought_upgrades += 1  # increment count of bought upgrades

    def _upgrades_breakdown(self) -> dict:
        """Creates a final dictionary of the type and number of upgrades bought for a given completed strategy."""
        elements = self.driver.find_elements(
            by=By.CLASS_NAME,
            value="amount"
        )
        amounts = [int(e.text) for e in elements]
        upgrades = [upgrade for upgrade in self.upgrades.keys()]
        return {upgrades[i]: amounts[i] for i in range(len(amounts))}

    def final_stats(self) -> None:
        """Display final stats and breakdown of no. of upgrades bought into a text file."""
        elapsed_time = self.calc_elapsed_time()
        cps = self.webdriver_clicks / elapsed_time
        upg_breakdown = self._upgrades_breakdown()
        with open(f"{self.text_file}", "w") as file:
            file.write("FINAL STATISTICS:")
            file.write(f"\n\n- '{self.name}' generated {self.total_cookies:,} cookies in {self.digital_elapsed_time()}.")
            file.write(f"\n- {self.bought_upgrades} upgrades were bought from spending {self.cookies_spent:,} cookies.")
            file.write(f"\n- The final 'cookies/second' rate value reached was {self.clicks_rate} clicks/s.")
            file.write(f"\n- {self.webdriver_clicks:,} total webdriver clicks were processed ({cps:.2f} clicks/s).")
            file.write("\n\nUPGRADES BREAKDOWN:")
            file.write(f"\n{json.dumps(upg_breakdown, indent=2)}")
        self._read_stats_file(self.text_file)

    def _read_stats_file(self, file_name):
        """Reads and prints the contents of the text file."""
        clear_screen()
        with open(self.text_file, "r") as file:
            contents = file.read()
        print(f"\n{contents}")


if __name__ == "__main__":

    # --- test web scraping content --- #
    bot = CookieClickerBot("test_bot", 100)
    print(json.dumps(bot.upgrades, indent=4))
    bot.print_stats()
    print(type(bot.upgrades["Time machine"]["price"]))
    bot.driver.quit()
