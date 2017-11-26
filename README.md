# Visualizing Shakespeare

Shakespeare’s works have been performed and analyzed for centuries, yet truly understanding the text often requires extensive manual data collection - from character relationships to prevalent themes to inter-play connections. Our project allows users to easily visualize the structural properties of Shakespeare’s plays, such that anyone from an actor to a director can enrich their interpretations of the text. Automated data collection provides us with more data to make the visualizations more detailed and accurate.

## Authors
Anthony Romm, Srinidhi Srinivasan, Alex Trudeau, Jane Wu

## Run Time Components
Our website uses the following components:
- HTML
- CSS
- AngularJS 1 as an MVC framework
- Javascript
- D3 for visualizations

## Data Storage/File Structure

## Python Scripts/XML
Our visualizations are created by parsing Shakespeare's texts. Specifically, we use Python scripts and Shakespeare plays in XML format, found [here](https://www.ibiblio.org/xml/examples/shakespeare/), to create the backend data for our various visualizations. These can be represented in `JSON`, `CSV`, or `TSV` files depending on the needs of the specific visualization.

##

## Running Server

To develop with our website, you should first clone the repository and then you must run a simple Python server with the following command:
```
$ python -m SimpleHTTPServer
```

