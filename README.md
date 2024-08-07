# The whs-calculation package
The package aims at calculating a golf player index according to the world handicap system from scorecards recorded with the [popular golfshot](https://golfshot.com/) app.

# How it works
1. The package will scrape the scorecards saved with your golshot account
2. An sqlite database will be created with 3 related tables:
  * courses: the courses played (Id, name)
  * holes: holes details (hcp, distance, par, ...) for all the teeboxes of a course
  * scores: the scoring and round detail (date, starting teebox, course hcp, strokes, ....) of all the holes played by a player
3. A table summarizing your rounds and calculating your playing handicap (Index) based on your last 20 rounds will be generated (printed in the terminal)



# Instructions (if direnv & .env are setup)
Once the repository is cloned locally and the package is installed (with `make reinstall_package`)

`cd` in the root directory of the repository and run the following `make` commands in your terminal (after editing the `.env` file)

``` shell
# scrape your golfshot account
make scrape_golfshot

# create / refresh a sqlite database
make sql_database

# print your index table
make run_main
```
--------------------------

# -- Setup direnv & .env --
In order to be able to configure the behavior of the package 📦 depending on the values of the variables defined in a .env project configuration file.

**💻 First install the direnv shell extension.**

Its job is to locate the nearest .env file in the parent directory structure of the project and load its content into the environment.
``` shell
# MacOS
brew install direnv

# Ubuntu (Linux or Windows WSL2)
sudo apt update
sudo apt install -y direnv
```
Once direnv is installed, configure zsh to load direnv whenever the shell starts

``` shell
# with VS CODE configured
code ~/.zshrc

# otherwise simply locate and edit the file in your favorite text editor
```
Add `direnv` to the end of your list of plugins in your .zshrc

When you’re done, it should look something like this:
``` shell
plugins=(git gitfast ... direnv)
```
Start a new zsh window in order to load direnv

**💻 At this point, direnv is still not able to load anything, as there is no .env file, so let’s create one:**

1. Duplicate the env.sample file and rename the duplicate as .env

2. Enable the project configuration with:
```shell
direnv allow .
```
3. 🧪 Check that direnv is able to read the environment variables from the .env file:
``` shell
# return in the shell your USER_NAME entry in the .env file...
echo $USER_NAME
```
From now on, every time you need to update the behavior of the project:

Edit .env, save it
Then
```shell
# to reload your env variables 🚨🚨
direnv reload .
```
