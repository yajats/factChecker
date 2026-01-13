###Verify AI

This website can analyze the validity of news, including mp4 links, YouTube videos, and text from articles. It will provide a brief summary and check for any bias or wrong information.

* Make sure to change cookies to your own youtube cookies

## Inspiration
As the current political climate grows more extreme and more fake news continues to flood the Internet, it is becoming increasingly more important to verify that the information available on the Internet is reliable and unbiased. This need to filter out the large amount of fake news present today is what led us to building Verify AI.

## What it does
VerifyAI is a website that can take either video or text based news and checks for any flags that may indicate false claims or bias, including overly assertive statements or highly emotional language. It additionally checks for sources to back up possible claims, and using Twelvelab's Pegasus model, the site provides an AI generated summary describing any potential bias from the article.

## How we built it
The backend was developed in Python and makes use of Twelvelabs to analyze video content in the form of YouTube links or direct mp4 uploads, while text-based articles use a system that checks for flags that indicate any potential bias or misinformation. The frontend was developed using HTML and CSS, with Flask being used to set up a framework that connects the two.

## Challenges we ran into
Getting the script to call the Twelvelabs API was challenging at first, and it took lots of time reading through the documentation and trying various things to get it to work. There was also some trouble integrating the frontend and backend, since different team members were working on each part.

## Accomplishments that we're proud of
As this is our first time building in a hackathon, we are very proud of the fact that we were able to build a fully working website in just a day, especially since we had very little experience in this area of computer science and software engineering beforehand.

## What we learned
 We learned a lot about the process of building a full stack application and how the workflow of such a project is managed. Verify AI also taught us more about multimodal LLMs such as Twelvelabs, and how they can be used in different ways compared to more traditional models. 

## What's next for Verify AI
There are still lots of improvements that can be made to the website, including the ability to include various kinds of text-based articles, such as websites or social media posts, as well as a more expansive analysis that can refute claims by providing additional sources and information.
