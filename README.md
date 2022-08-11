# Crawler Script

This script counts the occurences of the most common words in the "History" section of the Microsoft Wikipedia. That page can be found here: 
[Microsoft Wikipedia](https://en.wikipedia.org/wiki/Microsoft#History)

## How It Works
This script uses Beautiful Soup to return all of the text on the Microsoft Wiki. 

The Wiki text is formatted, and then the script selects the "History" substring from that text.

The "History" text is stored in a counter which counts the number of occurences of each word. Any words to be excluded are removed from the coutner. Then the top n (default is 10) most common words are stored in a dictionary, printed out to the Terminal, and returned. 

## Setup

1) Create a [virtualenv](https://virtualenvwrapper.readthedocs.io/en/latest/command_ref.html) for this directory and install the necessary dependencies. 
    - `cd [path_to_crawler_script_directory]`
    - `make virtualenv crawler` 
    - `workon crawler`
    - `python3 -m pip install -r src/requirements.txt`

*NOTE: If you do not have virtualenv installed, you can install it with this command: `python3 -m pip install virtualenv`. The `make virtualenv` command should automatically activate your virtual environment, but if it does not, you can do so with this command: `workon crawler`.*

2) Make sure your python interpreter is pointing to the correct directory, for me this was ~/.virtualenvs/crawler/bin/python. You can set this either using your IDE or the CLI. If you get an error about imports not being found, it's because you still need to do this step. 

3) You can pass two optional arguments to `main()`:`num_words_to_return`(int, defaults to 10), `words_to_exclude`(list, defaults to None). If you do not care about passing any arguments and are okay with the defaults, you can run: `python3 src/crawler.py`. If you want to pass arguments, instead follow steps 4 & 5. 

4) From your virtual env bring up your python interpreter: `python3`.

5) Import the `main()` function and run the script: 
    ```
    from src.crawler import main
    main([args])
    ```

## Problem Solving Approach

When I first read this problem *(see CrawlerCodingChallenge.txt)*, I assumed I would be using [Selenium Webdriver](https://www.selenium.dev/documentation/webdriver/) to solve it. I anticipated a basic html structure like this for the wiki: 

```
<html>
    <body>
        <title id="microsoft-title">
        <div id="introduction">
            <h1>Microsoft</h1>
            <p>blurb</p>
        </div>
        <div id="first-section" class="article-section">
            <h2 class="section-header">First Section</h2>
            <p>paragraph1</p>
            <p>paragraph2</p>
            <p>paragraph3</p>
        </div>
        <div id="history-section" class="article-section">
            <h2 class="section-header">History</h2>
            <p>paragraph1</p>
            <p>paragraph2</p>
            <p>paragraph3</p>
        </div>
        <div id="third-section" class="article-section">
            <h2 class="section-header">Third section</h2>
            <p>paragraph1</p>
            <p>paragraph2</p>
            <p>paragraph3</p>
        </div>
    </body>
</html>
```
No big deal, find the css selectors I need, select the necessary elements, get their text, process the words in the text. However, what I instead found was (more or less) this:

```
<html>
    <body>
        <div id="bodyContent">
            <p>paragraph1</p>
            <p>paragraph2</p>
            <p>paragraph3</p>
            <p>paragraph4</p>
            <h2>Section Title</h2>
            <p>paragraph5</p>
            <p>paragraph6</p>
            <p>paragraph7</p>
            <h2>History</h2>
            <p>paragraph8</p>
            <p>paragraph9</p>
            <p>paragraph10</p>
            <h2>Another Section</h2>
            <p>paragraph11</p>
            <p>paragraph12</p>
            <p>paragraph13</p>
        </div>
    </body>
</html>
```

The lack of css selectors and lack of anticipated element nesting makes selecting elements much harder, whether I use css selectors, or tag names, or xml path. I could have selected all the `<h2>` and `<p>` elements (along with a couple `<span>` and `<a>` elements), but there would be a lot of them, and I'd need to loop over them to select the ones I want and disregard the others. This seemed like it would involve more lines of code than necessary, so I opted for a different solution.

[Beautiful Soup](https://www.crummy.com/software/BeautifulSoup/) seems better suited to this task. With Beautiful Soup I can quickly extract all the text from the wiki as one long string and then manipulate that string with a lot of regex to get the "history" words. 

## Remaining Questions

1) Is the example of the expected result given in the instructions *(see CrawlerCodingChallenge.txt)* supposed to contain correct answers for the words it shows? I do not get the same numbers, and if I copy/paste the "History" section into a [word document](https://docs.google.com/document/d/1-atX6Gz8R2UqYod9On-XoOZTWu_gmOrq3o1DOi8dcvE/edit?usp=sharing), but I still don't get those numbers. (However I did "test" my answers that way, and was able to verify I am returning the word counts I expect to return). Perhaps the wiki has been updated since this coding challenge was first written. 

2) How should hyphens be handled? The following words all appear in the "History" text: "Microsoft", "Micro-soft", "non-Microsoft". I replaced hyphens with empty strings, meaning those three words turn into two words: "microsoft", "microsoft" (same word), and "nonmicrosoft". The same problem exist with "IBM" and "non-IBM". Is this the correct approach? If not, why?

3) How should forward slashes be handled? Consider the words: "CP/M" and "X/S". The acronym "CP/M" stands for "Control Program for Microcomputers" and "X/S" is a particular Xbox series. Does it make more sense to replace the forward slashes with empty strings or spaces? I replaced them with empty string. If this is not the correct approach, what approach would be better and why?

4) This challenge did not specifically ask for tests. I "cheated" by using a [word document](https://docs.google.com/document/d/1-atX6Gz8R2UqYod9On-XoOZTWu_gmOrq3o1DOi8dcvE/edit?usp=sharing) which contains the "History" section of the wiki to manually test my code. (I.e. use the python debugger to print out all of the word counts, and then use the find feature in Google docs to search for each word and verify that the word count I return matches the number of times that word appears in the document.) I tested that I return the expected number of words and exclude excluded words by passing arguments to the main() function and examining what prints out. 

5) This script could stand to be optimized for time complexity. get_history_words() takes a brute force approach to formatting the wiki_text and has terrible time complexity. There are too many loops. Those replacement tuples could probably be combined some, and if I found the history_text before making the character replacements, then the length of the string I'm formatting would be shorter, which would make each re.sub() call faster. This isn't super noticable with the current length of the "History" section of the wiki but would be noticeable if scraping a webpage with a larger amount of text. 