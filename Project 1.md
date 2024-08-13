# Project 1
*Original Creator: Joseph Earl*


## Description
This is the first of many project apps built to help me grow and practice my coding knowledge and experience. While that was the base goal, my goal for this app is to provide a tool for:

* Memorizing
* Managing files and items to be memorized
* Testing user knowledge(via randomized quizes, asking for title when given a portion of data, etc,.)
* Analyzing and tracking data on what has been memorized and at what pace

During development and testing I will be using the LDS Standard Works for content. Should interest in this project grow or it ever become commercially used I will seek a license for this content or remove it.

The primary coding language used will be python, the GUI will be made using the PYQT6 library and the database will be built using MySQL(though I will probably switch to SQLlite).

## Ver. 1.0

### Functionalities & Features

* Dashboard
    * This will be where the user can decide between doing a test at the "Testing Station, memorize a file or manage the "Learning Queue" of files to memorize, browsing the directory of files & adding to the queue. There will also be a settings tab.
    <br><br>

* Testing Station Options
    * Long Term
        * Asking Users to recall things that they have memorized in the past few months and years
    * Short Term
        * Asking Users to state or recall things they have learned in the past week or two
    * Ask Users to state the title or label of a file based on a portion of the file.
<br><br>

* Learning Queue Options
    * Learning(or really memorizing) any content will begin with the user typing in the content repeatedly based on how many times they have specified in the settings. Once they have completed that task they may "Test" it by typing in the content correctly without looking at the answer. they the amount of times specified in the settings and once completed, the file moves from the learning queue to the Testing Station
    * "Start Learning!"
        * This option will have the user learn files in the order added  the queue
    * Select File
        * This option will have the user start learning the content they have selected
<br><br>

* Directory/File Management System(FMS)
    * Files
    * Folders
    <br><br>

* Custom Style Sheets(CSS)
    * Will add more to this when I start working on it, right now I just know that I want the app to look good and not stupid
<br><br>

* Settings
    * Dark Mode/Light Mode
    * Attempts to learn
    * attempts to test


### Development Timeline

The current goal is to complete version 1.0 before Jan. 1st, 2025. In order complete this, work will follow this timelime. The last week of each month will primarily be spent on refactoring and testing code.

* Aug
    * Database Built(using LDS Standard works)
    * Directory/FMS built.
    * Dashboard Layout
    * Learning Queue Started

* Sept
    * Begin CSS Implementation
    * Learning Queue Finished
    * Testing Station Started
* Oct
    * Testing Station Finished
* Nov
    * CSS Finalized
    * Settings Completed
* Dec
    * Compiling



## Future Versions
Depending on the interest in this project, I would like to build out future versions with features like:

* Dynamic Files
    * For version 1.0, each file will have a title and a content portion. I would like to build it out to have dynamic file types, meaning that each file type could have multiple attributes. For Example, the periodic table wouldn't fit well into our title/content system as there are multiple peices of content to support. 
* Smart Import and Export
    * This would provide a tool that would analyze a file and return a set or directory of files that would be added to the database with the user having to do the most minimal amount possible
* User Stats
    * I want users to be able to see their stats. For example if they are trying to memorize scriptures or anatomical terms, I want them to be able to see and share their progress. I would also be interested in possibly gathering the users in app stats/data(and really just that).
* File sharing
    * users can share or get folders from other users. for example, if someone has a set of all the anatomical terms needed to be memorized for a class, they can share that file in house with other users.