
This code was written for a Data Science Categorization competition: https://www.datasciencechallenge.org/challenges/2/growing-instability/

I am very pleased with the outcome, though the results were far from accurate or the leaderboard I appear to have been 57th out of 577. My main objective for this project was to create something that 'worked' and not something that won. I wanted something that would: read JSON training data, analyze training data, create DB of analyzed results, and use training data db to categorize target articles. Additionally, I quickly realized that simply creating this would be meaningless if I couldn't run the categorization on a subset of the training data and test it's accuracy. So, I decided to create something that would do this too. Aside from that, there are a few bits here and there to format and manage data. 

To start: cat.py is intended to open and analyze the training dataset. First, it uses python JSON reader to open, identify, and start scrolling through the training articles. To analyze the articles, the function ‘strip’ does most of the heavy lifting. This program implements a lot of the NLTK natural language tool kit plugin for Python. This cleans up the data, tokenizes, removes stop words and returns histogram of the frequency of popular words. After it does this it adds popular words against the category that the original author assigned to the article. If the word is already on the list for a specific category the program will increment the count for the word/category. 

This is the part of the code where I really would like to throw it all away and redesign this piece. Because this continues to add most popular words for a given category—and popular words for some categories like ‘culture’ or ‘media’ are incredibly varied, I ended up having nearly every word in the English language in these categories at least once. As I was looking at the frequency of words in addition to if a word was on the list it may not have mattered too much, but it caused performance problems and doesn’t help the program. I would like to re-implement this as a ‘heap’. At the point of finishing an article I’d also like to capture more statistics about the article—specifically the number of words in the article and the number of times most popular words appeared in a specific article. This would allow me to better calculate the ‘bag of words’ approach: 

x(i)=TF(i,d)⋅IDF(i) , where TF(i,d) (term frequency) is the number of times term i occurs in document d . IDF(i) =logNni is the Inverse Document Frequency, where N is the total number of documents in a collection, and ni is the number of documents that contain term i .

This code also uses the categories given by the training dataset and not additional categories. This created some problems for my ultimate submission as some of the required categories had no positive results as they were never included in the training data. Additionally, I very quickly had several thousand categories—most of which were not relevant as they were not part of the ultimate target categories. Ideally, I wouldn’t have to create a program that categorizes everything in the entire world just to return articles that correspond to a few categories. However, simply ignoring these categories would force all of the test articles to be positively identified as one of the target categories which would be incorrect. So, I really need an ‘other’ category where all categories not in the target categories could be dumped. Then, when analyzing target data I may be able to ask: does this correspond to a target category, or is it other. This would greatly increase performance as my current test data is run against all categories to find which it might correspond to, then singled out by articles which correspond to the categories. 

Dog.py: this program was initially written to read through the test data and compare it to the training data. However, once I built it I realized I needed to have dog.py’s methods also work to analyze new training data and compare the results against the given categories. This program does both though it should probably only do one or the other, or possibly have a variable set to determine which mode to run in. Currently it’s managed by commenting the ‘other’ code that you don’t want to run, which is probably not industry standard. Strip is the same as in cat.py, so perhaps I should not have copied the code here but I was thinking I would need different versions for the training and test data which proved to not be true. The majority of this program takes place in the check table and the inc table which checks the tokens from a test article against the training db and adds results to the test db. While this works, it’s fairly flawed as it does not take into account the prominence of tokens in a target article and as mentioned before, tests these tokens against all categories. 

Scoop.py analyzes all categories that have been assigned to an article and turns the ‘actual’ to true for the highest categories. 

Send.py looks at the test database after scoup.py has run and generates a DB to submit in the correct format. 


Wrap-up: 

The good: despite terrible performance and the obvious (and many less obvious) flaws mentioned above, this does work. I learned a number of python libraries and functions that I hadn’t used before. I had never worked with a DB, and so a lot of the time was spent learning sqlite creating DB’s and updating them appropriately. 

The bad: The main portion of this I would like to improve is the analysis section. I need to have a better picture of how the data will ultimately be used and work backward from there with respect to extracting and saving the data. A lot of good analysis ideas I had were unimplementable because of the method and organization of the data.  I also want to implement a heap as mentioned above. Additionally I would like to add the number of metrics to the training data. Currently I can only calculate Accuracy and I need to save a number of additional attributes.

I’d also like to analyze the number of categories that are generally suggested for an article. I hardcoded assigning three, but it’s likely that different types of categories or different lengths of articles generally have a different number of categories per article. This is an idea I had, but didn’t end up building. 

I also want to add two items—numbers and places as general attributes for each analysis. This was a good idea to programmatically handle number/places as some categories presumably had more than others and could be used as a method for categorization. 

I also need to address the aforementioned problem that I could only add categories that were formerly known. I’m not sure how I would go about sorting that out, but it should be done to allow target categories that are not part of the training dataset. 

I’d like to increase the performance by cleaning up my usage of NLTK libraries and ensuring that I don’t create unnecessary data in the program, which I do now.

It would be advantageous to build the input/output as part of a stand alone program so that I could enter a few parameters and run the program and return analytics. This would be ideal as I could then tinker with the matching code in the middle without having to rewrite the input/output programs each time I have a new idea to improve the program

I’d also like to research and implement Support Vector Machines (SVM), rather than my crude method of comparing and generating a percentage of likelihood of each category for an article. 

The sql is terrible. Don’t look at it. I was learning how to do it and have since learned using python to create strings is pretty shitty and I found out why each step of the way, but now I’m too indifferent to go back and rewrite this. 

There are a thousand things I’d like to do now to improve this, but the code is too jumbled and the competition is over so I’ll just tuck this away as a learning experience and move forward with some other projects.  

