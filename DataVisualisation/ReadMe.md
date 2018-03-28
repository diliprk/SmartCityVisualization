### Data Visualization:
[Bokeh](https://bokeh.pydata.org/en/latest/) was used  extensively to build all the visualizations for this project. It is recommended to have [Anaconda installed](https://conda.io/docs/user-guide/install/index.html) to load the jupyter notebook and other python scripts in this folder. Thereafter,
1. Open *Anaconda Prompt* or Terminal.
2. Install the required packages using `conda install bokeh pandas` directly into the root (or base) environment or in your [custom environment](https://conda.io/docs/user-guide/getting-started.html#managing-environments). 
3. Change the Directory to the folder where you have downloaded this repository and then launch Jupyter Notebook by typing `jupyter notebook`. After that you can open the `Traffic&EnergySavings.ipynb` in your Internet Browser.

All the visualizations that are in the jupyter notebook has also been made available as standalone external visualizations by calling the python script in a bokeh serve application (Example `bokeh serve --show MapViz.py`) in Anaconda Prompt. As before you have to navigate to the correct folder and activate your custom or root conda environment where the required packages are installed.


The following are the visualizations built for this project using Bokeh:

#### Map Based Visualization:
In this visualization we display the hourly vehicle count of a particular street on a map.

<p align="center">
  <img width="300" height="300" src="https://user-images.githubusercontent.com/20330371/37703368-76f6010a-2d1b-11e8-87da-8a3cc0feccc9.jpg">
</p>


#### Traffic Distribution:
In this visualization we display the hourly vehicle count distribution as a bar chart with an overlaid Line plot. The particular hours in the night where Street Lights can be dimmed are also marked in this plot as RED and GREEN dots.

<p align="center">
  <img width="300" height="300" src="https://user-images.githubusercontent.com/20330371/37703368-76f6010a-2d1b-11e8-87da-8a3cc0feccc9.jpg">
</p>

#### Energy Savings:
In this visualization we display the energy savings for one weekday and one weekend where Street Lights are Dimmed during certain hours compared to a Normal Scenario where street lights function at FULL Brightness during the entire night.

<p align="center">
  <img width="300" height="300" src="https://user-images.githubusercontent.com/20330371/37703368-76f6010a-2d1b-11e8-87da-8a3cc0feccc9.jpg">
</p>

* A video of all these visualizations working in a standalone browser window can be found [here](https://www.dropbox.com/s/9b4yx1137x2kzsx/BokehMapViz.mp4?dl=0).