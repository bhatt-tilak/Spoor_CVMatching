##############################################################
DO GOOGLE SEARCH AND LEARN HOW EACH THING MARKED WITHIN <>  DOES
<> QUESTIONS ARE FOR SURE ASKED BY THE EXTERNAL EXAMINER
the following 4 parts are absolutely esential and you need to learn about them
go through all these instructions and learn about the theories involved with great care by wednesday
At 8:40, afte greenlight from verma sir, i will show you guys how to run the demo and project
be ready
#################################################################



This is the main folder
manage.py contains all the handellers of the project
spoor is the project
UI is an application of project spoor




###DATA
Firstly data , i.e. resumes are required.
we extract text from resumes
we remove unnecessary words
we tag required word as Experience, Skill and Education
we create a csv
we split csv in 90:10 split ratio for training and testing respectively
<Stanford NER tagger>
<custom ner entity>
<https://dataturks.com/projects/abhishek.narayanan/Entity%20Recognition%20in%20Resumes>




###TRAINING
we use the training csv to calculate naive bayes probabilistic classifier
it retains probability of a word falling in a classificaion using maths
<Naive bayes>
<Multinominal naive bayes>
<bag-of-words model>
<Laplace smoothing>


###work flow
so the over all process flow goes like this
1. user registers/logs into site
2. he she uploads resumes
3. Text is extracted from the file using <Apache Tika> and jnius
4. the resume file is segmented into sentences and tokenized into words <nlth> <nlp> <Stanford POS tagger>
5. Noun and noun phrases extracted 
6. extracted things are classified into the classes
7. Each extraction is then used to querly dbpedia to get ontology <SPARQL> <DBPEDIA> <ONTOLOGY>
8. ontoloy information is stored in the database
9. user interacts with sit as necessary



###RANKING
see ranking.py file in UI/spoor
done based firstly on education degree
then ontology and labels are used to give points
the total score is used to rank the candidates











