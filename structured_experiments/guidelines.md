# Guidlines for Datascience and Machine learning experimentation
The purpose of this document is to elaborate on a sctructured experimental technique which utilizes the scitific method 
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
<br><br><br><br><br><br><br><br><br><br>
<br><br><br><br><br><br><br><br><br><br>
<br><br><br><br><br><br><br><br><br><br>
<br><br><br><br><br><br><br><br>
</td>

<td>

#### The Scientific method - explanation - for ds/ml/python notebooks
1) Question
   1) be specific
2) Research topic area
   1) spend at least 1 hour researching for each 2 hours you <br>
      anticipate that creating and executing the experiments <br>
      will take
3) Hypotheses
   1) State your reasoning and your assumption in no uncertain<br>
      terms. Be very specific.
   2) Each hypothesis should be in its own notebook
      1) Use clear filenames
      2) can have many experiments per hypothesis
4) Create and document testing environment:
   1) Because computer sciences have their own requirements <br>
    this step is necessary in order to help gauntee reporduce-<br>
    ability.
      1) Provide with your code a breakdown of your python <br>
      modules ie requirements.txt
      2) Because of the nature of random initialization of the<br>
         initial weights of NN based models it is HIGHLY <br>
         recommended to initialize all of your layer weights to<br>
         a constant.
         1) Instead you may wish to run the experiments some number<br>
            of times and provide a score distribution.
   2) standardize the structure of the notebook to be used in each<br>
      experiment, which experiments will be ran in each, and what <br>
      analysis will be conducted on the results for each experiment
   3) Code up each of your experiments, finalize each notebook, <br>
      after this point the number of changes to the notebook should<br>
      be **very small**.
5) Test with experiment:
   1) Execute the actuall experiment
      1) do whatever model fitting or training<br>
         **1) Do not change parameters and re-run the model!**
         1) Run each experiment once do not overwrite any results
6) Analyze data
   1) For each experiment in each notebook analyze the data and<br>
      state what that data means in context of your hypothesis <br>
      for the notebook
7) Report conclusions
   1) This should take the form of whatever it is that your<br>
      stakeholder will find most useful. Use the graphs and <br>
      figures from your hypothesis notebooks.
</td>
<td>

#### Example - classification problem
1) Question: Can any of the models at our disposal<br> 
   predict if the picture is a cat or a dog with 95%<br>
   accuracy or better?
2) Research topic area: <br>
   - notice that there are many models that can do this
3) hypotheses: (**_be more specific than these_**)
   1) "Because in our specific case we are only<br>
      worried about a narrow subet of all dogs and all cats<br>
      that we can use an even more simple model with ..."
   2) "Because of this our model will train faster by 50% and.."
   3) "Because of this we can use a decision tree with..."
4) Create and document testing environment:
   1) each of the notebooks will follow this format:
      1) description of operating system, processor, gpu acceleration
      2) !pip list
      3) Markdown cell with Hypothesis
         1) explanation of hypothesis and how it relates to the core<br>
            question
      4) A summary of the experiments to be performed
      5) Experimental sections each including
         1) explanation of methodology
         2) code cells to execute the experiment.
         3) analysis and statement regarding what the results mean<br>
            in context of the primary question
      6) Section summarizing the results and conclusions for the <br>
         entire hypothesis
   2) Create the notebooks with this format, if other requirements<br>
      are found update this document and make the changes
5) Execute the code cells in the notebooks that will run the <br>
   experiments.
   1) On some sort of execution error correct the error and run again
      1) optionally document what was changed
   2) provide execution length in time
6) Go into each notebook with completed experiments and fill out the<br>
   section regarding the results
7) Create a presentation to show the stakeholders using graphs and<br>
   charts from experiments.
<br><br><br><br><br><br><br>
 
   

</td>

</tr>

</table>