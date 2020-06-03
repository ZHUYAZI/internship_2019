# internship_2019
Analyse transport in paris

All the code is written on python developed by Jupyter notebook
There are three parts in the code
First part developed on windows, the file is named by the content and the order of creation. It’s for the read, analyze, visualize the data AFC, GTFS.

•	Read data and separate by day:
	read_in_database_enpc_donnees_1.ipynb
	
read_in_database 1.ipynb

•	Analyses statistic
2019_2_11 traitement 2.ipynb
2019_2_11 traitement 3.ipynb

•	Build model 
GTFS_feed_to_route_8.ipynb
Best_Plan_8.ipynb
BESTPLAN.py

•	Visualization
All rest files

Second part developed on Linux, which is for build the intramodality model as we need multi processes to treat the data faster

•	test_multi_processing_linux.ipynb
 and then we use the result to do machine learning.
 
•	Xgboost

•	SVM

•	Neural network

finally, we predict on the data EGT if the voyageur possible use the car.

Third part is do study on the EGT, and doing some work to complete. Like show OD-trip of EGT, classify EGT car users based on our prediction.
