# Guidelines for Data Science and Machine learning experimentation
The purpose of this document is to elaborate on a structured experimental technique which utilizes the scientific method 
<table>
<tr>
<td>

#### The Scientific method
1) Observation / question
2) Research topic area
3) Hypothesis
4) Test with experiment
5) Analyze data
6) Report conclusions


#### The Scientific method - explanation - for ds/ml/python notebooks
1) Question
   1) Be specific
2) Research topic area
   1) Spend at least 1 hour researching for each 2 hours you anticipate that creating 
   and executing the experiments will take
3) Hypotheses
   1) State your reasoning and your assumption in no uncertain terms. Be very specific.
   2) Each hypothesis should be in its own notebook
      1) Use clear filenames
      2) can have many experiments per hypothesis
4) Create and document testing environment:
   1) Because computer sciences have their own requirements this step is necessary in order to help guarantee 
   reproduce-ability
      1) Provide with your code a breakdown of your python modules ie requirements.txt
      2) Because of the nature of random initialization of the initial weights of NN based models it is 
      HIGHLY recommended that you initialize all of your layer weights to a constant
         1) Instead, you may wish to run the experiments some number of times and provide a score distribution.
   2) Standardize the structure of the notebook to be used in each experiment, which experiments will be ran in each, 
   and what analysis will be conducted on the results for each experiment
   3) Code up each of your experiments, finalize each notebook, after this point the number of changes to the notebook 
   should be **very small**.
5) Test with experiment:
   1) Execute the actual experiment
      1) Do whatever model fitting or training
         **1) Do not change parameters and re-run the model!**
         1) Run each experiment once - do not overwrite any results
6) Analyze data
   1) For each experiment in each notebook analyze the data and state what that data means in context of your hypothesis 
   for the notebook
7) Report conclusions
   1) This should take the form of whatever it is that your stakeholder will find most useful. Use the graphs and 
   figures from your hypothesis notebooks.
</td>
<td>

#### Example - classification problem
1) Question: Can any of the models at our disposal predict if the picture is a cat or a dog with 95% accuracy or better?
2) Research topic area: 
   - notice that there are many models that can do this
3) Hypotheses: (**_be more specific than these_**)
   1) "Because in our specific case we are only worried about a narrow subject of all dogs and all cats that we can use 
   an even more simple model with ..."
   2) "Because of this our model will train faster by 50% and.."
   3) "Because of this we can use a decision tree with..."
4) Create and document testing environment:
   1) Each of the notebooks will follow this format:
      1) Description of operating system, processor, gpu acceleration
      2) !pip list
      3) Markdown cell with hypothesis
         1) Explanation of hypothesis and how it relates to the core question
      4) A summary of the experiments to be performed
      5) Experimental sections each including
         1) Explanation of methodology
         2) Code cells to execute the experiment.
         3) Analysis and statement regarding what the results mean in context of the primary question
      6) Section summarizing the results and conclusions for the entire hypothesis
   2) Create the notebooks with this format, if other requirements are found update this document and make the changes
5) Execute the code cells in the notebooks that will run the experiments.
   1) On some sort of execution error, correct the error and run again
      1) Optionally document what was changed
   2) Provide execution length in time
6) Go into each notebook with completed experiments and fill out the section regarding the results
7) Create a presentation to show the stakeholders using graphs and charts from experiments.
<br><br><br><br><br><br><br>
 
   

</td>

</tr>

</table>

## Reproducible results
Exact reproducible results can be a hard thing to achieve in tensorflow / keras.  
Please see [does_synthetic_data_improve_mae.ipynb]
(./data_training_pipeline_experiments/story_photo_transformer_experiments/does_synthetic_data_improve_mae.ipynb)
for how to set up a model and fit to be reproducible.