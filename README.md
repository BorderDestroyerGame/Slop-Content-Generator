# Worst Fucking Video I'll Ever Make

Good evening, you are probably here for 1 of 3 reasons. Either you got the link from my Discord Server, you saw the YouTube video I'm going to be making on this, or you're a degenerate like myself who has way too much free time on their hands and yearns for the destruction of the attention spans of everyone under the age of 7. Either way, this code here is a program that automatically generates slop tiktok content in a matter of minutes ready to be published. The code is shit, I won't lie, but I feel as though if I were to make it more user friendly and accessible for everyone it would be the equivalent of Oppenheimer making a portable version of Gadget and then opensourcing the blueprints for it. Despite this, I will be giving a small, BRIEF explanation on how to use the code.

Obviously to start you are going to need to create a python environment and run `pip install -r requirements.txt` first before anything else.

## Part 1: Creating A Reddit App
The first thing you need to do is create an App on the Reddit Apps Page and get the corresponding keys needed to run `GetPosts.py`, which surprisingly, gets posts using python.

- Go onto the [Reddit Apps Page](https://www.reddit.com/login/?dest=https%3A%2F%2Fwww.reddit.com%2Fprefs%2Fapps%2F)
- Select "Create Another App" at the bottom of the page
- Create a fun and quirky name for the app to hide the pain that you will be feeling from using this code and run away from the feelings of grief and guilt you will be experiencing knowing that you are making the internet a worse place overall due to your hubris of wanting to get a few measly likes on a social media site
- Select `script` and put `http://localhost:8080` as the redirect url and finally `create`.

Wowie! You now have a Reddit App! You should feel fulfilled and accomplished in life now! Maybe you should take a break and just, I don't know, forget about this entire project all together now and never come back to it ever again!

No... 

Still here...

shit...

Alright well now that you've done that you need to copy over a few things. The first being the long ass string of characters under the "personal use script" text at the top of your app, this is your `ClientID`. The next is the `ClientSecret` which can be found in the very middle of the app, and finally you'll need `UserID` which will be at the left of the app. This is just your reddit account really, but for some reason you need to specify it when using PRAW, probably for security reasons but who really cares about that.

The final step for this part is plugging these new wacky and fun variables into the `GetPosts.py` file, specifically replacing `Secrets.ClientID`, `Secrets.ClientSecret`, and `Secrets.User` on lines 7, 8, and 9 respectfully with their appropriate keys. After this all you have to do is type what Subreddits you want to steal fro- I mean respectfully borrow from in the final line of the script (line 29 for the uninitiated). I have it default set to just r/AmITheAsshole cause let's be real, half of these videos just pull from there anyways. If you want to add more, all you'd have to do it replace it with something like this : `GetDatShit(["AmItheAsshole", "DnD", "yiff", "YouGetTheIdeaWhyAreYouStillReadingThroughAllOfThis])`. You can add as many or as little as you'd like.

A little note here, I do not have it set up to support images that may be added into the posts the code is taking from. While it probably wouldn't be that hard to impliment, I could not be bothered to work on this shithole of a project any more, so if you want to add something like that, feel free to go ahead.

## Part 2: Generate That Slop BAYBEEEEEEEEEEEEEEEEEEEEEEEEEEEEE
Are you tired of all this setup yet? Well I sure hope not because there's still a lot more left to do!

As much as I would've loved to, I have removed all of the footage I personally used for my experiment in this code (mainly because the file sizes were to big and Github was throwing a fit), but don't worry! It's not that much to do

## Part 2.5: oh shit more setup
There's two things you're going to have to create for this code to work, that being `background footage` to put behind the text being displayed (subway surfers, minecraft parkour, stuff like that) and the next being a little animated character to put in front of your footage to give it a bit more depth and personalize the experience a bit more so that viewers can recognize your brand a bit easier I am completely fucking with you it's to keep that retention up.

I recommend both of these be at least 3 minutes long since that's the max length I've allowed the code to generate videos to (and the max length of a youtube short), though you can change this by simply changing `line 99` in `GenerateSlop.py` to the max length you want.

You can also change the names of these in the code, with the background clip being found at `line 92`, and the character one being found at `line 101`. Yes the reference name for the character in the code is "Jesus", and I will not elaborate on this.

Once you have the video files for each of these created and have the names set properly in the code, all you need to do is put those video files in the `Footage` folder. Here you will also find the `Music` folder where you can add any background music you may want. (Note I recommend longer songs so that they don't get cut off half way through the video.)

## Part 3: Oh It's Actually Time To Generate Now
Congrats on making it through that hell of a setup! You've finally got the code in a working fashion so that way you can actually generate the videos no one has ever once in the history of ever asked for!

The final step for generating these videos is to specify how many you'd want to make in the for loop found on `line 72`, and specify on `lines 201-206` if you would like to run multiple instances of this or not (just uncomment the code found there.

Finally, in the terminal simply run `python GenerateSlop.py`, and let the sloppage begin! You will find the outputted files in the `Output` folder! If for some reason it doesn't work, please do not come to me asking for any help on it I cannot state enough how little I actually care about this project.

# Licence
This project in under an MIT Licence, meaning you can do literally whatever the fuck you want with it, I could not care in the slightest. All that I do ask for is if you make a fork of this code or use it in a YouTube video of some sort that you give credit in some way, specifically linking [My YouTube Channel](https://www.youtube.com/@BorderDestroyer) would be great.
