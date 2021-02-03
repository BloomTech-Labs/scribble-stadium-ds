# Scraped Illustrations
contained within is scraped data pulled from Google Images for testing and model-building. The images were searched and grade on a 1-3 scale. 1 being preschool-kindergarten typical skill level, 2 being gradeschool ranged skill,  3 being highschool+ level. 

### Work Flow:
1. The images were scraped using [this tool](https://github.com/debadridtt/Scraping-Google-Images-using-Python)
Different search queries were used at different levels, and many were translated into different languages(using google translate) in order to yield more unique results.
2. Next, the scraped images were hand processed. Images were cropped, relocated to different grade levels if needed, or deleted if irrelevant/duplicates.
3. Once organized, folders are compressed. 

### Uses/Next Steps:
These images can be used for testing pre-trained models, or used to train an independent model. For this, they would need to have a corresponding CSV with the image titles and grades.

Queries: 
1:
- preschoolers drawings
- Kinderzeichnungen von 3 bis 6 Jahren
- kids drawings
- first grader pencil drawings
- Bocetos infantiles de 3 a 6 años
- 5 year old sketches
- 3歳から6歳までの子供の絵
2:
- 5th grade drawings
- dessins d'élèves du collège
- dibujos a lapiz de secundaria
- middle school drawings
- middle school pencil drawings
- middle school sketches
- 中学生の絵
3:
- disegni delle scuole superiori (<10 images)
- grade 11 drawings
- High School Bleistiftkunst
- high school drawings
- high school pencil art
- high school sketches
- 高中铅笔艺术