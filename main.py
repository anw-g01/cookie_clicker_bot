from cookie_clicker import CookieClickerBot
import os


def simple_strategy(bot: CookieClickerBot) -> None:
    """
    This simple strategy scrapes the browser every specified interval
    of seconds and buys the most affordable upgrade at the given interval.
    """
    start_time = bot.start_time                             # keep track of starting time
    given_time = (bot.calc_current_time() - start_time)     # calc time at any given moment when method is called
    interval = 4                                            # specify interval of time (sec) for bot to act on a decision and print stats
    # ----- run automatic cookie clicker bot ----- #
    while bot.total_cookies < bot.target:                   # run loops until target money (cookies) is reached
        bot.click_cookie()                                  # click the cookie button
        elapsed_time = bot.calc_elapsed_time()              # calc elapsed time
        if elapsed_time > given_time + interval:            # every 'interval' seconds
            bot.update_scrapes()                            # update scraped stats from browser BEFORE buying upgrades
            bot.print_stats()                               # statistics will always lag one time-step
            # --- upgrading algorithm -- #
            upgrade = None                                  # find an affordable upgrade to buy
            for name, info in bot.upgrades.items():
                if info["price"] <= bot.money:
                    upgrade = name                          # traverses dictionary until highest affordable upgrade is found
                else:
                    break                                   # stop traversing when highest upgrade is found
            if upgrade is not None:                         # buy if an affordable upgrade was found
                bot.buy_upgrade(upgrade)
            given_time = elapsed_time                       # update stamp for next printing point0
    bot.final_stats()                                       # stores final stats into a text file


if __name__ == "__main__":

    TARGET = 25_000
    BOT_NAME = "simp_strat_bot"

    # --- instantiate cookie clicker bot --- #
    my_bot = CookieClickerBot(
        bot_name=BOT_NAME,          # name of your bot to refer to
        cookies_target=TARGET,      # specify target number of cookies to reach in the fastest time
        toggle_nums=True            # choose whether to display numbers in the browser when clicking
    )

    # --- run your strategy --- #
    simple_strategy(my_bot)
