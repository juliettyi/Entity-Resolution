# Entity-Resolution

##Description

In this project, we implement a python script names EntityResolution.py to resolve the records from two datasets Scholar.csv (64260 records) and DBLP1.csv (2616 records), and writes a final .csv file named “DBLP_Scholar_perfecMapping_YiChen.csv” that only contains the resolved entities.
 
##Files Included in This Project
 
Scholar.csv- input dataset
DBLP1.csv-input dataset
DBLP_Scholar_perfecMapping_YiChen.csv- required output dataset
EntityResolution.py – python script for the project
 
##Resolution Criteria and Assumptions

-Author name entered as: first name initial, middle name initial and last name, different author separated by comma.
- Entities are considered to be resolved if they can match the following fields: title, author, venue and year. All the matching fields will be normalized when needed before matching.
- Match criteria as follow:
  - Title: title should be exact match
  - Author: at least one author match if authors from both datasets are available
  - Year: exact match if years from both datasets are available
  - Venue: match based on field value as well as an additional manually created mapping from the knowledge of the datasets
 
##Resolution Algorithm
1.Title normalization:
- Remove punctuations
- Convert to lower cases
- Remove excessive spaces
- Example:
  “ZOO  :  A Desktop Experiment Management Environment” and
  “ZOO: A Desktop Experiment Management Environment” will be normalized to
  “zoo a desktop experiment management environment” and hence are an exact match
 
2.Author normalization
- Split each author by comma
- Convert to lower cases
- Keep first letter of first name and last name
 
3.Venue normalization
- Convert to lower cases
- Remove excessive spaces
- Remove punctuations
- Manually create a mapping between the two datasets based on common knowledge
 
4.Resolve strategy:
- First match title, for each entry that has exact match of title, then check author, venue and year
- Author: if both fields are not null, and no common author, then reject the resolution by author
- Venue: if both fields are not null and cannot be matched, then reject the resolution by venue
- Year: if both fields are not null and the year cannot be exactly matched, then reject the resolution by year 
 
##To Run the Program
python resolve.py

##Current Result and Future Work
Based on the current program, 2103 records are generated in the output file. There are still some future work can be done to improve the precision and number of resolved cases. For example, there are a number of titles such as “Editor’s Notes” with missing information. To achieve a better resolution, we will need the combination of the following:
- add more mappings of venues
- add more name mappings for common misspelling or variations.
- separate matching logic for common titles such as "Editor's Notes"
- Establish human evaluation process to judge the effectiveness and correctness of new matching rules.
