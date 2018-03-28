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
  <img width="450" height="300" src="https://user-images.githubusercontent.com/20330371/38013194-e569c548-3281-11e8-8c63-121e7e542d6e.PNG">
</p>


#### Traffic Distribution:
In this visualization we display the hourly vehicle count distribution as a bar chart with an overlaid Line plot. The particular hours in the night where Street Lights can be dimmed are also marked in this plot as <font color='#ea2539'>RED</font> and <font color='#48ad1d'>GREEN</font> dots.

<p align="center">    
  <img width="500" height="300" src="https://user-images.githubusercontent.com/20330371/38008688-a7d239d6-326d-11e8-9ced-a297e0543b6c.PNG">
</p>

#### Energy Savings:
In this visualization we display the energy savings for one weekday and one weekend where Street Lights are Dimmed during certain hours compared to a Normal Scenario where street lights function at FULL Brightness during the entire night.

<p align="center">
  <img width="500" height="300" src="https://user-images.githubusercontent.com/20330371/38008759-14e7798c-326e-11e8-9b3a-0221b7850488.PNG">
</p>

* A video of all these visualizations working in a standalone browser window can be found [here](https://youtu.be/7pv4N06TfDE).