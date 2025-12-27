import praw
import pandas as pd
import Secrets

def GetDatShit(subreddit_list):
    reddit_shithole = praw.Reddit(
        client_id = Secrets.ClientID,
        client_secret = Secrets.ClientSecret,
        user_agent = Secrets.User
    )
    
    for subreddit_name in subreddit_list:
        subreddit = reddit_shithole.subreddit(subreddit_name)
        
        posts = []
        for post in subreddit.top(limit=20):
            posts.append([post.title, post.author, post.selftext])
        dataframe = pd.DataFrame(posts, columns=["Title", "Author", "Body"])
        dataframe.to_csv(f"{subreddit_name}_top.csv", index=False)
        
        posts = []
        for post in subreddit.hot(limit=20):
            posts.append([post.title, post.author, post.selftext])
        dataframe = pd.DataFrame(posts, columns=["Title", "Author", "Body"])
        dataframe.to_csv(f"{subreddit_name}_hot.csv", index=False)
        
        print("One small step for reddit karma, one large step for AI kind")

GetDatShit(["AmItheAsshole"])