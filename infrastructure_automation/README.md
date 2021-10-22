## Scribble Stadium Data Science Infrastructure Automation Design Document

 The current state of the Scribble Stadium Data Science Infrastructure has several pain points that are outlined below
-   Manual deployment process to AWS Elastic Beanstalk  
-   Non functional end -to end and integration testing
 -   Non-centralized data storage to store data and model artefacts across the Data Science side of the application
 -   Manual Tesseract OCR model testing and monitoring processes
 -   Lack of data tracking and logging for analytics purposes
    
One of our major tasks is to outline a path to addressing some of the pain points indicated above. Our hope is to take advantage of a lot of recent progress around building large scale ML systems, which in our case is the Data Infrastructure at Scribble Stadium. The product is currently still in beta with a limited user base. Once it goes fully operational / live, we hope this infrastructure design will both be scalable and extensible to support user growth over time and support stakeholder requirements

*See figure below for a our current proposal for the future DS Infrastructure*

![](https://lh4.googleusercontent.com/r5Z_9I-H7yFORBA23DIoM7Vw-zHO507Z12YgU6kbFtMLcZY6YDxMgEyQJGy9HaQjQ0XrkVRAKCj8U0GUaPoL4wSqyavHS8bL-DitwuSD7VdRVZQlxXVnl353eTTu-CVOfgWAdyUh=s1600)
*Fig (1) : Proposed Scribble Stadium Data Science Infrastructure*

In line with this vision, these are five major areas we believe will benefit from this automation exercise

  *   **Code Deployment** - Currently, we wrap all Data Science interactions with Engineering behind API endpoints. We do not currently deploy a model as the current transcription pipeline is supported by the Google Vision API. Our hope is to eventually replace this with our custom Tesseract OCR model. The Tesseract model is a `*.traineddata` object. Our hope is that this will perform transcription across all services on the product - including the Word Cloud feature and other future planned features that would rely on transcription / illustrations.
    
*   **Model Monitoring** Once we have an operational Tesseract model in production, we‘ll have to be able to track the performance of this model and check for model degradation. If this detection there should be a way for the model to be refreshed or updated by training on new data. The model monitoring and refresh process ideally needs to automated as there might be several other internal services tied to it
	* The last couple steps of the Metaflow workflow outlined in the *Model Training Infrastructure* section below, will be dedicated to monitoring the model.

* **Automated Data EDA** - We now have a tool that enables auto data cleaning. Giving this a command line interface and Integrating It into the Data Lake and the rest of the infrastructure should also be automated
    
*  **Model Training Infrastructure** - Our current model training infrastructure is an AWS EC2 instance with Tesseract installed and built from source. The process of setting up the Tesseract training infrastructure isn’t trivial but we believe this process can be automated as well - setting up the EC2 machines, using build script to install all necessary packages and then building them from source, doing all the necessary data transfers, model training, model tuning and performance analytics on serialized Tesseract OCR models
	* Tasha Upchurch put together this nice overview what the Infrastructure would look like: https://whimsical.com/9yxUF9BxXf3Ee2S6ku3prE
	* We are currently working on getting a Docker container configured so we can be training the models on local machines with much better CPU's and GPU's. This will vastly reduce the time needed for training the models. 
	* Utilizing **Metaflow** will be paramount in automating the training infrastructure. Here's the basic layout for Metaflow steps
		* Get raw data
		* Clean data
		* Pre-process
		* Parallel steps for training model with different params.
		* Compare training results *(Model monitoring)*
		* Store results in DB *(Model monitoring)*
    
*   **Module Integration** - As shown in Fig(1), our proposed infrastructure will constitute several different modules, including an Analytics module that will sit between Data Storage and the ML Engine (not shown in diagram). The different modules have to be very tightly coupled and integrated. To achieve this, we’ll have to outline all the requirements and connections between modules and make a determination on which ones can be automated

*See figure below for some tooling recommendation to get to this future state*
![](https://lh3.googleusercontent.com/shbz05ePRTWgDj3j9q02DvI0YMAQ9sArbows3ZjAF-emJBGx0XxRkHqY5BdfYVHkoqMlZRBVMn7yUL0h_2_6XMUIe3O9dxk9h_eriPppztXVdk6mwap1kKKD1gUQTL-MFt_n6fH5=s1600)
*Fig (2) : Proposed Scribble Stadium Data Science Tech Stack*

**References:**
1. [ML System Design Deck](https://docs.google.com/presentation/d/195ZF74cxa_MOZ8j2aVQdWyhz2NTxi4OtvqrAcEKX2pI/edit#slide=id.gb04f10a9dd_0_305)
2. [ML System Design Video](https://drive.google.com/file/d/1w3_cTJBaPb93WeR6cxBLJLX84mjt-amh/view?usp=sharing)
3. [Scaling ML as a Service](http://proceedings.mlr.press/v67/li17a/li17a.pdf)
4. [Metaflow overview](https://www.youtube.com/watch?v=2zbnJ37R7DQ)
