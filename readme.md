# dj

python cli package for creating django models and views in a single command.

### Install

Pull the code from github and install dj through `setup.py`.

```sh
$ cd dj
$ python setup.py install
```

### To list all installed local apps:

```sh
dj list
```

### To create a new model:

1. cd into the django project (ie, into the directory where `manage.py` exists)

2. Command format for creating new model.

```sh
dj create model <model-name> <app-name>
```

we can use `c` for `create` and `m` for model in the above format.

3. The below command will create a new model `Book` inside `student` app.

```sh
dj c m Book student
```

### To create a new view:

```sh
dj c v BookView student
```

![selection_005](https://user-images.githubusercontent.com/3929632/31307339-2225b692-ab80-11e7-842b-fef686d9c3b7.png)