# Flask User Example 

## What is this?

This is a Flask app that lets a user signup, logout, and login. It is the simplest way I could find to do it. 
No fluff. No BS. Just information in plain English. This is not meant for production. This is a mini guide explaining 
what certain words and concepts mean.

### Who is this for?

This is for folks who are learning to write python web apps for the first time. This is for folks who didn't get CS
degrees. If you don't know anything about storing passwords, this is for you. If you don't know anything about using 
a database with Flask, this is for you. This doesn't explain SQL fully. I hope to add that in the future. This is for 
someone who knows a little bit of Flask, but hasn't connected it to a database. 

### Why did you make this?

I made this because when I first started learning web development I didn't have anything like this example. People tried to 
teach me but they used fancy phrase like "password hashing", "salting", "user sessions", and "type coercion". That didn't help me.
I wanted a way for people to learn that didn't use spooky words. I wanted something in plain English.

### What do I need to know before using this?

You need to know how to run a Flask app. You need to understand how to write a couple lines of SQL. If you're rusty on 
SQL, keep reading, hopefully this will shed some light.

## The Basics

### Python

This repo uses the `.format()` function. Seasoned python users forget how uncommon `format` is among new coders.

The `.format()` function is a function that every string has. It replaces brackets like `{}` with a variable. For 
example:

```python
the_authors_name = 'Adam'
greeting = 'My name is {}'.format(the_authors_name)
print(greeting)
# >>> 'My name is Adam'
friends_name = 'Bob'
friendship = '{} is friends with {}'.format(the_authors_name, friends_name)
print(friendship)
# >>> 'Adam is friends with Bob'
```

Why should you do this instead of `the_authors_name + ' is friends with ' + friends_name`?

The example above only worked because the variables were strings. If you did `1 + ' is less that ' + 2`, it would throw 
an error. `'{} is less than {}.format(1, 2)` will not throw an error. The fancy name for what this is doing is called 
"type coercion". That's a fancy way of say "changing the type so things don't error". You should always use `.format()` 
for building things like sentences. I use them in this project to build our SQL queries, which are just sentences.

#### Python 3.6.X

I'm going to talk about something called "f-strings". This is only supported in python 3.6+, but it's good that people 
see it as often as possible so we can all move to new versions of python together. Below is the exact same as the above code, 
but it uses the "f-string" style.

```python
the_authors_name = 'Adam'
greeting = f'My name is {the_authors_name}'
print(greeting)
# >>> 'My name is Adam'
friends_name = 'Bob'
friendship = f'{the_authors_name} is friends with {friends_name}'
print(friendship)
# >>> 'Adam is friends with Bob'
```

Don't worry about "f-strings" too much. I just want people to see them bit by bit until they become more mainstream in python.

### Passwords

#### Hashing

When you go to Facebook and type in your password, Facebook doesn't know your password. They know a scrambled version 
of your password called a "password hash". The one of the reasons you store a password this way is that if Facebook ever got 
hacked the hacker would only have hashes, not real passwords.

Most _hashed_ passwords are impossible to reverse into their plain passwords. How is this possible? How can Facebook know your password 
is right if they don't know the real thing? Scrambling, or _hashing_ a password is destructive. It removes information from what is being scrambled. 

Imagine your password was `abcdefghijk`. Lets say our scrambler removed every other letter. The scrambled password or _hash_ would be `acegik`. If someone 
stole this hash, they would have no idea what your full password is. If you came to our site and provided the correct password 
we'd be able to remove every other letter and it would match the hash we stored. *This only works if the scrambling process is the same every time.*

Doesn't that mean someone could use a password like `a1c1e1g1i1k` and get into our site? Yes. That's because our hashing example  
is simple. Websites use a much more complicated method of destruction.

The method of destruction is called a _salt_. In the example I just gave, our salt was removing every other letter. In web apps 
the salt usually uses the application's _secret key_ to determine how to scramble. Lets say our secret key was `abefij` and our 
salt method was "remove every letter from a password that is in our secret key". If our original password is still `abcdefghijk`, 
then our sale would be `cdghk`. As you can imagine, salting/hashing can get really complex really quickly.

### Talking to the internet

When an app sends information to the internet or gets information, the info is usually in the form of an _http request_. Lets say 
I'm a user and you're a computer. If I want to _get_ information from you, I might send you a text that says "What's up?". Me asking 
you for info is called a GET. The text I sent you is an HTTP Request. If you response and say "Not much, just hanging out.", that 
is an HTTP Response. 

If I want to _give_ you information, like "Lets grab lunch tomorrow at noon", that is a POST. When you reply "Sounds good", that 
is also an HTTP Response.

# READ ME TODOS: 

db connections
spooky syntax like the unused exception and all the decorators
setup application
connection and cursor
database commits and why
database close connection
why not doc strings