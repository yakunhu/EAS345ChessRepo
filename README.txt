Welcome to the repo for the Chess Positional Evaluator project. This repo contains all the code required to clean the input data the LiChess evaluation database, building a dataframe from the JSON file, wrangle the resulting data into a dataframe with 7 positional factors and the centipawn evaluation of each position, and build machine learning models on the data using Random Forest, XGBoost, and Logistic Regression in the R programming language.  

The filtered_lichess folder contains the data files of the project. 

Step 1: Download the LiChess evaluation database from https://database.lichess.org/#evals
Step 2: Run the following command in a Linux terminal after navigating to the directory that contains the downloaded database: zstdcat lichess_db_eval.jsonl.zst | head -n 1000000 >
a_milli_positions.jsonl. Move the output file into the filtered_lichess data folder. Note that the database is updated frequently, so your file may be different from the one we used. 
Step 3: Run the script jsonl_to_fen.py, which cleans the .jsonl file, filters a million positions down to 85000 based on the parameters specified in our report, and converts the format to a csv for downstream analysis. The output file is "eval_db_filtered.csv" in the filtered_lichess folder.
Step 4: Run matrix_convert.py, which, along with a helper script for each positional factor we define in the report, wrangles the "eval_db_filtered.csv" and creates a column with a numeric value for each factor and outputs to "eval_db_processed.csv" in the filtered_lichess folder. 
Step 5: Run eda.py, which processes eval_db_processed.csv and performs exploratory data analysis. 
Step 6: Use the script split_train_validate.py to a) divide the 85000 rows into a training set and a validation set and b) do this 5 times with different segments belonging to the validation set. Note that line 34 and lines 4 and 5 have to be manipulated manually; divide the total rows in eval_db_processed.csv by 5 and compute the segment start and end points. The output will be 5 pairs of train and validate files. 

For steps 7-9, navigate into R_models:

Step 7: Run models_comp.R, which compares XGBoost, Random Forest, and logistic regression models on our data. 
Step 8: Run the logistic regression model glm.R, which outputs performance metrics for the full model as well as models with each factor dropped. 
Step 9: Run k_cross.R, which performs k-fold cross validation and generates averaged metrics across  folds. 
