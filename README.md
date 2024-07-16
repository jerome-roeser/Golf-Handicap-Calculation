# whs-calculation
calculate a golf player index according to the world handicap system from recorded golfshot scorecards

# how it will work
The package will scrape your golshot account
An sqlite database will be created with all the holes you played
A table summarizing your rounds and calculating your playing handicap (Index) based on your last 20 rounds will be generated



# instructions (if direnv & .env are setup)
Once the repository is cloned locally and the package is installed (with `make reinstall_package`)

``` shell
# scrape your golfsshot account
make scrape_golfshot

# create a sqlite database
make sql_database

# print your index table
make run-main
```


# Setup direnv & .env
Our goal is to be able to configure the behavior of our package 📦 depending on the value of the variables defined in a .env project configuration file.

**💻 In order to do so, we will install the direnv shell extension.** Its job is to locate the nearest .env file in the parent directory structure of the project and load its content into the environment.
``` shell
# MacOS
brew install direnv

# Ubuntu (Linux or Windows WSL2)
sudo apt update
sudo apt install -y direnv
```
Once direnv is installed, we need to tell zsh to load direnv whenever the shell starts

``` shell
code ~/.zshrc
```
Add `direnv` to the end of your list of plugins in your .zshrc When you’re done, it should look something like this:
``` shell
plugins=(git gitfast ... direnv)
```
Start a new zsh window in order to load direnv

**💻 At this point, direnv is still not able to load anything, as there is no .env file, so let’s create one:**

1. Duplicate the env.sample file and rename the duplicate as .env

2. **Enable the project configuration with:**
```shell
direnv allow .
```
3. 🧪 Check that direnv is able to read the environment variables from the .env file:
``` shell
echo $USER_NAME
# should return your USER_NAME entry in the .env file...
```
From now on, every time you need to update the behavior of the project:

Edit .env, save it
Then
```shell
direnv reload . # to reload your env variables 🚨🚨
```
