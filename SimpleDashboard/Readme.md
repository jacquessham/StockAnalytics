# Dashboard Refactoring

Jacques' original project is a cool stock charting app which works. It's just a nice project for me to build on as I learn Plotly Dash. There are a number of things about the project which I want to "improve on" just for fun, not because there's really anything wrong with the original. And working through this list will help me learn Plotly Dash.

Also, I am forcing myself to take a planned approach to refactoring to learn this as a skill. Typically, I just start ripping into everything as I see it. But when something breaks, it can be a nightmare to get it back together. 

Check out Jacques' [Original ReadMe](./Readme_original.md)

### Refactoring 

The second tab on this dashboard is unnecessary since the index can be overlayed on the same chart as the stock. Therefore, I will not be testing the second tab while attempting these refactoring tasks.

1. **~~Setup to work on docker~~** Done!

~~I tend to do everything in docker now because it makes life easier down the track. And ultimately I will need to learn to deploy Plotly Dash apps. So this is just a quick change that doesn't really fix anything. I will also add Jupyter Notebooks for testing code changes on the same setup.~~

Todo: 
- Configuration currently assuming development environment. At some point I will update this to depend on environment variables.

2. **~~Reduce API calls~~** Done!

~~The original design uses the yfinance Python API to get stock history and stock info. However, this API is called multiple times for different purposes in a single render (i.e. validating that it exists, getting the data, and for calculating moving averages). This process also happens every time you change the chart date range for the same stock. The result is a bit of an annoying delay when playing with the charts.~~

~~There only needs to be one call to the API for max history and filtering can be done within the app. Also, in the future I could see a preference to caching API results in the case of switching between stocks, or a local database which is kept updated via a separate process.~~

~~My solution to these problems which will not break the dashboard is to create my own mini API (Python class) to sit between the functional code and the API. This will facilitate a sort of caching and simplify the code to some extent.~~

~~What I am not yet sure on is where is the best place to store the data. I am thinking of storing the object as json serialised on the client. But this needs further research if it is performant or not.~~

Notes:
- I learned that all python code in Plotly Dash executes on the server. Therefore there is no point using a browser cache for this. This makes sense, however, it seems to defeat the purpose of building the framework in React.js. In the Plotly Dash docs, there is an ability to create JS modules and front-end callbacks, so I guess there is an escape hatch if something is really non-performant due to unnecessary round-trips.
- Plotly Dash is built on Flask which offers "Flask cache" (separate install). Apart from being simple to use, this is preferred because implementing your own simple cache can have issues with multi-threading and with simultaneous users. It is interesting that Flask cache offers a Redis interface. I would like to investigate this in the future but for simplicity, I have implemented a filesystem cache. 
- Also looking into the yfinance source code, I see an option to cache. However, I think it is better to plug into the Flask cache for the reasons mentioned above.
- The cache is now working really well, the responsiveness is what you would expect when you switch between time periods and when you re-select an already cached stock. 

Todo:
- One issue I encountered was the configuration of the 'FileSystemCache' in Flask, apparently the version of Flask I am using (default on anaconda3 2021.05) is old, so the cache configuration variable must be set to filesystem. I will upgrade at a later stage. 


3. **Move Data Transformations to API class**

I will move all the data transformations to the new data API, as part of simplifying the app callback functions e.g.:
- Moving Averages
- Last price movement
- 52 Week Ranges

4. **Split Callback Functions**

Currently a single callback function triggered by the Input submit is rendering both the table and chart elements on the page.

Again, in the name of simplifying the callbacks to achieve a single objective I will split the callbacks. The benefit of this is when I get to the point of adding more features, separating these will make life easier in the future. 

5. **Move structural styling to CSS**

In the main app structure, there is a lot of styling in the code. I find this a problem mainly because it's harder to see the layout with all those style attributes in there. If I want to modify the layout, I want it to be really simple to read. Also, I think it will be easier to fiddle with style adjustments with CSS. 

Rather than create my own CSS, I will use <a href="http://getskeleton.com/">skeleton responsive boilerplate CSS</a> which includes a CSS reset and a framework for typography, flex grid and general look and feel. This refactoring step will change the appearance of the app. However, it will not change the functionality, and I will ensure that the app is still usable with the style changes. 

6. **Move programmatic style features to CSS**

In a number of situations in the code, style elements are passed back in the callbacks. Again, I find this annoying because it's a bit confusing to read the code. Sometimes the same style elements are always passed back, therefore these should be just removed from the callback.

In other situations, such as the color change for price movements whether they are up or down, these are required to be set in th code. However, I will be annoyingly pure about this and make the function update the element's class, so that the css typography can control the coloring. As well as being annoyingly anal... This does bring benefits, for example to enable the CSS to control the whole look and feel (e.g. if up/down is to be coded as Blue/Red instead of Green/Red for colorblind persons).

7. **Activate flex grid**

I will move the classes for core "widgets" to flex grid containers to activate the resizing functionality that comes with skeleton. 

In some ways, this is not a refactoring step as it adds some new functionality. But nothing is changing in terms of the app features.