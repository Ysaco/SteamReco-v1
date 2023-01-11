# Welcome to SteamReco v1

This is a beta of a project based on a Steam Webscraper I made myself without selenium, its pure python and it gets all the 70k+ games on the steam store for recommendation.

In this case we are only using 19618 games after doing some data cleaning which its around 30% of the pure useful data. The reason behind is so any pc with 16gb ram can run it without any trouble. If you have less than 8gb or around it, please refrain from running this code, since it can freeze your whole pc.

If you have any questions please feel free to dm me at ysaco7@gmail.com

Soon Ill be uploading a video with all the explanation, top process, how I made the webscraper and how does it work.

For testing please be mindful that you need to change the variables "game list" and "img" paths.
This app may be to heavy to run in streamlit itself, so sooner than later ill be moving all this app to django. The reason I havent done that is that I dont have a server for hosting the project.