# se_project

## 
This repository contains a web application, which allows to retrieve statistics of a selected GitHub user from the GitHub API, in particular:
- a list of repositories together with the number of stars (stargazers) in each repository, 
- the total number of stars in all repositories, 
- used languages, together with the number of bytes of code written by the user in each language.
  
  
### Instructions to run the app
  
To run the app follow these steps:  
1. Create a parent directory.  
2. Clone this repository into the parent directory, either using the Git command (recommended)    
`git clone https://github.com/m-kosik/se_project.git`  
or by downloading the repository manually as a ZIP file and extracting in the parent directory.  
3. Create a virtual environment. It is recommended to use a virtual environment to avoid conflicts between various package versions. To create a virtual evironment, you can follow the [official Python documentation](https://docs.python.org/3/tutorial/venv.html#creating-virtual-environments). Please make sure you create an environment with Python 3.  
4. Activate the virtual environment, enter the downloaded `se_project` directory and install dependecies which are listed in `requirements.txt` by typing:  
`pip install -r requirements.txt` 
5. Enter the `app` directory and run:   
`python3 user_stats.py` 
7. Finally, open the address http://localhost:8080/ in your web browser. This is where you should find the app.  
  
  
### How to use the app?
  
The repositories with corresponding star amounts and the total number of stargazers will always be printed in the output. Listing the languages takes significantly more time than just listing the repositories, therefore this functionality is optional.
  
In the main screen, provide the username of the user you want to scan and determine whether you want to see the most used languages (type "y" for yes and "n" for no). Depending on the number of repositories that the selected user has published on his profile, this action can take from several seconds up to several minutes.  
  
**WARNING**  
Please note that there is an hourly API access limit imposed by GitHub on unauthenticated users.   
After the limit is reached, the requested information will be obtained by scraping the GitHub profile of the user. Therefore, only the 30 first repositories together with the starcount in them will be listed. The list of used languages will only contain languages which have been used in those 30 repositories and will be printed without specifying their usage in bytes. Moreover, the statistics for organisation accounts (like Microsoft) will not be presented correctly.  
  
The **output file** is formatted as a JSON and it contains the following information:
- `GH_limit_reached` - contains information whether the GitHub API access limit has been reached (`true`) or not (`false`),
- `repositories` - a dictionary containing repository names as keys and the number of stars in each repository as corresponding values,
- `total_stars` - the total number of stars in all repositories,
- `used_languages` - a dictionary containing used languages as keys and the number of bytes of code written by the user in each language as corresponding values,
- `username` - the username of the user for which the search has been performed.
  
  
### Ideas for further improvement
- **Enabling authenticated requests** would help to overcome the GitHub API access per IP limit for unauthenticated users and improve the usability of the app.
- Using **asynchronous API calls** is another promising idea for improving the app performance. In the case when a user has a large number of repositories even the simple operation of counting total stars takes a significant amount of time, and listing the used languages is even slower. Using asynchronous requests would very likely speed up executing these actions.  
- **Creating a cache** for saving requests could be another means to fight the problem with the GitHub API access limit. Every time a call is made, the retrieved data can be stored in a temporary cache, thus allowing to access it again directly from the local machine without the need to send another request. This would also make the repeated calls much quicker than downloading data from the GitHub API.  
- **Testing** on a mock server would be a good way to find any potential defects of the app, reduce its flaws and ensure that it is reliable.  