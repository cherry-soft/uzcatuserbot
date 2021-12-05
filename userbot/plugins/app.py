"""
Fetch App Details from Playstore.
.app <app_name> to fetch app details.
  © [cHAuHaN](http://t.me/amnd33p)
"""

import bs4
import requests

from . import ALIVE_NAME, catub, edit_or_reply

plugin_category = "utils"


@catub.cat_cmd(
    pattern="app ([\s\S]*)",
    command=("app", plugin_category),
    info={
        "header": "Play Marketdan dastur qidirish",
        "description": "Play Marketdan bir yoki bir nechta so'zlar bilan dastur qidirtira olasiz",
        "usage": "{tr}app <dastur nomi>",
    },
)
async def app_search(event):
    "Play Marketdan narsa qidirish."
    app_name = event.pattern_match.group(1)
    event = await edit_or_reply(event, "`Qidirilyapti!..`")
    try:
        remove_space = app_name.split(" ")
        final_name = "+".join(remove_space)
        page = requests.get(
            "https://play.google.com/store/search?q=" + final_name + "&c=apps"
        )
        str(page.status_code)
        soup = bs4.BeautifulSoup(page.content, "lxml", from_encoding="utf-8")
        results = soup.findAll("div", "ZmHEEd")
        app_name = (
            results[0].findNext("div", "Vpfmgd").findNext("div", "WsMG1c nnK0zc").text
        )
        app_dev = results[0].findNext("div", "Vpfmgd").findNext("div", "KoLSrc").text
        app_dev_link = (
            "https://play.google.com"
            + results[0].findNext("div", "Vpfmgd").findNext("a", "mnKHRc")["href"]
        )
        app_rating = (
            results[0]
            .findNext("div", "Vpfmgd")
            .findNext("div", "pf5lIe")
            .find("div")["aria-label"]
        )
        app_link = (
            "https://play.google.com"
            + results[0]
            .findNext("div", "Vpfmgd")
            .findNext("div", "vU6FJ p63iDd")
            .a["href"]
        )
        app_icon = (
            results[0]
            .findNext("div", "Vpfmgd")
            .findNext("div", "uzcko")
            .img["data-src"]
        )
        app_details = "<a href='" + app_icon + "'>📲&#8203;</a>"
        app_details += " <b>" + app_name + "</b>"
        app_details += (
            "\n\n<code>Dasturchisi :</code> <a href='"
            + app_dev_link
            + "'>"
            + app_dev
            + "</a>"
        )
        app_details += "\n<code>Reytingi :</code> " + app_rating.replace(
            "Rated ", "⭐ "
        ).replace(" out of ", "/").replace(" stars", "", 1).replace(
            " stars", "⭐ "
        ).replace(
            "five", "5"
        )
        app_details += (
            "\n<code>Hususiyatlari :</code> <a href='"
            + app_link
            + "'>Play Marketda ko'rish</a>"
        )
        app_details += f"\n\n===> {ALIVE_NAME} <==="
        await event.edit(app_details, link_preview=True, parse_mode="HTML")
    except IndexError:
        await event.edit("No result found in search. Please enter **Valid app name**")
    except Exception as err:
        await event.edit("Exception Occured:- " + str(err))
