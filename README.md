# Stacked-bar-chart-visualizer
## UW-Madison 2021 Fall CS765 Data Visualization
## Course Final Project - Design Challenge 2
### [Yuchen Zeng](https://github.com/yzeng58), [Lihe Liu](https://github.com/liulihe954)

### 1. Motivation and Goal
Stacked bar graphs (SBG) can be used to visualize the quantitative relationship that exists between a main category and its subcategories. Each bar represents a primary category and will be divided into different section that represents the subcategories for a second categorical variable. 

However, there are many challenges in automatically resizing SBG. The change of the size and/or the aspect ratio of plotting frame will make the content too compact/skewed, and/or obscure the underlying relationship. Such limitation will create perceptional challenge and affect the visualization effectiveness. 

The goal of this project is to develop a web app that visualizes the input dataset as a stacked bar chart in the required figure size.

### 2. About this Tool

#### 2.1 Description

Our main contribution to this project will be:

    * developing an efficient algorithm which automatically adapts a stacked bar chart to a smaller size;
    * building a small program which takes a dataset, required figure size, two categorical variables and one numerical positive variable as input, and output a stacked bar chart in the required figure size;
    * embedding the resizing algorithm into the program and building a user-friendly web app that can automatically generate customized stacked bar charts.

#### 2.2 Implementation
To run our application, please first download this repository.

Then run `python app.py`.

Then access http://127.0.0.1:1234/ using your web browser.

#### 2.3 Demo



### 3. Application Framework
This tool is developed using [Dash apps](https://plotly.com/dash/)



