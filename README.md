# se_project

## 
This repository contains a web application, which allows to retrieve statistics of a selected GitHub user from the GitHub API, in particular:
- a list of repositories together with the number of stars (stargazers) in each repository, 
- the total number of stars in all repositories, 
- used languages, together with the nubmer of bytes of code written by the user in each language.


### Instructions

To use the app follow these steps:  
1. Create a parent directory.  
2. It is recommended to use a virtual environment to avoid conflicts between various package versions.   
To create a virtual evironment, you can follow [official Python documentation](https://docs.python.org/3/tutorial/venv.html#creating-virtual-environments).  
3. Activate the virtual environment and install dependecies which are listed in `requirements.txt`.  
4. Clone this repository into the parent directory.  
5. Enter the `/app` directory (the same directory in which `user_stats.py` is located) and set up the name of the application to run to `user_stats`.  
On Windows (PowerShell) use the command:  
`$env:FLASK_APP = 'user_stats'`  
On Linux use the command:  
`export FLASK_APP = user_stats`  
6. Next, run the app using the following command:  
`flask run`  
7. Finally, open the address http://127.0.0.1:5000/ in your web browser (or any other address if you specified a different port, the address will be printed out in your terminal).  
  

### Ideas for further improvement
- **Enabling authenticated requests** would help to overcome the GitHub API access per IP limit for unauthenticated users and improve the usability of the app.
- Using **asynchronous API calls** is another promising idea for improving the app performance. In the case when a user has a large number of repositories even the simple operation of counting the total stars takes a significant amount of time, and listing the used languages is even slower. Using asynchronous requests would very likely speed up executing these actions.  
- **Creating a cache** for saving requests could be another means to fight the problem with the GitHub API access limit. Every time a call is made, the retrieved data can be stored in a temporary cache, thus allowing to access it again directly from the local machine without the need to send another request. This would also make the repeated calls much quicker than downloading data from the GitHub API.  
- **Testing** on a mock server would be a good way to find any potential defects of the app, reduce its flaws and ensure that it is reliable.  