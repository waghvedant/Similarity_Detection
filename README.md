# Similarity_Detection
Here I have created an algorithm for detecting the similarity of your documents with the others documents in the dataset. Two algorithm I have used 
1. Cosine Similarity for word detection
2. Latent Symantic analyis for meaning matching.

Herewith I have created modules:
1) preprocessing : It is for preprocessing the files and main algorithm will work on raw data content
2) BagOfWords : Here is counting the words in the document in order to find out content matching from each document
3) Term Frequency and Inverse Document Frequency : Here it calculte the terms occurence in the document based on formula.
4) Document Calculator: Here it calculate the vector multiplication of TF and IDF
5) Cosine : Actual similarity is checked here having an algorithm which works on processed documents result is on words content.
6)LSA :  Actual similarity is checked here having an algorithm which works on processed documents result is on meanning of document

First 3 modules work individually on every modules and next 3 modules work integrally when all the files are uploading for checking similarity.
